from odoo import models, fields, api
import hashlib
from datetime import datetime, timedelta

class StockReorderContract(models.Model):
    _name = 'stock.reorder.contract'
    _description = 'Smart Contract Réapprovisionnement Auto'
    _order = 'trigger_date desc'
    
    name = fields.Char(string="Référence", readonly=True, default='New')
    product_id = fields.Many2one('stock.product', string="Produit", required=True, readonly=True)
    trigger_date = fields.Datetime(string="Date Déclenchement", default=fields.Datetime.now, readonly=True)
    trigger_quantity = fields.Float(string="Quantité au Déclenchement", readonly=True)
    threshold = fields.Float(string="Seuil Configuré", readonly=True)
    order_quantity = fields.Float(string="Quantité à Commander", required=True)
    supplier_id = fields.Many2one('res.partner', string="Fournisseur", domain=[('supplier_rank', '>', 0)])
    expected_delivery_date = fields.Date(string="Livraison Prévue", compute='_compute_expected_delivery')
    
    state = fields.Selection([
        ('draft', 'Brouillon'),
        ('triggered', 'Déclenché'),
        ('validated', 'Validé Blockchain'),
        ('ordered', 'Commandé'),
        ('received', 'Reçu'),
        ('cancelled', 'Annulé')
    ], default='draft', string="État", required=True)
    
    # Blockchain Fields
    contract_hash = fields.Char(string="Hash Contrat", readonly=True)
    previous_hash = fields.Char(string="Hash Précédent", readonly=True)
    validation_hash = fields.Char(string="Hash Validation", readonly=True)
    blockchain_timestamp = fields.Datetime(string="Timestamp Blockchain", readonly=True)
    
    # Entry link when received
    entry_id = fields.Many2one('stock.entry', string="Entrée de Stock", readonly=True)
    
    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code('stock.reorder.contract') or 'RC-' + str(datetime.now().timestamp())
        return super(StockReorderContract, self).create(vals)
    
    @api.depends('trigger_date', 'product_id.lead_time_days')
    def _compute_expected_delivery(self):
        for record in self:
            if record.trigger_date and record.product_id.lead_time_days:
                trigger_dt = fields.Datetime.from_string(record.trigger_date)
                record.expected_delivery_date = (trigger_dt + timedelta(days=record.product_id.lead_time_days)).date()
            else:
                record.expected_delivery_date = False
    
    def action_validate_contract(self):
        """Validate contract using blockchain"""
        for rec in self:
            # Skip if already validated
            if rec.state not in ['draft', 'triggered']:
                continue
                
            # IMPORTANT: Search for the previous contract that was already validated
            # This creates the blockchain chain by linking to previous validation_hash
            last_contract = self.search([
                ('product_id', '=', rec.product_id.id),
                ('id', '<', rec.id),  # Only contracts created before this one
                ('validation_hash', '!=', False),  # Must have been validated
                ('blockchain_timestamp', '!=', False)  # Must have blockchain timestamp
            ], order='blockchain_timestamp desc', limit=1)
            
            # Link to previous contract's validation_hash (this creates the chain)
            previous = last_contract.validation_hash if last_contract else '0'
            
            # Create contract hash using all important data
            contract_data = f"{rec.product_id.id}|{rec.trigger_quantity}|{rec.threshold}|{rec.order_quantity}|{rec.trigger_date}|{previous}"
            contract_hash_value = hashlib.sha256(contract_data.encode()).hexdigest()
            
            # Create validation hash (simulates consensus/block validation)
            validation_data = f"{contract_hash_value}|{rec.supplier_id.id if rec.supplier_id else 'NO_SUPPLIER'}|{datetime.now()}"
            validation_hash_value = hashlib.sha256(validation_data.encode()).hexdigest()
            
            # Write all blockchain fields at once
            rec.write({
                'previous_hash': previous,
                'contract_hash': contract_hash_value,
                'validation_hash': validation_hash_value,
                'blockchain_timestamp': fields.Datetime.now(),
                'state': 'validated'
            })
            
            # Auto-execute if supplier is configured
            if rec.supplier_id:
                rec.action_create_order()
    
    def action_create_order(self):
        """Simulate order creation (in real system, this would create a purchase order)"""
        for rec in self:
            if rec.state != 'validated':
                continue
            
            rec.state = 'ordered'
            
            # Here you would integrate with Odoo's purchase module
            # For now, we just mark it as ordered
            # self.env['purchase.order'].create({...})
    
    def action_receive_stock(self):
        """Manually mark as received and create stock entry"""
        for rec in self:
            if rec.state != 'ordered':
                continue
            
            # Create stock entry
            entry = self.env['stock.entry'].create({
                'product_id': rec.product_id.id,
                'quantity': rec.order_quantity,
                'location_id': self.env['stock.location.custom'].search([], limit=1).id,
                'state': 'draft'
            })
            
            # Confirm and complete the entry
            entry.action_confirm()
            entry.action_set_done()
            
            rec.entry_id = entry.id
            rec.state = 'received'
    
    def action_cancel(self):
        """Cancel the contract"""
        for rec in self:
            rec.state = 'cancelled'
    
    def verify_blockchain_integrity(self):
        """Verify blockchain chain integrity"""
        for rec in self:
            if not rec.previous_hash:
                continue
            
            # Find previous contract
            prev_contract = self.search([
                ('validation_hash', '=', rec.previous_hash)
            ], limit=1)
            
            if not prev_contract:
                return {
                    'valid': False,
                    'message': f'Chaîne brisée: Hash précédent non trouvé'
                }
            
            # Verify current hash
            contract_data = f"{rec.product_id.id}|{rec.trigger_quantity}|{rec.threshold}|{rec.order_quantity}|{rec.trigger_date}|{rec.previous_hash}"
            expected_hash = hashlib.sha256(contract_data.encode()).hexdigest()
            
            if expected_hash != rec.contract_hash:
                return {
                    'valid': False,
                    'message': f'Hash invalide pour contrat {rec.name}'
                }
        
        return {
            'valid': True,
            'message': 'Blockchain valide ✓'
        }

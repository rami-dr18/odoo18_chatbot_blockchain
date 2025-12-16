from odoo import models, fields, api
import hashlib

class StockProduct(models.Model):
    _name = 'stock.product'
    _description = 'Produit Stock'
    _rec_name = 'name'

    name = fields.Char(string="Nom du produit", required=True)
    quantity = fields.Float(string="Quantité en stock", default=0)    
    # Champ calculé pour le statut
    status = fields.Char(string="Statut", compute='_compute_status', store=True)
    
    # Smart Contract Auto-Reorder Fields
    auto_reorder_enabled = fields.Boolean(string="Activer Réapprovisionnement Auto", default=False)
    reorder_threshold = fields.Float(string="Seuil de Réapprovisionnement", default=10.0)
    reorder_quantity = fields.Float(string="Quantité à Commander", default=50.0)
    supplier_id = fields.Many2one('res.partner', string="Fournisseur par Défaut", domain=[('supplier_rank', '>', 0)])
    lead_time_days = fields.Integer(string="Délai Livraison (jours)", default=7)

    @api.depends('quantity')
    def _compute_status(self):
        for record in self:
            record.status = "Disponible" if record.quantity > 0 else "Rupture"
            
            # Trigger smart contract when threshold is reached
            if record.auto_reorder_enabled and record.quantity <= record.reorder_threshold:
                record._trigger_smart_contract_reorder()
    
    def _trigger_smart_contract_reorder(self):
        """Smart Contract: Automatically creates reorder when threshold is hit"""
        # Check if there's already a pending reorder for this product
        existing_contract = self.env['stock.reorder.contract'].search([
            ('product_id', '=', self.id),
            ('state', 'in', ['draft', 'triggered', 'ordered'])
        ], limit=1)
        
        if existing_contract:
            # Contract already exists, don't create duplicate
            return
        
        # Create new smart contract
        contract = self.env['stock.reorder.contract'].create({
            'product_id': self.id,
            'trigger_quantity': self.quantity,
            'threshold': self.reorder_threshold,
            'order_quantity': self.reorder_quantity,
            'supplier_id': self.supplier_id.id if self.supplier_id else False,
            'state': 'triggered'
        })
        
        # Execute blockchain validation
        contract.action_validate_contract()
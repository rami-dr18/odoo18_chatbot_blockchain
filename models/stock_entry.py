from odoo import models, fields
import hashlib

class StockEntry(models.Model):
    _name = "stock.entry"
    _description = "Entrée de Stock"

    product_id = fields.Many2one('stock.product', string="Produit", required=True)
    quantity = fields.Float("Quantité", required=True)

    location_id = fields.Many2one('stock.location.custom', string="Emplacement", required=True)

    date = fields.Date("Date", default=fields.Date.context_today)
    state = fields.Selection([
        ('draft', 'Brouillon'),
        ('confirmed', 'Confirmé'),
        ('done', 'Terminé')
    ], default='draft', string="Statut")
    tx_hash = fields.Char(string="Hash Transaction", readonly=True)
    previous_hash = fields.Char(string="Hash précédent", readonly=True)

    def action_confirm(self):
        for rec in self:
            rec.state = 'confirmed'

    def action_set_done(self):
        for rec in self:
            if rec.state != 'done':
                # Récupérer la dernière transaction "done" pour ce produit
                last_tx = self.search([
                    ('product_id', '=', rec.product_id.id),
                    ('state', '=', 'done')
                ], order='create_date desc', limit=1)
                rec.previous_hash = last_tx.tx_hash if last_tx else '0'

                # Calculer le hash actuel
                data = f"{rec.product_id.id}|{rec.quantity}|{rec.previous_hash}|{rec.date}"
                rec.tx_hash = hashlib.sha256(data.encode()).hexdigest()

                # Mettre à jour le stock
                rec.state = 'done'
                rec.product_id.sudo().write({
                    'quantity': rec.product_id.quantity + rec.quantity
                })

    def action_reset(self):
        for rec in self:
            rec.state = 'draft'

    # --- Blockchain ---
    def check_chain_integrity(self, product_id):
        txs = self.search([('product_id', '=', product_id), ('state', '=', 'done')], order='create_date')
        previous = '0'
        for tx in txs:
            # Vérifier previous_hash
            if tx.previous_hash != previous:
                return False, f"Hash précédent incorrect pour la transaction {tx.id}"

            # Recalculer le hash actuel (même logique que action_set_done)
            data = f"{tx.product_id.id}|{tx.quantity}|{tx.previous_hash}|{tx.date}"
            recalculated_hash = hashlib.sha256(data.encode()).hexdigest()
            if tx.tx_hash != recalculated_hash:
                return False, f"Hash incorrect pour la transaction {tx.id}"

            previous = tx.tx_hash
        return True, "Chaîne intègre"

    # --- Bouton vérification intégrité ---
    def action_check_integrity(self):
        for rec in self:
            is_valid, msg = self.check_chain_integrity(rec.product_id.id)
            if is_valid:
                return {
                    'type': 'ir.actions.client',
                    'tag': 'display_notification',
                    'params': {
                        'title': "Succès",
                        'message': msg,
                        'type': 'success',
                        'sticky': False,
                    }
                }
            else:
                return {
                    'type': 'ir.actions.client',
                    'tag': 'display_notification',
                    'params': {
                        'title': "Erreur",
                        'message': msg,
                        'type': 'danger',
                        'sticky': True,
                    }
                }
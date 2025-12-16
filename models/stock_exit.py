from odoo import models, fields
import hashlib

class StockExit(models.Model):
    _name = "stock.exit"
    _description = "Sortie de Stock"

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
                if rec.quantity > rec.product_id.quantity:
                    raise ValueError(f"Quantité insuffisante pour {rec.product_id.name}")

                # Récupérer la dernière transaction "done" pour ce produit
                last_tx = self.search([
                    ('product_id', '=', rec.product_id.id),
                    ('state', '=', 'done')
                ], order='create_date desc', limit=1)
                rec.previous_hash = last_tx.tx_hash if last_tx else '0'

                # Calculer le hash actuel
                data = f"{rec.product_id.id}|{rec.quantity}|{rec.previous_hash}"
                rec.tx_hash = hashlib.sha256(data.encode()).hexdigest()

                # Mettre à jour le stock
                rec.state = 'done'
                rec.product_id.sudo().write({
                    'quantity': rec.product_id.quantity - rec.quantity
                })

    def action_reset(self):
        for rec in self:
            rec.state = 'draft'

from odoo import models, fields, api
from odoo.exceptions import UserError

class StockMoveCustom(models.Model):
    _name = 'stock.move.custom'
    _description = 'Mouvement de Stock'

    product_id = fields.Many2one('stock.product', string="Produit", required=True)
    quantity = fields.Float(string="Quantité", required=True)

    location_from_id = fields.Many2one('stock.location.custom', string="Depuis", required=True)
    location_to_id = fields.Many2one('stock.location.custom', string="Vers", required=True)

    scheduled_date = fields.Datetime(string="Date", required=True, default=fields.Datetime.now)

    @api.model
    def create(self, vals):
        rec = super().create(vals)
        rec.apply_movement()
        return rec

    def write(self, vals):
        res = super().write(vals)
        self.apply_movement()
        return res

    def apply_movement(self):
        for rec in self:
            product = rec.product_id.sudo()
            if rec.location_from_id:
                if product.quantity < rec.quantity:
                    raise UserError("Quantité insuffisante pour ce produit dans l'emplacement source.")
                product.sudo().write({'quantity': product.quantity - rec.quantity})

            if rec.location_to_id:
                product.sudo().write({'quantity': product.quantity + rec.quantity})

from odoo import models, fields

class StockLocation(models.Model):
    _name = 'stock.location.custom'
    _description = 'Emplacement de Stock'

    name = fields.Char(string="Nom de l’emplacement", required=True)

    # Produits présents dans cet emplacement (plusieurs)
    product_ids = fields.Many2many(
        'stock.product',      # Modèle lié
        string="Produits",    # Nom affiché
        relation='stock_location_product_rel',  # Nom de la table relationnelle
        column1='location_id', 
        column2='product_id'
    )
    

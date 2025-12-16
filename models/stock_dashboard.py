from odoo import models, fields, api
from datetime import date

class StockDashboard(models.Model):
    _name = 'stock.dashboard'
    _description = 'Dashboard Stock'

    today_entries = fields.Float(
        " Entrées",
        digits=(16, 0)  # 0 décimale
    )
    today_exits = fields.Float(
        " Sorties",
        digits=(16, 0)  # 0 décimale
    )
    total_quantity = fields.Float(
        " Total produits en stock",
        digits=(16, 0)  # 0 décimale
    )
    out_of_stock_count = fields.Integer(
        " Produits en rupture",
        digits=(16, 0)
    )

    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)

        StockEntry = self.env['stock.entry']
        StockExit = self.env['stock.exit']
        StockProduct = self.env['stock.product']
        today = fields.Date.context_today(self)

        res['today_entries'] = sum(StockEntry.search([('date', '=', today), ('state', '=', 'done')]).mapped('quantity'))
        res['today_exits'] = sum(StockExit.search([('date', '=', today), ('state', '=', 'done')]).mapped('quantity'))
        res['total_quantity'] = sum(StockProduct.search([]).mapped('quantity'))
        res['out_of_stock_count'] = StockProduct.search_count([('quantity', '=', 0)])

        return res

    def get_dashboard_data(self):
        """Bouton Actualiser si besoin"""
        today = fields.Date.context_today(self)
        StockEntry = self.env['stock.entry']
        StockExit = self.env['stock.exit']
        StockProduct = self.env['stock.product']

        self.today_entries = sum(StockEntry.search([('date', '=', today), ('state', '=', 'done')]).mapped('quantity'))
        self.today_exits = sum(StockExit.search([('date', '=', today), ('state', '=', 'done')]).mapped('quantity'))
        self.total_quantity = sum(StockProduct.search([]).mapped('quantity'))
        self.out_of_stock_count = StockProduct.search_count([('quantity', '=', 0)])
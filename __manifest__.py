{
    'name': 'Gestion de Stock Custom',
    'version': '1.0',
    'author': 'Your Name',
    'category': 'Inventory',
    'summary': 'Module personnalisé pour la gestion des produits, entrées et sorties de stock',
    'depends': [
        'base',
        'stock',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/menu.xml',
        'views/product_views.xml',
        'views/stock_entry_views.xml',
        'views/stock_exit_views.xml',
        'views/stock_dashboard_views.xml',
        'views/stock_reorder_contract_views.xml',
        'views/smartchat_views.xml',
        'views/stock_location_views.xml',
        'views/stock_move_views.xml',
    ],


    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}

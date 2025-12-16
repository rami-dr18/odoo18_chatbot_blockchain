from odoo import models, fields, api
import requests
import json
from datetime import datetime

class SmartChatBot(models.Model):
    _name = 'smart.chat.bot'
    _description = 'Smart ChatBot avec IA'
    _order = 'date desc'

    user_id = fields.Many2one('res.users', string='Utilisateur', default=lambda self: self.env.user, readonly=True)
    message = fields.Text(string='Votre Message', required=True)
    response = fields.Text(string='Réponse IA', readonly=True)
    date = fields.Datetime(string="Date", default=lambda self: fields.Datetime.now(), readonly=True)
    
    def send_smart_message(self):
        """Envoyer le message à l'IA et obtenir la réponse"""
        for rec in self:
            if not rec.message:
                rec.response = "Veuillez écrire un message."
                return
                
            try:
                # Appeler la fonction pour obtenir la réponse intelligente
                ai_response = self.get_smart_response(rec.message)
                rec.response = ai_response
                rec.date = fields.Datetime.now()
            except Exception as e:
                rec.response = f"Erreur: {str(e)}"
    
    def get_smart_response(self, user_msg):
        """Obtenir une réponse intelligente basée sur la base de données"""
        # STEP 1: Query your database
        products = self.env['stock.product'].search_read([], ['name', 'quantity', 'status', 'auto_reorder_enabled', 'reorder_threshold', 'reorder_quantity'])
        locations = self.env['stock.location.custom'].search_read([], ['name'])
        entries = self.env['stock.entry'].search_count([('state', '=', 'done')])
        exits = self.env['stock.exit'].search_count([('state', '=', 'done')])
        
        # Produits en rupture
        rupture_products = self.env['stock.product'].search_read([('quantity', '<=', 0)], ['name', 'quantity'])
        
        # Smart Contracts Information
        active_contracts = self.env['stock.reorder.contract'].search_read([
            ('state', 'in', ['triggered', 'validated', 'ordered'])
        ], ['name', 'product_id', 'state', 'order_quantity', 'trigger_date', 'supplier_id'])
        
        completed_contracts = self.env['stock.reorder.contract'].search_count([('state', '=', 'received')])
        pending_contracts = self.env['stock.reorder.contract'].search_count([('state', 'in', ['triggered', 'validated', 'ordered'])])
        
        # Products with auto-reorder enabled
        auto_reorder_products = self.env['stock.product'].search_read([
            ('auto_reorder_enabled', '=', True)
        ], ['name', 'quantity', 'reorder_threshold', 'reorder_quantity', 'supplier_id'])
        
        # STEP 2: Build context from database
        context = f"""
Base de données de gestion de stock:
- Produits disponibles: {json.dumps(products, ensure_ascii=False)}
- Emplacements: {json.dumps(locations, ensure_ascii=False)}
- Total entrées validées: {entries}
- Total sorties validées: {exits}
- Produits en rupture: {json.dumps(rupture_products, ensure_ascii=False)}

Smart Contracts de Réapprovisionnement Automatique:
- Contrats actifs (en cours): {json.dumps(active_contracts, ensure_ascii=False)}
- Total contrats complétés: {completed_contracts}
- Total contrats en attente: {pending_contracts}
- Produits avec réapprovisionnement auto activé: {json.dumps(auto_reorder_products, ensure_ascii=False)}

Instructions IMPORTANTES:
- Réponds en français de manière claire et conversationnelle
- NE PAS utiliser de markdown (pas de **, ##, -, etc.)
- Écris en texte simple et naturel
- Utilise des émojis pour rendre la réponse conviviale
- Formate les listes avec des numéros simples (1., 2., 3.) ou des tirets simples
- Utilise les données ci-dessus pour répondre aux questions
- Sois précis avec les chiffres et les noms
- Garde un ton amical et professionnel
- Si on te demande sur les smart contracts ou réapprovisionnement automatique, utilise les données des contrats
- Explique l'état des contrats: triggered (déclenché), validated (validé blockchain), ordered (commandé), received (reçu)
"""
        
        # STEP 3: Send to AI with database context
        response = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": "Bearer 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",
                "Content-Type": "application/json"
            },
            data=json.dumps({
                "model": "mistralai/devstral-2512:free",
                "messages": [
                    {
                        "role": "system",
                        "content": context
                    },
                    {
                        "role": "user",
                        "content": user_msg
                    }
                ]
            }),
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            return result['choices'][0]['message']['content']
        else:
            return f"Erreur API: {response.status_code} - {response.text}"
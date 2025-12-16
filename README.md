# Gestion de Stock Custom - Odoo Module

Module Odoo personnalisé pour la gestion intelligente des stocks avec smart contracts blockchain et assistant IA.

## 📋 Description

Ce module offre une solution complète de gestion des stocks avec des fonctionnalités avancées incluant :
- Gestion des produits avec alertes automatiques
- Entrées et sorties de stock
- Smart contracts de réapprovisionnement automatique avec blockchain
- Dashboard de visualisation en temps réel
- Assistant chatbot IA pour analyser vos stocks
- Gestion des emplacements et mouvements de stock

## ✨ Fonctionnalités principales

### 🎯 Dashboard Stock
- Vue d'ensemble des entrées/sorties du jour
- Total des produits en stock
- Alertes de rupture de stock
- Métriques en temps réel

### 📦 Gestion des Produits
- Fiche produit complète (référence, nom, catégorie)
- Suivi des quantités en stock
- Statut automatique (en stock, stock bas, rupture)
- Prix unitaire et valeur totale
- Gestion des emplacements de stockage

### 🔄 Smart Contracts de Réapprovisionnement
- **Réapprovisionnement automatique** basé sur des seuils
- **Validation blockchain** avec hash cryptographique
- États du contrat : Brouillon → Déclenché → Validé → Commandé → Reçu
- Traçabilité complète avec horodatage blockchain
- Lien avec les fournisseurs et délais de livraison
- Création automatique d'entrées de stock lors de la réception

#### Configuration du Smart Contract
1. Activez le réapprovisionnement auto sur un produit
2. Définissez le seuil de déclenchement
3. Configurez la quantité à commander
4. Associez un fournisseur
5. Le contrat se déclenche automatiquement quand le stock atteint le seuil

### 📥 Entrées de Stock
- Enregistrement des réceptions de marchandises
- Lien avec les produits et emplacements
- États : Brouillon → Confirmé → Réceptionné
- Mise à jour automatique des quantités

### 📤 Sorties de Stock
- Enregistrement des expéditions/consommations
- Gestion des motifs de sortie
- États : Brouillon → Confirmé → Expédié
- Vérification des quantités disponibles

### 📍 Emplacements de Stock
- Organisation par zones/emplacements
- Traçabilité des produits par emplacement
- Capacité et occupation des emplacements

### 🔀 Mouvements de Stock
- Historique complet des mouvements
- Traçabilité des transferts entre emplacements
- Types de mouvement (entrée, sortie, transfert)

### 🤖 Smart ChatBot IA
- Assistant intelligent pour analyser votre stock
- Réponses en français
- Analyse contextuelle de votre base de données
- Questions supportées :
  - "Quels produits sont en rupture ?"
  - "Combien de contrats sont actifs ?"
  - "Quel est l'état de mon stock ?"
  - "Quels produits ont le réapprovisionnement automatique ?"

## 📦 Installation

### Prérequis
- Odoo 15.0 ou supérieur
- Module `base` (core)
- Module `stock` (core)
- Python 3.8+

### Étapes d'installation

1. Clonez le repository dans votre dossier `addons` :
```bash
cd /path/to/odoo/addons
git clone <repository-url> gestion_stock_custom
```

2. Redémarrez le serveur Odoo :
```bash
./odoo-bin -c /path/to/odoo.conf --stop-after-init
./odoo-bin -c /path/to/odoo.conf
```

3. Mettez à jour la liste des modules dans Odoo :
   - Allez dans Applications
   - Cliquez sur "Mettre à jour la liste des applications"

4. Recherchez et installez "Gestion de Stock Custom"

## 🚀 Utilisation

### Configuration initiale

1. **Créer des emplacements** :
   - Menu : Gestion de Stock → Emplacements
   - Définissez vos zones de stockage

2. **Ajouter des produits** :
   - Menu : Gestion de Stock → Produits
   - Remplissez les informations produit
   - Assignez un emplacement

3. **Configurer le réapprovisionnement automatique** (optionnel) :
   - Sur la fiche produit, cochez "Réappro. Auto"
   - Définissez le seuil et la quantité
   - Sélectionnez un fournisseur

### Workflow Smart Contract

```
Stock atteint le seuil
    ↓
Contrat créé automatiquement (état: triggered)
    ↓
Validation blockchain avec hash cryptographique
    ↓
Contrat validé (état: validated)
    ↓
Commande passée au fournisseur (état: ordered)
    ↓
Réception marchandise → Entrée de stock créée
    ↓
Contrat complété (état: received)
```

### Utiliser le ChatBot IA

1. Menu : Gestion de Stock → Smart ChatBot IA
2. Créez un nouveau message
3. Posez votre question en français
4. Cliquez sur "Envoyer Message"
5. La réponse s'affiche automatiquement

## 🛠️ Structure technique

### Modèles

- `stock.product` - Gestion des produits
- `stock.entry` - Entrées de stock
- `stock.exit` - Sorties de stock
- `stock.reorder.contract` - Smart contracts blockchain
- `stock.dashboard` - Dashboard et statistiques
- `stock.location.custom` - Emplacements de stockage
- `stock.move` - Mouvements de stock
- `smart.chat.bot` - Assistant IA
- `product.alert` - Alertes produits

### Sécurité

Les règles d'accès sont définies dans `security/ir.model.access.csv`.

### Vues

- Dashboard avec widgets KPI
- Formulaires et listes pour chaque modèle
- Vue arbre avec filtres intelligents
- Actions et boutons contextuels

## 🔐 Blockchain & Sécurité

Le module utilise un système de hash cryptographique (SHA-256) pour garantir l'intégrité des smart contracts :
- Chaque contrat a un hash unique
- Les contrats sont chaînés (hash précédent)
- Validation immuable avec timestamp
- Traçabilité complète

## 🤝 Contribution

Les contributions sont les bienvenues ! Pour contribuer :

1. Forkez le projet
2. Créez une branche pour votre fonctionnalité (`git checkout -b feature/AmazingFeature`)
3. Committez vos changements (`git commit -m 'Add some AmazingFeature'`)
4. Pushez vers la branche (`git push origin feature/AmazingFeature`)
5. Ouvrez une Pull Request

## 📝 Licence

Ce module est sous licence **LGPL-3**.

## 👤 Auteur

**Your Name**

## 📞 Support

Pour toute question ou problème :
- Ouvrez une issue sur GitHub
- Contactez l'équipe de support

## 🔄 Versions

### v1.0 (Décembre 2025)
- Release initiale
- Smart contracts avec blockchain
- Dashboard interactif
- ChatBot IA intégré
- Gestion complète des stocks

## 📸 Captures d'écran

_Ajoutez vos captures d'écran ici pour montrer l'interface du module_

## ⚠️ Notes importantes

- Les smart contracts nécessitent la configuration d'un fournisseur
- Le ChatBot IA analyse uniquement les données de votre base Odoo locale
- Les seuils de réapprovisionnement doivent être configurés pour chaque produit
- La blockchain est simulée localement (pas de réseau distribué)

---

Made with ❤️ for Odoo

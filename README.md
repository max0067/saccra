# 🌙 SACRA - Guide Spirituel IA

**SACRA** est une plateforme web d'interprétation spirituelle par IA qui permet aux utilisateurs d'obtenir des interprétations personnalisées de leurs rêves, signes, synchronicités et tirages intuitifs.

## ✨ Fonctionnalités

### Version Gratuite (3 interprétations/mois)
- 🌙 **Interprétation de rêves** - Décrypte les messages de ton inconscient
- ✨ **Signes & Synchronicités** - Décode les messages de l'univers (nombres miroirs, animaux totems, etc.)
- 🔮 **Tirage intuitif** - Tire 3 cartes et reçois une guidance spirituelle
- 💫 **Profil spirituel** - Découvre ton type d'âme, élément dominant et couleur vibratoire

### Version Premium (9,90€/mois ou 49€/an)
- Interprétations illimitées
- Historique complet de toutes tes interprétations
- Journal spirituel personnel
- Guide IA avec contexte utilisateur

## 🛠 Stack Technique

- **Backend** : Python 3 + Flask
- **Base de données** : SQLite (pour le MVP)
- **IA** : OpenAI GPT-4o-mini
- **Paiements** : Stripe Checkout
- **Authentification** : Flask-Login
- **Frontend** : HTML + TailwindCSS + Vanilla JS
- **Hébergement** : o2switch (Passenger)

## 📦 Installation

### 1. Cloner le projet
```bash
git clone <repo-url>
cd saccra
```

### 2. Créer un environnement virtuel
```bash
python3 -m venv venv
source venv/bin/activate  # Sur Windows: venv\Scripts\activate
```

### 3. Installer les dépendances
```bash
pip install -r requirements.txt
```

### 4. Configuration
Copier `.env.example` vers `.env` et compléter les clés API :
```bash
cp .env.example .env
```

Éditer `.env` avec tes clés :
- `OPENAI_API_KEY` : Clé API OpenAI (https://platform.openai.com/api-keys)
- `STRIPE_PUBLIC_KEY` et `STRIPE_SECRET_KEY` : Clés Stripe (https://dashboard.stripe.com/)
- `SECRET_KEY` : Une clé secrète aléatoire pour Flask

### 5. Créer les produits Stripe
1. Aller sur https://dashboard.stripe.com/products
2. Créer 2 produits :
   - **SACRA Premium Mensuel** : 9,90€/mois (récurrent)
   - **SACRA Premium Annuel** : 49€/an (récurrent)
3. Copier les `price_id` dans `.env`

### 6. Lancer l'application
```bash
python app.py
```

L'application sera accessible sur `http://localhost:5000`

## 🚀 Déploiement sur o2switch

### 1. Uploader les fichiers
Uploader tous les fichiers du projet sur ton serveur o2switch via FTP/SFTP.

### 2. Configuration Python
S'assurer que Python 3.9+ est installé sur le serveur o2switch.

### 3. Installer les dépendances
```bash
pip install -r requirements.txt --user
```

### 4. Configuration Passenger
Le fichier `passenger_wsgi.py` est déjà configuré pour o2switch.

### 5. Variables d'environnement
Configurer les variables d'environnement sur o2switch (panneau de contrôle ou fichier `.env`).

### 6. Domaine
Pointer le domaine `sacra.fr` vers le répertoire du projet.

## 📝 Structure du projet

```
saccra/
├── app/
│   ├── __init__.py              # Factory Flask
│   ├── models.py                # Modèles de données
│   ├── routes/
│   │   ├── main.py              # Routes principales (accueil, dashboard)
│   │   ├── auth.py              # Authentification (login, register)
│   │   ├── interpretations.py  # Interprétations (rêves, signes, tirage)
│   │   └── premium.py           # Abonnements Stripe
│   ├── services/
│   │   └── ai_service.py        # Service OpenAI
│   ├── templates/               # Templates HTML
│   │   ├── base.html
│   │   ├── index.html
│   │   ├── dashboard.html
│   │   ├── auth/
│   │   ├── interpretations/
│   │   └── premium/
│   └── static/
│       ├── css/
│       ├── js/
│       └── images/
├── config.py                    # Configuration
├── app.py                       # Point d'entrée (développement)
├── passenger_wsgi.py            # Point d'entrée (production o2switch)
├── requirements.txt             # Dépendances Python
├── .env.example                 # Exemple de configuration
├── .gitignore
└── README.md
```

## 🎨 Design

Le design suit une esthétique **mystique, apaisante et bienveillante** :
- Couleurs : dégradé beige, doré, lavande, violet
- Typographie : Cormorant Garamond (titres) + Montserrat (texte)
- Animations douces et effet de frappe progressive
- Interface responsive et minimaliste

## 🔐 Sécurité

- Mots de passe hashés avec Werkzeug
- Sessions sécurisées avec Flask-Login
- Validation des entrées utilisateur
- Clés API stockées dans variables d'environnement
- Webhooks Stripe sécurisés

## 📊 Modèle économique

- **Gratuit** : 3 interprétations/mois
- **Premium** : 9,90€/mois ou 49€/an
  - Interprétations illimitées
  - Historique complet
  - Journal spirituel

## 🌟 Évolutions futures

- Notifications email pour signes à ne pas ignorer
- Journal spirituel avec édition Markdown
- Export PDF des interprétations
- Intégration vocale (dictée de rêves)
- Communauté et partage d'interprétations
- Application mobile

## 📧 Support

Pour toute question : contact@sacra.fr

---

🌙 **SACRA** - Laisse ton âme te parler ✨

#!/usr/bin/env python3
"""
Script pour initialiser les contenus éditables du site SACCRA
"""
from app import create_app
from app.models import db, SiteContent

app = create_app()

# Tous les contenus du site organisés par catégorie
CONTENTS = [
    # Page d'accueil
    {
        'key': 'home_title',
        'category': 'Accueil',
        'value': 'Explore ton chemin spirituel avec l\'IA',
        'description': 'Titre principal de la page d\'accueil'
    },
    {
        'key': 'home_subtitle',
        'category': 'Accueil',
        'value': 'SACCRA est ton guide spirituel personnel propulsé par l\'intelligence artificielle. Interprète tes rêves, décode les signes de l\'univers, et découvre ton profil spirituel unique.',
        'description': 'Sous-titre de la page d\'accueil'
    },
    {
        'key': 'home_cta_button',
        'category': 'Accueil',
        'value': 'Commencer mon voyage spirituel',
        'description': 'Texte du bouton principal'
    },

    # Section Fonctionnalités
    {
        'key': 'feature_dream_title',
        'category': 'Fonctionnalités',
        'value': 'Interprétation des rêves',
        'description': 'Titre de la fonctionnalité rêves'
    },
    {
        'key': 'feature_dream_desc',
        'category': 'Fonctionnalités',
        'value': 'Découvre la signification profonde de tes rêves avec une analyse symbolique personnalisée',
        'description': 'Description de la fonctionnalité rêves'
    },
    {
        'key': 'feature_signs_title',
        'category': 'Fonctionnalités',
        'value': 'Signes & Synchronicités',
        'description': 'Titre de la fonctionnalité signes'
    },
    {
        'key': 'feature_signs_desc',
        'category': 'Fonctionnalités',
        'value': 'Comprends les messages que l\'univers t\'envoie : nombres miroirs, animaux totems, coïncidences',
        'description': 'Description de la fonctionnalité signes'
    },
    {
        'key': 'feature_tarot_title',
        'category': 'Fonctionnalités',
        'value': 'Tirage intuitif',
        'description': 'Titre de la fonctionnalité tarot'
    },
    {
        'key': 'feature_tarot_desc',
        'category': 'Fonctionnalités',
        'value': 'Reçois une guidance spirituelle à travers un tirage de cartes inspiré et bienveillant',
        'description': 'Description de la fonctionnalité tarot'
    },
    {
        'key': 'feature_profile_title',
        'category': 'Fonctionnalités',
        'value': 'Profil spirituel',
        'description': 'Titre de la fonctionnalité profil'
    },
    {
        'key': 'feature_profile_desc',
        'category': 'Fonctionnalités',
        'value': 'Découvre ton type d\'âme, ton élément dominant et ta couleur vibratoire personnelle',
        'description': 'Description de la fonctionnalité profil'
    },

    # Page Rêves
    {
        'key': 'dream_page_title',
        'category': 'Interprétations',
        'value': 'Interprétation de rêves',
        'description': 'Titre de la page d\'interprétation des rêves'
    },
    {
        'key': 'dream_page_subtitle',
        'category': 'Interprétations',
        'value': 'Raconte ton rêve et reçois une interprétation spirituelle personnalisée',
        'description': 'Sous-titre de la page rêves'
    },
    {
        'key': 'dream_placeholder',
        'category': 'Interprétations',
        'value': 'Exemple : J\'ai rêvé que je volais au-dessus d\'un océan turquoise...',
        'description': 'Placeholder du champ de saisie des rêves'
    },
    {
        'key': 'dream_submit_button',
        'category': 'Interprétations',
        'value': 'Recevoir mon interprétation',
        'description': 'Texte du bouton de soumission rêves'
    },

    # Page Signes
    {
        'key': 'sign_page_title',
        'category': 'Interprétations',
        'value': 'Signes & Synchronicités',
        'description': 'Titre de la page signes'
    },
    {
        'key': 'sign_page_subtitle',
        'category': 'Interprétations',
        'value': 'Décris le signe que tu as remarqué et découvre son message spirituel',
        'description': 'Sous-titre de la page signes'
    },
    {
        'key': 'sign_placeholder',
        'category': 'Interprétations',
        'value': 'Exemple : Je vois 11:11 partout, un papillon blanc est entré chez moi...',
        'description': 'Placeholder du champ de saisie des signes'
    },

    # Page Tarot
    {
        'key': 'tarot_page_title',
        'category': 'Interprétations',
        'value': 'Tirage intuitif',
        'description': 'Titre de la page tarot'
    },
    {
        'key': 'tarot_page_subtitle',
        'category': 'Interprétations',
        'value': 'Tire 3 cartes et reçois ta guidance spirituelle',
        'description': 'Sous-titre de la page tarot'
    },
    {
        'key': 'tarot_instructions',
        'category': 'Interprétations',
        'value': 'Respire profondément, concentre-toi sur ta question intérieure, puis choisis 3 cartes.',
        'description': 'Instructions pour le tirage tarot'
    },

    # Page Profil Spirituel
    {
        'key': 'profile_page_title',
        'category': 'Profil',
        'value': 'Découvre ton profil spirituel',
        'description': 'Titre de la page profil spirituel'
    },
    {
        'key': 'profile_page_subtitle',
        'category': 'Profil',
        'value': 'Réponds à quelques questions pour révéler ton type d\'âme et ton essence énergétique',
        'description': 'Sous-titre de la page profil'
    },

    # Premium
    {
        'key': 'premium_title',
        'category': 'Premium',
        'value': 'Deviens membre Premium',
        'description': 'Titre de la page premium'
    },
    {
        'key': 'premium_subtitle',
        'category': 'Premium',
        'value': 'Accède à des interprétations illimitées et à des fonctionnalités exclusives',
        'description': 'Sous-titre premium'
    },
    {
        'key': 'premium_benefit_1',
        'category': 'Premium',
        'value': 'Interprétations illimitées',
        'description': 'Premier avantage premium'
    },
    {
        'key': 'premium_benefit_2',
        'category': 'Premium',
        'value': 'Historique complet de tes interprétations',
        'description': 'Deuxième avantage premium'
    },
    {
        'key': 'premium_benefit_3',
        'category': 'Premium',
        'value': 'Analyses plus détaillées et approfondies',
        'description': 'Troisième avantage premium'
    },
    {
        'key': 'premium_benefit_4',
        'category': 'Premium',
        'value': 'Nouvelles fonctionnalités en avant-première',
        'description': 'Quatrième avantage premium'
    },
    {
        'key': 'premium_price',
        'category': 'Premium',
        'value': '9,99€',
        'description': 'Prix de l\'abonnement premium'
    },
    {
        'key': 'premium_cta',
        'category': 'Premium',
        'value': 'Passer Premium maintenant',
        'description': 'Bouton call-to-action premium'
    },

    # Footer
    {
        'key': 'footer_tagline',
        'category': 'Footer',
        'value': 'Ton guide spirituel personnel propulsé par l\'IA',
        'description': 'Slogan dans le footer'
    },
    {
        'key': 'footer_copyright',
        'category': 'Footer',
        'value': '© 2025 SACCRA. Tous droits réservés.',
        'description': 'Copyright dans le footer'
    },

    # Messages système
    {
        'key': 'login_required_message',
        'category': 'Système',
        'value': 'Connecte-toi pour accéder à cette page',
        'description': 'Message quand connexion requise'
    },
    {
        'key': 'limit_reached_message',
        'category': 'Système',
        'value': 'Tu as atteint ta limite mensuelle. Passe en Premium pour des interprétations illimitées',
        'description': 'Message limite freemium atteinte'
    },
    {
        'key': 'error_generic',
        'category': 'Système',
        'value': 'Une erreur est survenue. Réessaye dans quelques instants.',
        'description': 'Message d\'erreur générique'
    },
]

with app.app_context():
    print("🔮 Initialisation des contenus du site SACCRA...\n")

    added = 0
    updated = 0

    for content_data in CONTENTS:
        # Vérifier si le contenu existe déjà
        existing = SiteContent.query.filter_by(key=content_data['key']).first()

        if existing:
            # Mettre à jour si la valeur a changé
            if existing.value != content_data['value']:
                existing.value = content_data['value']
                existing.category = content_data['category']
                existing.description = content_data['description']
                updated += 1
                print("✏️  Mis à jour: {}".format(content_data['key']))
        else:
            # Créer nouveau contenu
            new_content = SiteContent(
                key=content_data['key'],
                category=content_data['category'],
                value=content_data['value'],
                description=content_data['description']
            )
            db.session.add(new_content)
            added += 1
            print("➕ Ajouté: {}".format(content_data['key']))

    db.session.commit()

    print("\n✅ Terminé!")
    print("📊 {} contenus ajoutés".format(added))
    print("📝 {} contenus mis à jour".format(updated))
    print("\n🌐 Accède à la gestion sur: https://saccra.fr/admin/site-contents")

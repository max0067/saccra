"""
Script pour initialiser les contenus modifiables de la page d'accueil

Usage: python seed_home_contents.py
"""
from app import create_app
from app.models import db, SiteContent

app = create_app()

# Contenus de la page d'accueil
HOME_CONTENTS = [
    # Hero Section
    {
        'key': 'home_hero_badge',
        'category': 'Accueil - Hero',
        'value': '🆕 Nouveau : Coach Spirituel avec réponses vocales !',
        'description': 'Badge de nouveauté en haut de la page d\'accueil'
    },
    {
        'key': 'home_hero_title',
        'category': 'Accueil - Hero',
        'value': 'Ton guide spirituel personnel',
        'description': 'Titre principal de la page d\'accueil (ligne 1)'
    },
    {
        'key': 'home_hero_subtitle',
        'category': 'Accueil - Hero',
        'value': 'disponible 24/7',
        'description': 'Sous-titre du hero (ligne 2, en gradient)'
    },
    {
        'key': 'home_hero_tagline',
        'category': 'Accueil - Hero',
        'value': 'Guidance empathique • Réponses audio personnalisées • Disponible 24/7',
        'description': 'Tagline sous le titre principal'
    },
    {
        'key': 'home_hero_cta_primary',
        'category': 'Accueil - Hero',
        'value': 'Commencer gratuitement ✨',
        'description': 'Bouton principal du hero'
    },
    {
        'key': 'home_hero_cta_secondary',
        'category': 'Accueil - Hero',
        'value': 'Découvrir →',
        'description': 'Bouton secondaire du hero'
    },
    {
        'key': 'home_hero_disclaimer',
        'category': 'Accueil - Hero',
        'value': '✓ 5 messages gratuits par jour • ✓ Pas de carte bancaire requise',
        'description': 'Texte sous les boutons du hero'
    },

    # Section Nouveautés
    {
        'key': 'home_features_badge',
        'category': 'Accueil - Nouveautés',
        'value': '🚀 NOUVEAUTÉS',
        'description': 'Badge de la section nouveautés'
    },
    {
        'key': 'home_features_title',
        'category': 'Accueil - Nouveautés',
        'value': 'Une expérience spirituelle réinventée',
        'description': 'Titre de la section nouveautés'
    },
    {
        'key': 'home_features_subtitle',
        'category': 'Accueil - Nouveautés',
        'value': 'Découvre les fonctionnalités innovantes qui rendent SACRA unique',
        'description': 'Sous-titre de la section nouveautés'
    },

    # Coach Spirituel Card
    {
        'key': 'home_coach_title',
        'category': 'Accueil - Nouveautés',
        'value': 'Coach Spirituel',
        'description': 'Titre de la carte Coach'
    },
    {
        'key': 'home_coach_description',
        'category': 'Accueil - Nouveautés',
        'value': 'Discute avec ton guide spirituel personnel en temps réel. Pose toutes tes questions sur le développement personnel, l\'énergie, les relations...',
        'description': 'Description de la carte Coach'
    },

    # Audio Card
    {
        'key': 'home_audio_title',
        'category': 'Accueil - Nouveautés',
        'value': 'Guidance Vocale',
        'description': 'Titre de la carte Audio'
    },
    {
        'key': 'home_audio_description',
        'category': 'Accueil - Nouveautés',
        'value': 'Écoute tes interprétations avec une voix douce et apaisante. Parfait pour méditer ou te détendre.',
        'description': 'Description de la carte Audio'
    },

    # Section Fonctionnalités
    {
        'key': 'home_services_title',
        'category': 'Accueil - Services',
        'value': '4 façons de recevoir ta guidance',
        'description': 'Titre de la section services'
    },
    {
        'key': 'home_services_subtitle',
        'category': 'Accueil - Services',
        'value': 'Choisis le type d\'interprétation qui résonne avec toi',
        'description': 'Sous-titre de la section services'
    },

    # Section Pourquoi SACRA
    {
        'key': 'home_why_title',
        'category': 'Accueil - Pourquoi',
        'value': 'Pourquoi SACRA est différent ?',
        'description': 'Titre de la section pourquoi'
    },
    {
        'key': 'home_why_feature1_title',
        'category': 'Accueil - Pourquoi',
        'value': 'Guidance Empathique',
        'description': 'Titre feature 1'
    },
    {
        'key': 'home_why_feature1_text',
        'category': 'Accueil - Pourquoi',
        'value': 'Un accompagnement bienveillant, chaleureux et intuitif pour ton chemin spirituel',
        'description': 'Texte feature 1'
    },
    {
        'key': 'home_why_feature2_title',
        'category': 'Accueil - Pourquoi',
        'value': 'Personnalisé',
        'description': 'Titre feature 2'
    },
    {
        'key': 'home_why_feature2_text',
        'category': 'Accueil - Pourquoi',
        'value': 'Chaque réponse est adaptée à ton profil spirituel et ton chemin de vie',
        'description': 'Texte feature 2'
    },
    {
        'key': 'home_why_feature3_title',
        'category': 'Accueil - Pourquoi',
        'value': 'Instantané',
        'description': 'Titre feature 3'
    },
    {
        'key': 'home_why_feature3_text',
        'category': 'Accueil - Pourquoi',
        'value': 'Reçois ta guidance en quelques secondes, 24h/24, 7j/7',
        'description': 'Texte feature 3'
    },

    # Section Pricing
    {
        'key': 'home_pricing_title',
        'category': 'Accueil - Pricing',
        'value': 'Choisis ton chemin',
        'description': 'Titre de la section pricing'
    },
    {
        'key': 'home_pricing_subtitle',
        'category': 'Accueil - Pricing',
        'value': 'Commence gratuitement, passe en Premium quand tu veux',
        'description': 'Sous-titre de la section pricing'
    },
    {
        'key': 'home_pricing_free_tagline',
        'category': 'Accueil - Pricing',
        'value': 'Pour découvrir SACRA',
        'description': 'Tagline de l\'offre gratuite'
    },
    {
        'key': 'home_pricing_premium_badge',
        'category': 'Accueil - Pricing',
        'value': '⭐ RECOMMANDÉ',
        'description': 'Badge de l\'offre premium'
    },
    {
        'key': 'home_pricing_premium_tagline',
        'category': 'Accueil - Pricing',
        'value': 'Guidance illimitée',
        'description': 'Tagline de l\'offre premium'
    },
    {
        'key': 'home_pricing_premium_price',
        'category': 'Accueil - Pricing',
        'value': '9,99€',
        'description': 'Prix de l\'offre premium'
    },

    # CTA Final
    {
        'key': 'home_cta_title',
        'category': 'Accueil - CTA Final',
        'value': 'Prêt(e) à commencer ton voyage ?',
        'description': 'Titre du CTA final'
    },
    {
        'key': 'home_cta_subtitle',
        'category': 'Accueil - CTA Final',
        'value': 'Rejoins des milliers de personnes qui utilisent SACRA pour leur développement spirituel',
        'description': 'Sous-titre du CTA final'
    },
    {
        'key': 'home_cta_button',
        'category': 'Accueil - CTA Final',
        'value': 'Créer mon compte gratuit ✨',
        'description': 'Bouton du CTA final'
    },
    {
        'key': 'home_cta_disclaimer',
        'category': 'Accueil - CTA Final',
        'value': 'Inscription en 30 secondes • Pas de carte bancaire',
        'description': 'Disclaimer du CTA final'
    },
]


def seed_home_contents():
    """Ajoute les contenus de la page d'accueil en base de données"""
    with app.app_context():
        print('🏠 Initialisation des contenus de la page d\'accueil...\n')

        # Vérifier si des contenus existent déjà
        existing_count = SiteContent.query.filter(
            SiteContent.category.like('Accueil%')
        ).count()

        if existing_count > 0:
            print(f'⚠️  Il y a déjà {existing_count} contenu(s) d\'accueil en base.')
            response = input('Voulez-vous quand même ajouter ces contenus ? (y/n): ')
            if response.lower() != 'y':
                print('❌ Annulé.')
                return

        # Ajouter chaque contenu
        added = 0
        updated = 0

        for content_data in HOME_CONTENTS:
            # Vérifier si ce contenu existe déjà (par clé)
            existing = SiteContent.query.filter_by(key=content_data['key']).first()

            if existing:
                # Mettre à jour si la valeur a changé
                if existing.value != content_data['value']:
                    existing.value = content_data['value']
                    existing.description = content_data['description']
                    updated += 1
                    print(f'🔄 Mis à jour: {content_data["key"]}')
                else:
                    print(f'⏭️  "{content_data["key"]}" existe déjà, ignoré.')
                continue

            content = SiteContent(
                key=content_data['key'],
                category=content_data['category'],
                value=content_data['value'],
                description=content_data['description']
            )
            db.session.add(content)
            added += 1
            print(f'✅ Ajouté: {content_data["key"]} ({content_data["category"]})')

        if added > 0 or updated > 0:
            db.session.commit()
            print(f'\n✨ {added} contenu(s) ajouté(s) et {updated} mis à jour !')
            print(f'\n💡 Tu peux maintenant modifier ces contenus sur https://saccra.fr/admin/site-contents')
        else:
            print('\n💡 Aucun nouveau contenu ajouté.')


if __name__ == '__main__':
    seed_home_contents()

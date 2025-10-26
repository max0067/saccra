# 📝 Gestion des Contenus du Site

## Vue d'ensemble

Le système de gestion de contenus (CMS) permet de modifier tous les textes du site depuis l'interface admin sans toucher au code.

## Accès

Interface admin: **https://saccra.fr/admin/site-contents**

## Initialisation des contenus

Sur le serveur, exécute une seule fois:

```bash
cd ~/saccra.fr
source venv/bin/activate
python3 init_site_contents.py
```

Cela créera environ 30+ contenus éditables organisés par catégories:
- **Accueil** - Titre, sous-titre, CTA
- **Fonctionnalités** - Descriptions des features
- **Interprétations** - Textes des pages rêves/signes/tarot
- **Premium** - Avantages et pricing
- **Footer** - Copyright, slogan
- **Système** - Messages d'erreur, notifications

## Utilisation dans les templates

### Méthode simple

Dans n'importe quel template Jinja2:

```jinja
<h1>{{ get_content('home_title', 'Titre par défaut') }}</h1>
<p>{{ get_content('home_subtitle') }}</p>
```

### Exemples concrets

**Page d'accueil:**
```jinja
<div class="hero">
    <h1>{{ get_content('home_title', 'Explore ton chemin spirituel') }}</h1>
    <p>{{ get_content('home_subtitle') }}</p>
    <a href="/auth/register" class="btn">
        {{ get_content('home_cta_button', 'Commencer') }}
    </a>
</div>
```

**Page de fonctionnalités:**
```jinja
<div class="feature">
    <h3>{{ get_content('feature_dream_title', 'Interprétation des rêves') }}</h3>
    <p>{{ get_content('feature_dream_desc') }}</p>
</div>
```

**Messages système:**
```jinja
{% if error %}
    <div class="alert">{{ get_content('error_generic', 'Une erreur est survenue') }}</div>
{% endif %}
```

## Ajouter de nouveaux contenus

### Via l'interface admin

1. Va sur https://saccra.fr/admin/site-contents
2. Clique sur "➕ Nouveau Contenu"
3. Remplis:
   - **Clé**: Identifiant unique (ex: `about_mission`)
   - **Catégorie**: Pour organiser (ex: `À propos`)
   - **Valeur**: Le texte à afficher
   - **Description**: Note pour te rappeler où c'est utilisé

### Via le code

Ajoute dans `init_site_contents.py`:

```python
{
    'key': 'about_mission',
    'category': 'À propos',
    'value': 'Notre mission est d\'illuminer ton chemin spirituel',
    'description': 'Mission statement sur la page À propos'
},
```

Puis relance: `python3 init_site_contents.py`

## Bonnes pratiques

### Nommage des clés

Utilise un format cohérent:
- `{page}_{section}_{element}`
- Exemples:
  - `home_hero_title`
  - `premium_pricing_monthly`
  - `footer_copyright_text`

### Catégories

Organise par sections logiques:
- Pages principales: `Accueil`, `Premium`, `À propos`
- Fonctionnalités: `Fonctionnalités`
- Formulaires: `Interprétations`, `Profil`
- Global: `Footer`, `Navigation`, `Système`

### Valeurs par défaut

Toujours fournir une valeur par défaut dans `get_content()`:

```jinja
{# ✅ Bon #}
{{ get_content('home_title', 'Bienvenue sur SACCRA') }}

{# ❌ Éviter (affichera rien si la clé n'existe pas) #}
{{ get_content('home_title') }}
```

## Migration d'un template existant

### Avant:
```html
<h1>Interprétation de rêves</h1>
<p>Raconte ton rêve et reçois une interprétation spirituelle</p>
```

### Après:
```html
<h1>{{ get_content('dream_page_title', 'Interprétation de rêves') }}</h1>
<p>{{ get_content('dream_page_subtitle', 'Raconte ton rêve et reçois une interprétation spirituelle') }}</p>
```

### Étapes:

1. Identifie tous les textes statiques dans le template
2. Crée les entrées correspondantes dans `init_site_contents.py`
3. Exécute `python3 init_site_contents.py`
4. Remplace le texte en dur par `{{ get_content('key', 'default') }}`
5. Teste que tout s'affiche correctement

## Avantages

✅ **Modification sans code** - Change les textes depuis l'admin
✅ **Multilingue** - Facile d'ajouter des traductions plus tard
✅ **A/B Testing** - Teste différents messages facilement
✅ **Historique** - Chaque modification est tracée (updated_at)
✅ **Collaboration** - Les non-développeurs peuvent modifier les textes

## Exemples de modifications courantes

### Changer le prix Premium
```
Clé: premium_price
Valeur: 9,99€ → 7,99€ (promo)
```

### Modifier le message de limite freemium
```
Clé: limit_reached_message
Valeur: Plus d'interprétations ce mois-ci! Passe en Premium ✨
```

### Adapter le ton de la homepage
```
Clé: home_subtitle
Valeur: Ton assistant spirituel intelligent → Explore ta spiritualité avec l'IA
```

## Troubleshooting

### Le contenu ne s'affiche pas

1. Vérifie que la clé existe: `SELECT * FROM site_contents WHERE key='ma_cle';`
2. Vérifie le template: `{{ get_content('ma_cle') }}` bien appelé?
3. Redémarre Passenger: `touch tmp/restart.txt`

### Erreur lors de l'init

```bash
# Vérifier que la table existe
python3 -c "from app import create_app; from app.models import db, SiteContent; app = create_app(); app.app_context().push(); print(SiteContent.query.count())"
```

### Réinitialiser tous les contenus

```bash
python3 << 'EOF'
from app import create_app
from app.models import db, SiteContent
app = create_app()
with app.app_context():
    SiteContent.query.delete()
    db.session.commit()
    print("Tous les contenus supprimés")
EOF

# Puis réinitialiser
python3 init_site_contents.py
```

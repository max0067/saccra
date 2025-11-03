#!/usr/bin/env python3
"""
Script pour ajouter automatiquement les loaders spirituels à tous les templates
"""
import os
import re

TEMPLATES_TO_UPDATE = [
    'app/templates/interpretations/dream.html',
    'app/templates/interpretations/sign.html',
    'app/templates/chat/coach.html',
]

# CSS/JS à ajouter au début du bloc content
LOADER_IMPORTS = """<!-- Spiritual Loader CSS/JS -->
<link rel="stylesheet" href="{{ url_for('static', filename='css/spiritual-loader.css') }}">
<script src="{{ url_for('static', filename='js/spiritual-loader.js') }}"></script>

"""

def add_spiritual_loader_to_template(filepath):
    """Ajoute le loader spirituel à un template"""

    if not os.path.exists(filepath):
        print(f"❌ Fichier non trouvé: {filepath}")
        return False

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Ajouter les imports CSS/JS après {% block content %}
    if 'spiritual-loader.css' not in content:
        content = re.sub(
            r'({% block content %})\n',
            r'\1\n' + LOADER_IMPORTS,
            content
        )

    # 2. Remplacer les loaders simples par des div vides
    # Chercher les patterns de loaders existants
    loader_patterns = [
        (r'<div id="loader"[^>]*>.*?</div>', '<div id="loader" class="hidden"></div>'),
        (r'<div id="loading"[^>]*>.*?</div>', '<div id="loading" class="hidden"></div>'),
    ]

    for pattern, replacement in loader_patterns:
        content = re.sub(pattern, replacement, content, flags=re.DOTALL)

    # 3. Remplacer loader.classList.remove('hidden') par showSpiritualLoader()
    content = re.sub(
        r"loader\.classList\.remove\('hidden'\)",
        "showSpiritualLoader('loader')",
        content
    )

    # 4. Remplacer loader.classList.add('hidden') par hideSpiritualLoader()
    content = re.sub(
        r"loader\.classList\.add\('hidden'\)",
        "hideSpiritualLoader('loader')",
        content
    )

    # 5. Pour les autres patterns (loading au lieu de loader)
    content = re.sub(
        r"loading\.classList\.remove\('hidden'\)",
        "showSpiritualLoader('loading')",
        content
    )

    content = re.sub(
        r"loading\.classList\.add\('hidden'\)",
        "hideSpiritualLoader('loading')",
        content
    )

    content = re.sub(
        r"loading\.style\.display\s*=\s*'block'",
        "showSpiritualLoader('loading')",
        content
    )

    content = re.sub(
        r"loading\.style\.display\s*=\s*'none'",
        "hideSpiritualLoader('loading')",
        content
    )

    # Sauvegarder
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"✅ {filepath} mis à jour")
    return True

if __name__ == '__main__':
    print("=" * 70)
    print("AJOUT DES LOADERS SPIRITUELS")
    print("=" * 70)

    for template_path in TEMPLATES_TO_UPDATE:
        add_spiritual_loader_to_template(template_path)

    print("\n✅ Tous les templates ont été mis à jour !")
    print("\nPense à tester sur le site pour vérifier que tout fonctionne.")

#!/usr/bin/env python3
"""
Script pour créer la table blog_posts dans la base de données
"""
from app import create_app
from app.models import db, BlogPost

app = create_app()

with app.app_context():
    # Créer la table blog_posts
    db.create_all()
    print("✅ Base de données mise à jour")

    # Vérifier si la table existe
    from sqlalchemy import inspect
    inspector = inspect(db.engine)
    tables = inspector.get_table_names()

    if 'blog_posts' in tables:
        print("✅ Table blog_posts créée avec succès")

        # Compter les articles
        count = BlogPost.query.count()
        print(f"📊 Articles de blog actuels: {count}")

        print("\n📝 Prochaines étapes:")
        print("1. Accède à https://saccra.fr/admin/blog pour gérer tes articles")
        print("2. Crée ton premier article avec un titre optimisé SEO")
        print("3. Ajoute une image (utilise Imgur ou Unsplash)")
        print("4. Publie l'article pour qu'il apparaisse sur /blog")
        print("\n💡 Tips SEO:")
        print("- Utilise des mots-clés dans le titre (ex: 'méditation', 'chakras', 'spiritualité')")
        print("- Ajoute une meta description accrocheuse (155 caractères)")
        print("- Inclus des images avec des URLs optimisées")
        print("- Écris au moins 500 mots par article")

    else:
        print("❌ Erreur: la table blog_posts n'a pas été créée")

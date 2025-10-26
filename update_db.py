#!/usr/bin/env python3
"""
Script pour mettre à jour la base de données avec la nouvelle table SiteContent
"""
from app import create_app
from app.models import db, SiteContent

app = create_app()

with app.app_context():
    # Créer la nouvelle table
    db.create_all()
    print("✅ Base de données mise à jour avec la table SiteContent")

    # Vérifier si la table existe
    from sqlalchemy import inspect
    inspector = inspect(db.engine)
    tables = inspector.get_table_names()

    if 'site_contents' in tables:
        print("✅ Table site_contents créée avec succès")

        # Compter les contenus
        count = SiteContent.query.count()
        print("📊 Contenus actuels: {}".format(count))
    else:
        print("❌ Erreur: la table site_contents n'a pas été créée")

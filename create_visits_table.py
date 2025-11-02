#!/usr/bin/env python3
"""
Script pour créer la table visits pour le tracking des visiteurs
"""
from app import create_app
from app.models import db, Visit

app = create_app()

with app.app_context():
    # Créer la table visits
    db.create_all()
    print("✅ Base de données mise à jour")

    # Vérifier si la table existe
    from sqlalchemy import inspect
    inspector = inspect(db.engine)
    tables = inspector.get_table_names()

    if 'visits' in tables:
        print("✅ Table visits créée avec succès")

        # Compter les visites
        count = Visit.query.count()
        print(f"📊 Visites enregistrées: {count}")

        print("\n📈 Fonctionnalités analytics:")
        print("- Tracking automatique de chaque page visitée")
        print("- Visiteurs uniques par jour (hash anonyme IP + User-Agent)")
        print("- Visiteurs en ligne (actifs dans les 5 dernières minutes)")
        print("- Compatible RGPD (pas de stockage d'IP en clair)")
        print("\n💡 Les stats sont visibles dans le dashboard admin:")
        print("   https://saccra.fr/admin/dashboard")

    else:
        print("❌ Erreur: la table visits n'a pas été créée")

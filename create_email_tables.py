#!/usr/bin/env python3
"""
Script pour créer les tables email marketing dans la base de données
"""
from app import create_app
from app.models import db, EmailContact, EmailCampaign, EmailLog

app = create_app()

with app.app_context():
    # Créer les tables email marketing
    db.create_all()
    print("✅ Base de données mise à jour")

    # Vérifier si les tables existent
    from sqlalchemy import inspect
    inspector = inspect(db.engine)
    tables = inspector.get_table_names()

    expected_tables = ['email_contacts', 'email_campaigns', 'email_logs']
    all_created = True

    for table_name in expected_tables:
        if table_name in tables:
            print(f"✅ Table {table_name} créée avec succès")
        else:
            print(f"❌ Erreur: la table {table_name} n'a pas été créée")
            all_created = False

    if all_created:
        # Compter les données
        contacts_count = EmailContact.query.count()
        campaigns_count = EmailCampaign.query.count()
        logs_count = EmailLog.query.count()

        print(f"\n📊 État actuel:")
        print(f"   - Contacts: {contacts_count}")
        print(f"   - Campagnes: {campaigns_count}")
        print(f"   - Logs d'envoi: {logs_count}")

        print("\n📝 Prochaines étapes:")
        print("1. Accède à https://saccra.fr/admin/emails pour gérer l'email marketing")
        print("2. Importe tes contacts depuis un fichier CSV (jusqu'à 70 000 lignes)")
        print("3. Crée ta première campagne d'emailing")
        print("4. Envoie ta campagne à tous tes contacts abonnés")

        print("\n💡 Tips Email Marketing:")
        print("- Format CSV: email,first_name,last_name")
        print("- L'import utilise un traitement par batch (1000 lignes à la fois)")
        print("- Les doublons sont automatiquement ignorés")
        print("- Utilise les variables {{first_name}} et {{email}} dans tes campagnes")
        print("- Surveille tes stats: taux d'ouverture, clics, bounces")

#!/usr/bin/env python3
"""
Script pour synchroniser les statistiques des campagnes avec les EmailLog réels
"""
import sys
import os

# Ajouter le répertoire parent au path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from app.models import db, EmailCampaign, EmailLog

def sync_all_campaigns():
    """Synchronise les stats de toutes les campagnes"""
    app = create_app()

    with app.app_context():
        campaigns = EmailCampaign.query.all()

        print("=" * 70)
        print("SYNCHRONISATION DES STATS DE CAMPAGNE")
        print("=" * 70)

        for campaign in campaigns:
            # Compter les vrais logs
            total_sent = EmailLog.query.filter_by(
                campaign_id=campaign.id,
                status='sent'
            ).count()

            total_opened = EmailLog.query.filter_by(
                campaign_id=campaign.id
            ).filter(EmailLog.opened_at.isnot(None)).count()

            # Afficher avant/après
            print(f"\n📧 Campagne: {campaign.name} (ID: {campaign.id})")
            print(f"   Avant: {campaign.total_sent} envoyés, {campaign.total_opened} ouverts")
            print(f"   Réel:  {total_sent} envoyés, {total_opened} ouverts")

            # Mettre à jour
            campaign.total_sent = total_sent
            campaign.total_opened = total_opened

            if total_sent > 0:
                open_rate = (total_opened / total_sent * 100)
                print(f"   Taux d'ouverture: {open_rate:.1f}%")

        # Sauvegarder
        db.session.commit()

        print("\n" + "=" * 70)
        print("✅ Synchronisation terminée !")
        print("=" * 70)

if __name__ == '__main__':
    sync_all_campaigns()

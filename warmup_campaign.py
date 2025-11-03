#!/usr/bin/env python3
"""
Script de warm-up progressif pour campagne email
Envoie progressivement pour éviter le spam et établir une bonne réputation d'expéditeur

Usage:
    python3 warmup_campaign.py <campaign_id>

Plan de warm-up (14 jours) :
    Jour 1-2:  500 emails/jour
    Jour 3-4:  1000 emails/jour
    Jour 5-6:  2000 emails/jour
    Jour 7-8:  5000 emails/jour
    Jour 9-10: 10000 emails/jour
    Jour 11+:  Volume complet

Recommandation: Lancer ce script une fois par jour
"""
import sys
import os
import json
from datetime import datetime, timedelta
import argparse

# Ajouter le répertoire parent au path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from app.models import db, EmailCampaign, EmailContact, EmailLog

# Fichier de progression du warm-up
WARMUP_PROGRESS_FILE = 'warmup_progress.json'

# Plan de warm-up (jour -> nombre d'emails)
WARMUP_PLAN = {
    1: 500,
    2: 500,
    3: 1000,
    4: 1000,
    5: 2000,
    6: 2000,
    7: 5000,
    8: 5000,
    9: 10000,
    10: 10000,
    # À partir du jour 11, volume complet
}

def load_warmup_progress(campaign_id):
    """Charge la progression du warm-up"""
    if os.path.exists(WARMUP_PROGRESS_FILE):
        with open(WARMUP_PROGRESS_FILE, 'r') as f:
            data = json.load(f)
            if data.get('campaign_id') == campaign_id:
                return data
    return None

def save_warmup_progress(campaign_id, day, total_sent, start_date):
    """Sauvegarde la progression du warm-up"""
    data = {
        'campaign_id': campaign_id,
        'day': day,
        'total_sent': total_sent,
        'start_date': start_date,
        'last_run': datetime.now().isoformat()
    }
    with open(WARMUP_PROGRESS_FILE, 'w') as f:
        json.dump(data, f, indent=2)

def calculate_warmup_day(start_date):
    """Calcule le jour actuel du warm-up"""
    start = datetime.fromisoformat(start_date)
    now = datetime.now()
    days_diff = (now - start).days + 1  # +1 car le premier jour est le jour 1
    return max(1, days_diff)

def get_daily_limit(day):
    """Retourne la limite d'envoi pour un jour donné"""
    return WARMUP_PLAN.get(day, None)  # None = pas de limite (volume complet)

def warmup_send(campaign_id):
    """Effectue l'envoi du jour selon le plan de warm-up"""
    app = create_app()

    with app.app_context():
        # Récupérer la campagne
        campaign = EmailCampaign.query.get(campaign_id)
        if not campaign:
            print(f"❌ Campagne ID {campaign_id} introuvable")
            return

        print("=" * 70)
        print("WARM-UP PROGRESSIF - SACRA EMAIL MARKETING")
        print("=" * 70)
        print(f"\n📧 Campagne: {campaign.name}")
        print(f"   Sujet: {campaign.subject}")

        # Charger ou initialiser la progression
        progress = load_warmup_progress(campaign_id)

        if progress:
            # Warm-up en cours
            start_date = progress['start_date']
            total_sent_before = progress['total_sent']
            current_day = calculate_warmup_day(start_date)

            print(f"\n🔄 Warm-up en cours")
            print(f"   Démarré le: {datetime.fromisoformat(start_date).strftime('%d/%m/%Y')}")
            print(f"   Jour actuel: {current_day}")
            print(f"   Total envoyé: {total_sent_before:,} emails")
        else:
            # Nouveau warm-up
            start_date = datetime.now().isoformat()
            current_day = 1
            total_sent_before = 0

            print(f"\n🆕 Nouveau warm-up")
            print(f"   Démarrage: Aujourd'hui")
            print(f"   Jour 1: {WARMUP_PLAN[1]} emails")

        # Déterminer la limite du jour
        daily_limit = get_daily_limit(current_day)

        if daily_limit is None:
            print(f"\n✅ Warm-up terminé ! (Jour {current_day})")
            print(f"   Tu peux maintenant envoyer en volume complet.")
            print(f"\n💡 Utilise send_campaign_batch.py pour l'envoi complet")
            return

        print(f"\n📊 Plan du jour {current_day}:")
        print(f"   Limite: {daily_limit:,} emails")

        # Compter combien on peut encore envoyer aujourd'hui
        # On vérifie si on a déjà envoyé aujourd'hui
        last_run = progress.get('last_run') if progress else None
        if last_run:
            last_run_date = datetime.fromisoformat(last_run).date()
            today = datetime.now().date()

            if last_run_date == today:
                print(f"\n⚠️  Envoi déjà effectué aujourd'hui ({datetime.fromisoformat(last_run).strftime('%H:%M')})")
                print(f"   Reviens demain pour continuer le warm-up!")
                return

        # Lancer l'envoi avec le script batch
        print(f"\n🚀 Lancement de l'envoi de {daily_limit} emails...")
        print(f"   Batch size: 100")
        print(f"   Délai: 60s entre chaque batch")

        # Importer et lancer le script batch avec limite
        from send_campaign_batch import send_campaign_batch

        send_campaign_batch(
            campaign_id=campaign_id,
            batch_size=100,
            delay=60,
            max_total=daily_limit,
            no_confirm=True
        )

        # Mettre à jour la progression
        total_sent_after = total_sent_before + daily_limit
        save_warmup_progress(campaign_id, current_day, total_sent_after, start_date)

        print(f"\n✅ Jour {current_day} terminé !")
        print(f"   Envoyés aujourd'hui: {daily_limit:,}")
        print(f"   Total: {total_sent_after:,}")

        # Afficher le prochain jour
        next_day = current_day + 1
        next_limit = get_daily_limit(next_day)

        if next_limit:
            print(f"\n📅 Prochain envoi:")
            print(f"   Jour {next_day}: {next_limit:,} emails")
            print(f"   Lance à nouveau ce script demain!")
        else:
            print(f"\n🎉 Warm-up sera terminé demain !")
            print(f"   Tu pourras ensuite envoyer en volume complet.")

def main():
    parser = argparse.ArgumentParser(
        description='Warm-up progressif pour campagne email',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )

    parser.add_argument('campaign_id', type=int, help='ID de la campagne')
    parser.add_argument('--reset', action='store_true',
                       help='Réinitialiser le warm-up (recommencer à zéro)')

    args = parser.parse_args()

    if args.reset:
        if os.path.exists(WARMUP_PROGRESS_FILE):
            os.remove(WARMUP_PROGRESS_FILE)
            print("✅ Warm-up réinitialisé")
        else:
            print("ℹ️  Aucun warm-up en cours")
        return

    warmup_send(args.campaign_id)

if __name__ == '__main__':
    main()

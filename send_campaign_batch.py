#!/usr/bin/env python3
"""
Script d'envoi automatique de campagne par batch
Pour envoyer à des milliers de contacts sans surcharger le serveur SMTP

Usage:
    python3 send_campaign_batch.py <campaign_id> [options]

Options:
    --batch-size SIZE      Nombre d'emails par batch (défaut: 100)
    --delay SECONDS        Délai entre chaque batch en secondes (défaut: 60)
    --max-total MAX        Nombre maximum total d'emails à envoyer
    --resume               Reprendre un envoi interrompu

Exemples:
    # Envoi standard (100 emails par minute)
    python3 send_campaign_batch.py 1

    # Envoi rapide (500 emails toutes les 5 minutes)
    python3 send_campaign_batch.py 1 --batch-size 500 --delay 300

    # Test avec limite
    python3 send_campaign_batch.py 1 --batch-size 10 --max-total 50

    # Reprendre un envoi interrompu
    python3 send_campaign_batch.py 1 --resume
"""
import sys
import os
import time
import json
from datetime import datetime
import argparse

# Ajouter le répertoire parent au path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from app.models import db, EmailCampaign, EmailContact, EmailLog
from app.services.email_service import _send_email
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Fichier de progression
PROGRESS_FILE = 'campaign_progress.json'

def load_progress(campaign_id):
    """Charge la progression d'un envoi précédent"""
    if os.path.exists(PROGRESS_FILE):
        with open(PROGRESS_FILE, 'r') as f:
            data = json.load(f)
            if data.get('campaign_id') == campaign_id:
                return data
    return None

def save_progress(campaign_id, sent_count, failed_count, last_contact_id):
    """Sauvegarde la progression"""
    data = {
        'campaign_id': campaign_id,
        'sent_count': sent_count,
        'failed_count': failed_count,
        'last_contact_id': last_contact_id,
        'timestamp': datetime.now().isoformat()
    }
    with open(PROGRESS_FILE, 'w') as f:
        json.dump(data, f, indent=2)

def clear_progress():
    """Efface le fichier de progression"""
    if os.path.exists(PROGRESS_FILE):
        os.remove(PROGRESS_FILE)

def send_campaign_batch(campaign_id, batch_size=100, delay=60, max_total=None, resume=False, no_confirm=False):
    """
    Envoie une campagne par batch

    Args:
        campaign_id: ID de la campagne
        batch_size: Nombre d'emails par batch
        delay: Délai en secondes entre chaque batch
        max_total: Nombre maximum d'emails à envoyer (None = tous)
        resume: Reprendre un envoi interrompu
        no_confirm: Ne pas demander de confirmation (pour lancement automatique)
    """
    app = create_app()

    with app.app_context():
        # Récupérer la campagne
        campaign = EmailCampaign.query.get(campaign_id)
        if not campaign:
            print(f"❌ Campagne ID {campaign_id} introuvable")
            return

        print("=" * 70)
        print("ENVOI DE CAMPAGNE PAR BATCH - SACRA EMAIL MARKETING")
        print("=" * 70)
        print(f"\n📧 Campagne: {campaign.name}")
        print(f"   Sujet: {campaign.subject}")
        print(f"   Type: {campaign.campaign_type}")

        # Configuration
        smtp_server = os.environ.get('MAIL_SERVER', 'localhost')
        smtp_port = int(os.environ.get('MAIL_PORT', '25'))
        smtp_user = os.environ.get('MAIL_USERNAME', '')
        smtp_password = os.environ.get('MAIL_PASSWORD', '')
        sender_email = os.environ.get('MAIL_DEFAULT_SENDER', 'contact@saccra.fr')

        print(f"\n📨 Configuration:")
        print(f"   Serveur: {smtp_server}:{smtp_port}")
        print(f"   Expéditeur: {sender_email}")
        print(f"   Batch: {batch_size} emails")
        print(f"   Délai: {delay}s entre chaque batch")

        # Charger la progression si demandé
        start_from_id = 0
        total_sent = 0
        total_failed = 0

        if resume:
            progress = load_progress(campaign_id)
            if progress:
                start_from_id = progress['last_contact_id']
                total_sent = progress['sent_count']
                total_failed = progress['failed_count']
                print(f"\n🔄 Reprise de l'envoi:")
                print(f"   Déjà envoyés: {total_sent}")
                print(f"   Échecs: {total_failed}")
                print(f"   Reprise à partir du contact ID: {start_from_id}")

        # Récupérer tous les contacts abonnés
        query = EmailContact.query.filter_by(
            is_subscribed=True,
            is_bounced=False
        )

        if start_from_id > 0:
            query = query.filter(EmailContact.id > start_from_id)

        # Compter le total
        total_contacts = query.count()

        if max_total:
            total_to_send = min(total_contacts, max_total - total_sent)
        else:
            total_to_send = total_contacts

        print(f"\n👥 Contacts:")
        print(f"   Abonnés disponibles: {total_contacts:,}")
        print(f"   À envoyer: {total_to_send:,}")

        if total_to_send == 0:
            print("\n✅ Rien à envoyer!")
            return

        # Estimation du temps
        total_batches = (total_to_send + batch_size - 1) // batch_size
        estimated_time_minutes = (total_batches * delay) / 60

        print(f"\n⏱️  Estimation:")
        print(f"   Batches: {total_batches}")
        print(f"   Temps total: ~{estimated_time_minutes:.1f} minutes ({estimated_time_minutes/60:.1f} heures)")

        # Confirmation (sauf si --no-confirm)
        if not no_confirm:
            print("\n" + "=" * 70)
            response = input("🚀 Démarrer l'envoi ? (y/n): ")
            if response.lower() != 'y':
                print("❌ Envoi annulé")
                return

        print("\n" + "=" * 70)
        print("ENVOI EN COURS...")
        print("=" * 70)
        print("\n💡 Astuce: Appuie sur Ctrl+C pour arrêter proprement\n")

        # Envoi par batch
        contacts = query.limit(total_to_send).all()
        batch_number = 0
        last_contact_id = start_from_id

        try:
            for i in range(0, len(contacts), batch_size):
                batch = contacts[i:i + batch_size]
                batch_number += 1
                batch_sent = 0
                batch_failed = 0

                print(f"\n[Batch {batch_number}/{total_batches}] Envoi de {len(batch)} emails...")

                for contact in batch:
                    try:
                        # Créer le log AVANT l'envoi pour avoir l'ID (pour le pixel de tracking)
                        email_log = EmailLog(
                            contact_id=contact.id,
                            campaign_id=campaign.id,
                            email_to=contact.email,
                            subject=campaign.subject,
                            status='pending',
                            sent_at=datetime.utcnow()
                        )
                        db.session.add(email_log)
                        db.session.flush()  # Obtenir l'ID sans commit

                        # Personnaliser le contenu
                        html = campaign.html_content.replace(
                            '{{first_name}}',
                            contact.first_name or 'ami spirituel'
                        )
                        html = html.replace('{{email}}', contact.email)

                        # Ajouter le footer automatique avec lien de désinscription (RGPD)
                        from app.services.email_service import add_footer_to_html
                        html = add_footer_to_html(html, contact.email)

                        # Ajouter le pixel de tracking invisible à la fin du HTML
                        tracking_pixel = f'<img src="https://saccra.fr/api/track/email/open/{email_log.id}" width="1" height="1" style="display:none;" alt="" />'

                        # Insérer le pixel juste avant la fermeture du body (si existe)
                        if '</body>' in html:
                            html = html.replace('</body>', tracking_pixel + '</body>')
                        else:
                            # Sinon, ajouter à la fin
                            html += tracking_pixel

                        # Créer le message
                        message = MIMEMultipart('alternative')
                        message['Subject'] = campaign.subject
                        message['From'] = sender_email
                        message['To'] = contact.email

                        part = MIMEText(html, 'html', 'utf-8')
                        message.attach(part)

                        # Envoyer
                        _send_email(message, smtp_server, smtp_port, smtp_user, smtp_password)

                        # Mettre à jour le statut après envoi réussi
                        email_log.status = 'sent'

                        batch_sent += 1
                        total_sent += 1
                        last_contact_id = contact.id

                    except Exception as e:
                        print(f"   ❌ Erreur pour {contact.email}: {str(e)}")
                        batch_failed += 1
                        total_failed += 1

                # Commit du batch
                db.session.commit()

                # Mettre à jour les stats de la campagne en temps réel
                campaign.total_sent = EmailLog.query.filter_by(campaign_id=campaign_id, status='sent').count()
                campaign.total_opened = EmailLog.query.filter_by(campaign_id=campaign_id).filter(EmailLog.opened_at.isnot(None)).count()
                db.session.commit()

                # Sauvegarder la progression
                save_progress(campaign_id, total_sent, total_failed, last_contact_id)

                # Afficher les stats du batch
                print(f"   ✅ Envoyés: {batch_sent}")
                if batch_failed > 0:
                    print(f"   ❌ Échecs: {batch_failed}")
                print(f"   📊 Total: {total_sent}/{total_to_send} ({total_sent*100//total_to_send}%)")

                # Attendre avant le prochain batch (sauf pour le dernier)
                if i + batch_size < len(contacts):
                    print(f"   ⏳ Attente de {delay}s avant le prochain batch...")
                    time.sleep(delay)

            # Succès complet
            clear_progress()

            print("\n" + "=" * 70)
            print("✅ ENVOI TERMINÉ AVEC SUCCÈS!")
            print("=" * 70)
            print(f"\n📊 Résumé:")
            print(f"   Total envoyés: {total_sent:,}")
            print(f"   Échecs: {total_failed:,}")
            print(f"   Taux de succès: {total_sent*100//(total_sent+total_failed) if total_sent+total_failed > 0 else 0}%")
            print(f"\n⏱️  Temps écoulé: {(batch_number * delay) / 60:.1f} minutes")

        except KeyboardInterrupt:
            print("\n\n⚠️  INTERRUPTION DÉTECTÉE (Ctrl+C)")
            print("\n📊 Progression sauvegardée:")
            print(f"   Envoyés: {total_sent:,}")
            print(f"   Échecs: {total_failed:,}")
            print(f"   Dernier contact ID: {last_contact_id}")
            print("\n💡 Pour reprendre l'envoi:")
            print(f"   python3 send_campaign_batch.py {campaign_id} --resume")
            sys.exit(0)

def main():
    parser = argparse.ArgumentParser(
        description='Envoi de campagne email par batch',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )

    parser.add_argument('campaign_id', type=int, help='ID de la campagne')
    parser.add_argument('--batch-size', type=int, default=100,
                       help='Nombre d\'emails par batch (défaut: 100)')
    parser.add_argument('--delay', type=int, default=60,
                       help='Délai entre chaque batch en secondes (défaut: 60)')
    parser.add_argument('--max-total', type=int,
                       help='Nombre maximum d\'emails à envoyer')
    parser.add_argument('--resume', action='store_true',
                       help='Reprendre un envoi interrompu')
    parser.add_argument('--no-confirm', action='store_true',
                       help='Ne pas demander de confirmation (pour lancement automatique)')

    args = parser.parse_args()

    send_campaign_batch(
        args.campaign_id,
        batch_size=args.batch_size,
        delay=args.delay,
        max_total=args.max_total,
        resume=args.resume,
        no_confirm=args.no_confirm
    )

if __name__ == '__main__':
    main()

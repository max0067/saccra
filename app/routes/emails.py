"""
Routes pour la gestion des emails marketing
"""
from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash
from flask_login import login_required, current_user
from functools import wraps
from datetime import datetime
from app.models import db, EmailContact, EmailCampaign, EmailLog, User
from werkzeug.utils import secure_filename
import csv
import io

bp = Blueprint('emails', __name__, url_prefix='/admin/emails')


def admin_required(f):
    """Décorateur pour restreindre l'accès aux administrateurs"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            flash('Tu dois être connecté pour accéder à cette page', 'error')
            return redirect(url_for('auth.login'))
        if not current_user.is_admin:
            flash('Accès réservé aux administrateurs', 'error')
            return redirect(url_for('main.index'))
        return f(*args, **kwargs)
    return decorated_function


@bp.route('/')
@login_required
@admin_required
def index():
    """Dashboard email marketing"""

    total_contacts = EmailContact.query.count()
    subscribed_contacts = EmailContact.query.filter_by(is_subscribed=True).count()
    bounced_contacts = EmailContact.query.filter_by(is_bounced=True).count()

    total_campaigns = EmailCampaign.query.count()
    active_campaigns = EmailCampaign.query.filter_by(is_active=True).count()

    total_sent = EmailLog.query.count()
    total_opened = EmailLog.query.filter(EmailLog.opened_at.isnot(None)).count()

    stats = {
        'total_contacts': total_contacts,
        'subscribed_contacts': subscribed_contacts,
        'bounced_contacts': bounced_contacts,
        'total_campaigns': total_campaigns,
        'active_campaigns': active_campaigns,
        'total_sent': total_sent,
        'total_opened': total_opened,
        'open_rate': round((total_opened / total_sent * 100) if total_sent > 0 else 0, 1)
    }

    # Dernières campagnes
    recent_campaigns = EmailCampaign.query.order_by(EmailCampaign.created_at.desc()).limit(5).all()

    return render_template('admin/emails/dashboard.html', stats=stats, recent_campaigns=recent_campaigns)


@bp.route('/contacts')
@login_required
@admin_required
def contacts():
    """Liste des contacts"""

    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '')
    filter_status = request.args.get('filter', 'all')

    query = EmailContact.query

    # Filtres
    if filter_status == 'subscribed':
        query = query.filter_by(is_subscribed=True)
    elif filter_status == 'unsubscribed':
        query = query.filter_by(is_subscribed=False)
    elif filter_status == 'bounced':
        query = query.filter_by(is_bounced=True)

    # Recherche
    if search:
        query = query.filter(
            (EmailContact.email.contains(search)) |
            (EmailContact.first_name.contains(search)) |
            (EmailContact.last_name.contains(search))
        )

    contacts_paginated = query.order_by(EmailContact.subscribed_at.desc()).paginate(
        page=page, per_page=50, error_out=False
    )

    return render_template('admin/emails/contacts.html',
                          contacts=contacts_paginated,
                          search=search,
                          filter_status=filter_status)


@bp.route('/contacts/import', methods=['GET', 'POST'])
@login_required
@admin_required
def import_contacts():
    """Import de contacts depuis un CSV"""

    if request.method == 'POST':
        # Vérifier qu'un fichier a été envoyé
        if 'file' not in request.files:
            flash('Aucun fichier envoyé', 'error')
            return redirect(request.url)

        file = request.files['file']

        if file.filename == '':
            flash('Aucun fichier sélectionné', 'error')
            return redirect(request.url)

        if not (file.filename.endswith('.csv') or file.filename.endswith('.txt') or file.filename.endswith('.tsv')):
            flash('Le fichier doit être au format CSV, TSV ou TXT', 'error')
            return redirect(request.url)

        try:
            # Lire le fichier CSV/TSV (utf-8-sig supprime automatiquement le BOM)
            content = file.stream.read().decode('utf-8-sig')
            stream = io.StringIO(content)

            # Auto-détecter le délimiteur (virgule, tabulation, point-virgule)
            sample = stream.read(1024)
            stream.seek(0)

            try:
                dialect = csv.Sniffer().sniff(sample, delimiters=',\t;')
                csv_reader = csv.DictReader(stream, dialect=dialect)
            except:
                # Si la détection échoue, utiliser le comportement par défaut (virgule)
                # Cela fonctionne pour les fichiers avec une seule colonne
                stream.seek(0)
                csv_reader = csv.DictReader(stream)

            # Wrapper pour nettoyer les noms de colonnes (enlever espaces, BOM résiduel)
            class CleanDictReader:
                def __init__(self, reader):
                    self.reader = reader
                    self.fieldnames = [name.strip() for name in reader.fieldnames] if reader.fieldnames else []

                def __iter__(self):
                    return self

                def __next__(self):
                    row = next(self.reader)
                    # Créer un nouveau dict avec les clés nettoyées
                    cleaned_row = {}
                    for key, value in row.items():
                        clean_key = key.strip() if key else key
                        cleaned_row[clean_key] = value
                    return cleaned_row

            csv_reader = CleanDictReader(csv_reader)

            imported = 0
            skipped_empty = 0
            skipped_duplicates = 0
            skipped_invalid = 0

            # Pour le debug: stocker les colonnes détectées
            columns_found = []

            # Traiter par batch de 1000 pour ne pas surcharger la DB
            batch = []
            batch_size = 1000

            row_count = 0

            for row in csv_reader:
                row_count += 1

                # Première ligne: capturer les noms de colonnes pour debug
                if row_count == 1:
                    columns_found = list(row.keys())

                # Chercher la colonne email (flexible: email, Email, EMAIL, e-mail, etc.)
                email = None
                for key in row.keys():
                    key_clean = key.strip().lower().replace('-', '').replace('_', '')
                    if key_clean in ['email', 'mail', 'email', 'courriel']:
                        email = row[key].strip().lower()
                        break

                # Si pas trouvé, essayer directement
                if not email:
                    email = row.get('email', '').strip().lower()

                # Email vide ou invalide
                if not email:
                    skipped_empty += 1
                    continue

                # Validation basique email
                if '@' not in email or '.' not in email:
                    skipped_invalid += 1
                    continue

                # Vérifier si le contact existe déjà
                existing = EmailContact.query.filter_by(email=email).first()

                if existing:
                    skipped_duplicates += 1
                    continue

                # Créer le contact
                contact = EmailContact(
                    email=email,
                    first_name=row.get('first_name', row.get('prenom', row.get('prénom', ''))).strip() or None,
                    last_name=row.get('last_name', row.get('nom', '')).strip() or None,
                    source='import_csv',
                    is_subscribed=True,
                    subscribed_at=datetime.utcnow()
                )

                batch.append(contact)

                # Insérer par batch
                if len(batch) >= batch_size:
                    db.session.bulk_save_objects(batch)
                    db.session.commit()
                    imported += len(batch)
                    batch = []

            # Insérer le reste
            if batch:
                db.session.bulk_save_objects(batch)
                db.session.commit()
                imported += len(batch)

            # Message détaillé
            total_skipped = skipped_empty + skipped_duplicates + skipped_invalid
            message = f'✅ Import terminé ! {imported} contacts importés'

            if total_skipped > 0:
                details = []
                if skipped_duplicates > 0:
                    details.append(f'{skipped_duplicates} doublons')
                if skipped_empty > 0:
                    details.append(f'{skipped_empty} vides')
                if skipped_invalid > 0:
                    details.append(f'{skipped_invalid} invalides')
                message += f', {total_skipped} ignorés ({", ".join(details)})'

            if columns_found:
                message += f'<br>📋 Colonnes détectées: {", ".join(columns_found[:5])}'

            flash(message, 'success' if imported > 0 else 'warning')
            return redirect(url_for('emails.contacts'))

        except Exception as e:
            flash(f'Erreur lors de l\'import : {str(e)}', 'error')
            return redirect(request.url)

    return render_template('admin/emails/import.html')


@bp.route('/contacts/new', methods=['GET', 'POST'])
@login_required
@admin_required
def contact_new():
    """Ajouter un contact manuellement"""

    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        first_name = request.form.get('first_name', '').strip()
        last_name = request.form.get('last_name', '').strip()

        # Validation
        if not email:
            flash('L\'email est obligatoire', 'error')
            return redirect(request.url)

        if '@' not in email or '.' not in email:
            flash('L\'email n\'est pas valide', 'error')
            return redirect(request.url)

        # Vérifier si le contact existe déjà
        existing = EmailContact.query.filter_by(email=email).first()
        if existing:
            flash(f'❌ Ce contact existe déjà : {email}', 'error')
            return redirect(request.url)

        # Créer le contact
        contact = EmailContact(
            email=email,
            first_name=first_name or None,
            last_name=last_name or None,
            source='manual',
            is_subscribed=True,
            subscribed_at=datetime.utcnow()
        )

        db.session.add(contact)
        db.session.commit()

        flash(f'✅ Contact ajouté avec succès : {email}', 'success')
        return redirect(url_for('emails.contacts'))

    return render_template('admin/emails/contact_form.html')


@bp.route('/campaigns')
@login_required
@admin_required
def campaigns():
    """Liste des campagnes"""

    campaigns_list = EmailCampaign.query.order_by(EmailCampaign.created_at.desc()).all()

    return render_template('admin/emails/campaigns.html', campaigns=campaigns_list)


@bp.route('/campaigns/new', methods=['GET', 'POST'])
@login_required
@admin_required
def campaign_new():
    """Créer une nouvelle campagne"""

    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        campaign_type = request.form.get('campaign_type', '').strip()
        subject = request.form.get('subject', '').strip()
        html_content = request.form.get('html_content', '').strip()
        is_active = request.form.get('is_active') == 'on'

        if not name or not subject or not html_content:
            flash('Tous les champs sont obligatoires', 'error')
            return render_template('admin/emails/campaign_form.html', campaign=None)

        campaign = EmailCampaign(
            name=name,
            campaign_type=campaign_type,
            subject=subject,
            html_content=html_content,
            is_active=is_active
        )

        db.session.add(campaign)
        db.session.commit()

        flash('Campagne créée avec succès !', 'success')
        return redirect(url_for('emails.campaigns'))

    return render_template('admin/emails/campaign_form.html', campaign=None)


@bp.route('/campaigns/<int:campaign_id>/send', methods=['POST'])
@login_required
@admin_required
def campaign_send(campaign_id):
    """Envoyer une campagne à tous les contacts abonnés"""

    campaign = EmailCampaign.query.get_or_404(campaign_id)

    # Récupérer tous les contacts abonnés
    contacts = EmailContact.query.filter_by(is_subscribed=True, is_bounced=False).all()

    if not contacts:
        return jsonify({'success': False, 'error': 'Aucun contact abonné'}), 400

    # Envoyer les emails en arrière-plan (pour ne pas bloquer l'interface)
    # Note: Pour 70K emails, utiliser Celery ou un worker serait mieux
    # Pour l'instant, on fait simple avec un traitement direct

    from app.services.email_service import _send_email
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart
    import os

    sent = 0
    failed = 0

    smtp_server = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
    smtp_port = int(os.environ.get('MAIL_PORT', '587'))
    smtp_user = os.environ.get('MAIL_USERNAME', '')
    smtp_password = os.environ.get('MAIL_PASSWORD', '')
    sender_email = os.environ.get('MAIL_DEFAULT_SENDER', 'noreply@saccra.fr')

    if not smtp_user or not smtp_password:
        return jsonify({'success': False, 'error': 'SMTP non configuré'}), 500

    # Limiter à 100 emails par envoi pour ne pas surcharger
    max_emails = min(len(contacts), 100)

    for contact in contacts[:max_emails]:
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
            html = campaign.html_content.replace('{{first_name}}', contact.first_name or 'ami spirituel')
            html = html.replace('{{email}}', contact.email)

            # Ajouter le pixel de tracking invisible
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

            sent += 1

        except Exception as e:
            print(f'Erreur envoi à {contact.email}: {e}')
            failed += 1

    # Mettre à jour les stats de la campagne
    campaign.total_sent += sent
    db.session.commit()

    return jsonify({
        'success': True,
        'sent': sent,
        'failed': failed,
        'message': f'{sent} emails envoyés, {failed} échecs'
    })


@bp.route('/campaigns/<int:campaign_id>/delete', methods=['POST'])
@login_required
@admin_required
def campaign_delete(campaign_id):
    """Supprimer une campagne"""

    campaign = EmailCampaign.query.get_or_404(campaign_id)
    name = campaign.name

    db.session.delete(campaign)
    db.session.commit()

    return jsonify({
        'success': True,
        'message': f'Campagne "{name}" supprimée'
    })

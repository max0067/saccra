"""
Routes pour le tracking des visiteurs (analytics) et emails
"""
from flask import Blueprint, request, jsonify, send_file
from flask_login import current_user
from app.models import db, Visit, EmailLog, EmailCampaign
from datetime import datetime
import io
import base64

bp = Blueprint('analytics', __name__)


@bp.route('/track', methods=['POST'])
def track_visit():
    """Enregistre une visite de page (AJAX)"""

    try:
        data = request.get_json()
        page_url = data.get('page_url', request.referrer or '/')

        # Récupérer les informations du visiteur
        ip_address = request.headers.get('X-Forwarded-For', request.remote_addr)
        if ip_address:
            # Prendre seulement la première IP si derrière un proxy
            ip_address = ip_address.split(',')[0].strip()

        user_agent = request.headers.get('User-Agent', '')

        # Créer un hash anonyme du visiteur
        visitor_hash = Visit.create_visitor_hash(ip_address, user_agent)

        # Créer la visite
        visit = Visit(
            visitor_hash=visitor_hash,
            page_url=page_url,
            user_agent=user_agent,
            user_id=current_user.id if current_user.is_authenticated else None,
            visited_at=datetime.utcnow()
        )

        db.session.add(visit)
        db.session.commit()

        return jsonify({'success': True})

    except Exception as e:
        # Ne pas bloquer le site si le tracking échoue
        print(f'Erreur tracking: {str(e)}')
        return jsonify({'success': False}), 200  # Retourner 200 quand même


@bp.route('/track/email/open/<int:log_id>')
def track_email_open(log_id):
    """
    Tracking d'ouverture d'email via pixel invisible 1x1

    Cette route est appelée quand un email est ouvert (le pixel est chargé)
    Elle renvoie un GIF transparent 1x1 pixel
    """
    try:
        # Trouver le log d'email
        email_log = EmailLog.query.get(log_id)

        if email_log and not email_log.opened_at:
            # Première ouverture uniquement
            email_log.opened_at = datetime.utcnow()

            # Incrémenter le compteur de la campagne
            if email_log.campaign_id:
                campaign = EmailCampaign.query.get(email_log.campaign_id)
                if campaign:
                    campaign.total_opened += 1

            db.session.commit()

    except Exception as e:
        # Ne pas planter si erreur, juste logger
        print(f'Erreur tracking email open: {str(e)}')

    # Retourner un pixel transparent 1x1 (GIF)
    # GIF transparent 1x1 en base64
    pixel_data = base64.b64decode(
        'R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7'
    )

    return send_file(
        io.BytesIO(pixel_data),
        mimetype='image/gif',
        as_attachment=False
    )

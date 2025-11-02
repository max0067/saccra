"""
Routes pour le tracking des visiteurs (analytics)
"""
from flask import Blueprint, request, jsonify
from flask_login import current_user
from app.models import db, Visit
from datetime import datetime

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

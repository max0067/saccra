"""
Routes administrateur pour SACRA
Gestion des utilisateurs, codes promo, et statistiques
"""
from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash
from flask_login import login_required, current_user
from functools import wraps
from datetime import datetime, timedelta
from sqlalchemy import func
from app.models import db, User, Interpretation, PromoCode, SpiritualProfile

bp = Blueprint('admin', __name__)


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


@bp.route('/dashboard')
@login_required
@admin_required
def dashboard():
    """Dashboard administrateur avec statistiques globales"""

    # Statistiques générales
    total_users = User.query.count()
    premium_users = User.query.filter_by(is_premium=True).count()
    total_interpretations = Interpretation.query.count()
    active_promo_codes = PromoCode.query.filter_by(is_active=True).count()

    # Nouveaux utilisateurs cette semaine
    week_ago = datetime.utcnow() - timedelta(days=7)
    new_users_week = User.query.filter(User.created_at >= week_ago).count()

    # Interprétations par type
    dream_count = Interpretation.query.filter_by(type='dream').count()
    sign_count = Interpretation.query.filter_by(type='sign').count()
    tarot_count = Interpretation.query.filter_by(type='tarot').count()

    # Derniers utilisateurs
    recent_users = User.query.order_by(User.created_at.desc()).limit(10).all()

    stats = {
        'total_users': total_users,
        'premium_users': premium_users,
        'free_users': total_users - premium_users,
        'total_interpretations': total_interpretations,
        'active_promo_codes': active_promo_codes,
        'new_users_week': new_users_week,
        'dream_count': dream_count,
        'sign_count': sign_count,
        'tarot_count': tarot_count,
    }

    return render_template('admin/dashboard.html', stats=stats, recent_users=recent_users)


@bp.route('/users')
@login_required
@admin_required
def users():
    """Liste de tous les utilisateurs avec filtres"""

    page = request.args.get('page', 1, type=int)
    filter_type = request.args.get('filter', 'all')
    search = request.args.get('search', '')

    query = User.query

    # Filtres
    if filter_type == 'premium':
        query = query.filter_by(is_premium=True)
    elif filter_type == 'free':
        query = query.filter_by(is_premium=False)
    elif filter_type == 'admin':
        query = query.filter_by(is_admin=True)

    # Recherche
    if search:
        query = query.filter(
            (User.email.contains(search)) |
            (User.first_name.contains(search))
        )

    # Pagination
    users_paginated = query.order_by(User.created_at.desc()).paginate(
        page=page, per_page=20, error_out=False
    )

    return render_template('admin/users.html', users=users_paginated, filter_type=filter_type, search=search)


@bp.route('/users/<int:user_id>/add-credits', methods=['POST'])
@login_required
@admin_required
def add_credits(user_id):
    """Ajouter des crédits à un utilisateur"""

    user = User.query.get_or_404(user_id)
    data = request.get_json()
    credits = data.get('credits', 0)

    if credits <= 0 or credits > 1000:
        return jsonify({'success': False, 'error': 'Nombre de crédits invalide'}), 400

    user.credits += credits
    db.session.commit()

    return jsonify({
        'success': True,
        'message': '{} crédits ajoutés à {}'.format(credits, user.email),
        'new_credits': user.credits
    })


@bp.route('/users/<int:user_id>/toggle-premium', methods=['POST'])
@login_required
@admin_required
def toggle_premium(user_id):
    """Activer/désactiver le premium manuellement"""

    user = User.query.get_or_404(user_id)
    data = request.get_json()
    days = data.get('days', 30)

    if not user.is_premium or not user.premium_until or user.premium_until < datetime.utcnow():
        # Activer premium
        user.is_premium = True
        user.premium_until = datetime.utcnow() + timedelta(days=days)
        message = 'Premium activé pour {} jours'.format(days)
    else:
        # Désactiver premium
        user.is_premium = False
        user.premium_until = None
        message = 'Premium désactivé'

    db.session.commit()

    return jsonify({
        'success': True,
        'message': message,
        'is_premium': user.is_premium,
        'premium_until': user.premium_until.isoformat() if user.premium_until else None
    })


@bp.route('/users/<int:user_id>/toggle-admin', methods=['POST'])
@login_required
@admin_required
def toggle_admin(user_id):
    """Promouvoir/rétrograder un utilisateur admin"""

    user = User.query.get_or_404(user_id)

    # Ne pas se désadminer soi-même
    if user.id == current_user.id:
        return jsonify({'success': False, 'error': 'Tu ne peux pas modifier ton propre statut admin'}), 400

    user.is_admin = not user.is_admin
    db.session.commit()

    return jsonify({
        'success': True,
        'message': 'Admin {} pour {}'.format('activé' if user.is_admin else 'désactivé', user.email),
        'is_admin': user.is_admin
    })


@bp.route('/users/<int:user_id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_user(user_id):
    """Supprimer un utilisateur"""

    user = User.query.get_or_404(user_id)

    # Ne pas se supprimer soi-même
    if user.id == current_user.id:
        return jsonify({'success': False, 'error': 'Tu ne peux pas supprimer ton propre compte'}), 400

    email = user.email
    db.session.delete(user)
    db.session.commit()

    return jsonify({
        'success': True,
        'message': 'Utilisateur {} supprimé'.format(email)
    })


@bp.route('/promo-codes')
@login_required
@admin_required
def promo_codes():
    """Liste des codes promo"""

    codes = PromoCode.query.order_by(PromoCode.created_at.desc()).all()
    return render_template('admin/promo_codes.html', codes=codes)


@bp.route('/promo-codes/create', methods=['POST'])
@login_required
@admin_required
def create_promo_code():
    """Créer un nouveau code promo"""

    data = request.get_json()

    code = data.get('code', '').strip().upper()
    reward_type = data.get('reward_type')
    reward_value = data.get('reward_value', 0)
    max_uses = data.get('max_uses')
    expires_days = data.get('expires_days')
    description = data.get('description', '')

    # Validation
    if not code or len(code) < 3:
        return jsonify({'success': False, 'error': 'Code trop court (min 3 caractères)'}), 400

    if PromoCode.query.filter_by(code=code).first():
        return jsonify({'success': False, 'error': 'Ce code existe déjà'}), 400

    if reward_type not in ['credits', 'premium_days']:
        return jsonify({'success': False, 'error': 'Type de récompense invalide'}), 400

    if reward_value <= 0:
        return jsonify({'success': False, 'error': 'Valeur de récompense invalide'}), 400

    # Créer le code promo
    promo = PromoCode(
        code=code,
        reward_type=reward_type,
        reward_value=reward_value,
        max_uses=max_uses if max_uses and max_uses > 0 else None,
        expires_at=datetime.utcnow() + timedelta(days=expires_days) if expires_days else None,
        description=description,
        created_by=current_user.id
    )

    db.session.add(promo)
    db.session.commit()

    return jsonify({
        'success': True,
        'message': 'Code promo {} créé'.format(code),
        'code': {
            'id': promo.id,
            'code': promo.code,
            'reward_type': promo.reward_type,
            'reward_value': promo.reward_value
        }
    })


@bp.route('/promo-codes/<int:code_id>/toggle', methods=['POST'])
@login_required
@admin_required
def toggle_promo_code(code_id):
    """Activer/désactiver un code promo"""

    promo = PromoCode.query.get_or_404(code_id)
    promo.is_active = not promo.is_active
    db.session.commit()

    return jsonify({
        'success': True,
        'message': 'Code {} {}'.format(promo.code, 'activé' if promo.is_active else 'désactivé'),
        'is_active': promo.is_active
    })


@bp.route('/promo-codes/<int:code_id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_promo_code(code_id):
    """Supprimer un code promo"""

    promo = PromoCode.query.get_or_404(code_id)
    code = promo.code
    db.session.delete(promo)
    db.session.commit()

    return jsonify({
        'success': True,
        'message': 'Code promo {} supprimé'.format(code)
    })

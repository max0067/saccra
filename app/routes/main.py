"""
Routes principales : accueil, dashboard
"""
from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user
from app.models import Interpretation

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    """Page d'accueil"""
    return render_template('index.html')

@bp.route('/dashboard')
@login_required
def dashboard():
    """Dashboard utilisateur"""
    # Récupérer les dernières interprétations
    recent_interpretations = current_user.interpretations.order_by(
        Interpretation.created_at.desc()
    ).limit(5).all()

    # Dernière interprétation complète
    last_interpretation = current_user.interpretations.order_by(
        Interpretation.created_at.desc()
    ).first()

    # Stats
    remaining = current_user.get_remaining_free_interpretations()

    # Statistiques complètes
    total_interpretations = current_user.interpretations.count()
    dream_count = current_user.interpretations.filter_by(type='dream').count()
    sign_count = current_user.interpretations.filter_by(type='sign').count()
    tarot_count = current_user.interpretations.filter_by(type='tarot').count()

    return render_template(
        'dashboard.html',
        recent_interpretations=recent_interpretations,
        last_interpretation=last_interpretation,
        remaining_interpretations=remaining,
        total_interpretations=total_interpretations,
        dream_count=dream_count,
        sign_count=sign_count,
        tarot_count=tarot_count
    )

@bp.route('/about')
def about():
    """À propos"""
    return render_template('about.html')

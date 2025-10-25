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

    # Stats
    remaining = current_user.get_remaining_free_interpretations()

    return render_template(
        'dashboard.html',
        recent_interpretations=recent_interpretations,
        remaining_interpretations=remaining
    )

@bp.route('/about')
def about():
    """À propos"""
    return render_template('about.html')

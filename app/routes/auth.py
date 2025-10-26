"""
Routes d'authentification : login, register, logout
"""
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app.models import db, User
from app.services.email_service import send_welcome_email
from datetime import datetime

bp = Blueprint('auth', __name__)

@bp.route('/login', methods=['GET', 'POST'])
def login():
    """Page de connexion"""
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))

    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')

        user = User.query.filter_by(email=email).first()

        if user and user.check_password(password):
            # Mise à jour du last_login
            user.last_login = datetime.utcnow()
            db.session.commit()

            login_user(user, remember=True)
            flash('Bienvenue dans ton espace sacré 🌙', 'success')

            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.dashboard'))
        else:
            flash('Email ou mot de passe incorrect', 'error')

    return render_template('auth/login.html')

@bp.route('/register', methods=['GET', 'POST'])
def register():
    """Page d'inscription"""
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))

    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        first_name = request.form.get('first_name', '').strip()

        # Vérifier si l'email existe déjà
        if User.query.filter_by(email=email).first():
            flash('Cet email est déjà utilisé', 'error')
            return render_template('auth/register.html')

        # Créer le nouvel utilisateur
        user = User(email=email, first_name=first_name)
        user.set_password(password)

        db.session.add(user)
        db.session.commit()

        # Envoyer l'email de bienvenue (ne pas bloquer si ça échoue)
        try:
            send_welcome_email(email, first_name)
        except Exception as e:
            # Logger l'erreur mais continuer l'inscription
            print('Erreur envoi email bienvenue: {}'.format(str(e)))

        # Connecter l'utilisateur automatiquement
        login_user(user, remember=True)
        flash('Bienvenue dans la communauté SACRA ✨', 'success')

        # Rediriger vers le questionnaire de profil spirituel
        return redirect(url_for('interpretations.spiritual_profile'))

    return render_template('auth/register.html')

@bp.route('/logout')
@login_required
def logout():
    """Déconnexion"""
    logout_user()
    flash('À bientôt 🌙', 'info')
    return redirect(url_for('main.index'))

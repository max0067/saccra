"""
Routes d'authentification : login, register, logout
"""
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app.models import db, User
from app.services.email_service import send_welcome_email, send_password_reset_email
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


@bp.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    """Page 'Mot de passe oublié'"""
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))

    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()

        # Chercher l'utilisateur
        user = User.query.filter_by(email=email).first()

        # Toujours afficher le même message (sécurité)
        flash('Si cet email existe, tu recevras un lien de réinitialisation', 'info')

        if user:
            # Générer le token
            token = user.generate_reset_token()

            # Créer l'URL de réinitialisation
            reset_url = url_for('auth.reset_password', token=token, _external=True)

            # Envoyer l'email (ne pas bloquer si ça échoue)
            try:
                send_password_reset_email(user.email, reset_url)
            except Exception as e:
                print('Erreur envoi email reset: {}'.format(str(e)))

        return redirect(url_for('auth.login'))

    return render_template('auth/forgot_password.html')


@bp.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    """Page de réinitialisation avec token"""
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))

    # Vérifier le token
    user = User.verify_reset_token(token)

    if not user:
        flash('Ce lien de réinitialisation est invalide ou a expiré', 'error')
        return redirect(url_for('auth.forgot_password'))

    if request.method == 'POST':
        password = request.form.get('password', '')
        password_confirm = request.form.get('password_confirm', '')

        # Validation
        if not password or len(password) < 6:
            flash('Le mot de passe doit contenir au moins 6 caractères', 'error')
            return render_template('auth/reset_password.html', token=token)

        if password != password_confirm:
            flash('Les mots de passe ne correspondent pas', 'error')
            return render_template('auth/reset_password.html', token=token)

        # Changer le mot de passe
        user.set_password(password)
        db.session.commit()

        flash('Ton mot de passe a été changé avec succès ! 🎉', 'success')
        return redirect(url_for('auth.login'))

    return render_template('auth/reset_password.html', token=token)

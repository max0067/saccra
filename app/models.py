"""
Modèles de données pour SACRA
"""
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import json

db = SQLAlchemy()

class User(UserMixin, db.Model):
    """Utilisateur de SACRA"""
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)

    # Profil spirituel
    first_name = db.Column(db.String(100))
    birth_date = db.Column(db.Date)
    favorite_color = db.Column(db.String(50))
    element = db.Column(db.String(20))  # air, feu, eau, terre

    # Profil calculé
    soul_type = db.Column(db.String(100))  # ancienne, guérisseuse, créatrice...
    dominant_element = db.Column(db.String(20))
    vibratory_color = db.Column(db.String(50))

    # Abonnement
    is_premium = db.Column(db.Boolean, default=False)
    premium_until = db.Column(db.DateTime)
    stripe_customer_id = db.Column(db.String(100))
    stripe_subscription_id = db.Column(db.String(100))

    # Métadonnées
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)

    # Relations
    interpretations = db.relationship('Interpretation', backref='user', lazy='dynamic', cascade='all, delete-orphan')

    def set_password(self, password):
        """Hash le mot de passe"""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Vérifie le mot de passe"""
        return check_password_hash(self.password_hash, password)

    def get_monthly_interpretations_count(self):
        """Compte les interprétations du mois en cours"""
        start_of_month = datetime.utcnow().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        return self.interpretations.filter(Interpretation.created_at >= start_of_month).count()

    def can_interpret(self):
        """Vérifie si l'utilisateur peut faire une interprétation"""
        if self.is_premium and self.premium_until and self.premium_until > datetime.utcnow():
            return True
        return self.get_monthly_interpretations_count() < 3

    def get_remaining_free_interpretations(self):
        """Retourne le nombre d'interprétations gratuites restantes"""
        if self.is_premium:
            return -1  # Illimité
        count = self.get_monthly_interpretations_count()
        return max(0, 3 - count)


class Interpretation(db.Model):
    """Interprétation spirituelle (rêve, signe, tirage)"""
    __tablename__ = 'interpretations'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    # Type d'interprétation
    type = db.Column(db.String(20), nullable=False)  # dream, sign, tarot, energy

    # Contenu
    user_input = db.Column(db.Text, nullable=False)
    ai_response = db.Column(db.Text, nullable=False)

    # Métadonnées
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)

    def get_response_dict(self):
        """Parse la réponse JSON de l'IA"""
        try:
            return json.loads(self.ai_response)
        except:
            return {"symbolism": "", "spiritual_message": "", "personal_advice": ""}


class SpiritualProfile(db.Model):
    """Profil spirituel détaillé (optionnel, pour extension future)"""
    __tablename__ = 'spiritual_profiles'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True, nullable=False)

    # Questionnaire initial
    zodiac_sign = db.Column(db.String(20))
    life_path_number = db.Column(db.Integer)
    moon_sign = db.Column(db.String(20))

    # Préférences
    favorite_crystal = db.Column(db.String(50))
    meditation_frequency = db.Column(db.String(20))

    # Journal spirituel (texte libre)
    journal_entries = db.Column(db.Text)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

"""
Modèles de données pour SACRA
"""
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import URLSafeTimedSerializer
from datetime import datetime, timedelta
import json
import os

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

    # Admin et crédits
    is_admin = db.Column(db.Boolean, default=False)
    credits = db.Column(db.Integer, default=0)  # Crédits d'interprétation bonus

    # Métadonnées
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)

    # Relations
    interpretations = db.relationship('Interpretation', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    conversations = db.relationship('Conversation', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    meditation_listens = db.relationship('MeditationListen', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    journal_entries = db.relationship('JournalEntry', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    blog_posts = db.relationship('BlogPost', backref='author', lazy='dynamic', cascade='all, delete-orphan')

    def set_password(self, password):
        """Hash le mot de passe"""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Vérifie le mot de passe"""
        return check_password_hash(self.password_hash, password)

    def generate_reset_token(self, expires_sec=1800):
        """
        Génère un token de réinitialisation de mot de passe

        Args:
            expires_sec: int - Durée de validité en secondes (défaut 30 min)

        Returns:
            str: Token signé
        """
        secret_key = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production-sacra-2025')
        s = URLSafeTimedSerializer(secret_key)
        return s.dumps({'user_id': self.id}, salt='password-reset-salt')

    @staticmethod
    def verify_reset_token(token, expires_sec=1800):
        """
        Vérifie un token de réinitialisation et retourne l'utilisateur

        Args:
            token: str - Token à vérifier
            expires_sec: int - Durée de validité maximale en secondes

        Returns:
            User or None: L'utilisateur si le token est valide, None sinon
        """
        secret_key = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production-sacra-2025')
        s = URLSafeTimedSerializer(secret_key)
        try:
            data = s.loads(token, salt='password-reset-salt', max_age=expires_sec)
            user_id = data['user_id']
        except:
            return None
        return User.query.get(user_id)

    def get_monthly_interpretations_count(self):
        """Compte les interprétations du mois en cours"""
        start_of_month = datetime.utcnow().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        return self.interpretations.filter(Interpretation.created_at >= start_of_month).count()

    def can_interpret(self):
        """Vérifie si l'utilisateur peut faire une interprétation"""
        if self.is_premium and self.premium_until and self.premium_until > datetime.utcnow():
            return True
        # Vérifier les crédits bonus d'abord
        if self.credits > 0:
            return True
        return self.get_monthly_interpretations_count() < 3

    def get_remaining_free_interpretations(self):
        """Retourne le nombre d'interprétations gratuites restantes"""
        if self.is_premium:
            return -1  # Illimité
        count = self.get_monthly_interpretations_count()
        return max(0, 3 - count)

    def use_interpretation(self):
        """Consomme un crédit d'interprétation (si applicable)"""
        if self.is_premium:
            return  # Premium = illimité
        if self.credits > 0:
            self.credits -= 1
            db.session.commit()

    def get_daily_chat_messages_count(self):
        """Compte les messages du chat envoyés aujourd'hui"""
        from app.models import ChatMessage, Conversation
        start_of_day = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
        return ChatMessage.query.join(Conversation).filter(
            Conversation.user_id == self.id,
            ChatMessage.is_user == True,
            ChatMessage.created_at >= start_of_day
        ).count()

    def can_send_chat_message(self):
        """Vérifie si l'utilisateur peut envoyer un message au chatbot"""
        if self.is_premium and self.premium_until and self.premium_until > datetime.utcnow():
            return True
        return self.get_daily_chat_messages_count() < 5

    def get_remaining_chat_messages(self):
        """Retourne le nombre de messages chatbot restants"""
        if self.is_premium:
            return -1  # Illimité
        count = self.get_daily_chat_messages_count()
        return max(0, 5 - count)

    def get_monthly_meditations_count(self):
        """Compte les méditations écoutées ce mois"""
        from app.models import MeditationListen
        start_of_month = datetime.utcnow().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        return self.meditation_listens.filter(MeditationListen.listened_at >= start_of_month).count()

    def can_listen_meditation(self):
        """Vérifie si l'utilisateur peut écouter une méditation"""
        if self.is_premium and self.premium_until and self.premium_until > datetime.utcnow():
            return True
        count = self.get_monthly_meditations_count()
        return count < 3  # 3 méditations gratuites par mois

    def get_remaining_meditations(self):
        """Retourne le nombre de méditations restantes ce mois"""
        if self.is_premium and self.premium_until and self.premium_until > datetime.utcnow():
            return -1  # Illimité
        count = self.get_monthly_meditations_count()
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

    def get_user_input_dict(self):
        """Parse l'entrée utilisateur si c'est du JSON (pour tarot notamment)"""
        try:
            return json.loads(self.user_input)
        except:
            return None


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


class PromoCode(db.Model):
    """Code promo pour offrir des avantages"""
    __tablename__ = 'promo_codes'

    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(50), unique=True, nullable=False, index=True)

    # Type de récompense
    reward_type = db.Column(db.String(20), nullable=False)  # credits, premium_days, discount
    reward_value = db.Column(db.Integer, nullable=False)  # nombre de crédits, jours, ou % de réduction

    # Limites d'utilisation
    max_uses = db.Column(db.Integer)  # None = illimité
    current_uses = db.Column(db.Integer, default=0)
    expires_at = db.Column(db.DateTime)  # None = pas d'expiration

    # Statut
    is_active = db.Column(db.Boolean, default=True)

    # Métadonnées
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    description = db.Column(db.String(200))  # Note interne

    def is_valid(self):
        """Vérifie si le code promo est valide"""
        if not self.is_active:
            return False
        if self.expires_at and self.expires_at < datetime.utcnow():
            return False
        if self.max_uses and self.current_uses >= self.max_uses:
            return False
        return True

    def use_code(self, user):
        """Applique le code promo à un utilisateur"""
        if not self.is_valid():
            return False

        if self.reward_type == 'credits':
            user.credits += self.reward_value
        elif self.reward_type == 'premium_days':
            if user.premium_until and user.premium_until > datetime.utcnow():
                user.premium_until += timedelta(days=self.reward_value)
            else:
                user.premium_until = datetime.utcnow() + timedelta(days=self.reward_value)
            user.is_premium = True

        self.current_uses += 1
        db.session.commit()
        return True


class SiteContent(db.Model):
    """Contenu éditable du site (CMS simple)"""
    __tablename__ = 'site_contents'

    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(100), unique=True, nullable=False, index=True)
    category = db.Column(db.String(50), default='Général')
    value = db.Column(db.Text, nullable=False)
    description = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Conversation(db.Model):
    """Conversation avec le coach spirituel IA"""
    __tablename__ = 'conversations'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(200))  # Titre généré automatiquement depuis la 1ère question
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relations
    messages = db.relationship('ChatMessage', backref='conversation', lazy='dynamic', cascade='all, delete-orphan', order_by='ChatMessage.created_at')

    def get_message_count(self):
        """Compte le nombre de messages de l'utilisateur dans cette conversation"""
        return self.messages.filter_by(is_user=True).count()


class ChatMessage(db.Model):
    """Message individuel dans une conversation"""
    __tablename__ = 'chat_messages'

    id = db.Column(db.Integer, primary_key=True)
    conversation_id = db.Column(db.Integer, db.ForeignKey('conversations.id'), nullable=False)
    is_user = db.Column(db.Boolean, default=True)  # True = utilisateur, False = IA
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)


class Meditation(db.Model):
    """Méditation guidée audio"""
    __tablename__ = 'meditations'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    theme = db.Column(db.String(50), nullable=False, index=True)  # chakras, manifestation, guérison, sommeil
    duration_minutes = db.Column(db.Integer, nullable=False)  # Durée en minutes
    script = db.Column(db.Text, nullable=False)  # Le texte de la méditation

    # Audio (optionnel, pour cache)
    audio_file_path = db.Column(db.String(500))  # Chemin vers l'audio en cache

    # Métadonnées
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)  # Pour activer/désactiver

    # Relations
    listens = db.relationship('MeditationListen', backref='meditation', lazy='dynamic', cascade='all, delete-orphan')

    def __repr__(self):
        return '<Meditation {}>'.format(self.title)


class MeditationListen(db.Model):
    """Tracking des écoutes de méditations par utilisateur"""
    __tablename__ = 'meditation_listens'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    meditation_id = db.Column(db.Integer, db.ForeignKey('meditations.id'), nullable=False)
    listened_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)

    # Métriques d'écoute (optionnel, pour analytics)
    duration_listened = db.Column(db.Integer)  # Secondes écoutées
    completed = db.Column(db.Boolean, default=False)  # A écouté jusqu'au bout

    def __repr__(self):
        return '<MeditationListen user={} meditation={}>'.format(self.user_id, self.meditation_id)


class JournalEntry(db.Model):
    """Entrée de journal spirituel quotidien"""
    __tablename__ = 'journal_entries'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    date = db.Column(db.Date, nullable=False, index=True)  # Date de l'entrée
    content = db.Column(db.Text, nullable=False)  # Contenu du journal

    # Métriques spirituelles (échelle 1-10)
    mood = db.Column(db.Integer)  # Humeur (1=très bas, 10=excellent)
    energy_level = db.Column(db.Integer)  # Niveau d'énergie
    mental_clarity = db.Column(db.Integer)  # Clarté mentale

    # Analyse IA
    ai_analysis = db.Column(db.Text)  # Analyse générée par l'IA
    ai_analysis_generated_at = db.Column(db.DateTime)  # Quand l'analyse a été générée

    # Métadonnées
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return '<JournalEntry user={} date={}>'.format(self.user_id, self.date)


class BlogPost(db.Model):
    """Article de blog pour le référencement SEO"""
    __tablename__ = 'blog_posts'

    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)

    # Contenu
    title = db.Column(db.String(200), nullable=False)
    slug = db.Column(db.String(250), unique=True, nullable=False, index=True)  # URL SEO-friendly
    excerpt = db.Column(db.String(300))  # Résumé court pour la liste et meta description
    content = db.Column(db.Text, nullable=False)  # Contenu complet (HTML ou Markdown)
    image_url = db.Column(db.String(500))  # Image principale de l'article

    # SEO
    meta_title = db.Column(db.String(200))  # Si différent du title
    meta_description = db.Column(db.String(300))  # Pour les moteurs de recherche

    # Publication
    is_published = db.Column(db.Boolean, default=False, index=True)
    published_at = db.Column(db.DateTime, index=True)

    # Analytics
    views = db.Column(db.Integer, default=0)  # Compteur de vues

    # Métadonnées
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return '<BlogPost {}>'.format(self.title)

    @staticmethod
    def generate_slug(title):
        """Génère un slug SEO-friendly depuis un titre"""
        import re
        # Convertir en minuscules et remplacer les espaces/caractères spéciaux
        slug = title.lower()
        # Remplacer les caractères accentués
        replacements = {
            'à': 'a', 'â': 'a', 'ä': 'a', 'á': 'a',
            'é': 'e', 'è': 'e', 'ê': 'e', 'ë': 'e',
            'í': 'i', 'ì': 'i', 'î': 'i', 'ï': 'i',
            'ó': 'o', 'ò': 'o', 'ô': 'o', 'ö': 'o',
            'ú': 'u', 'ù': 'u', 'û': 'u', 'ü': 'u',
            'ç': 'c', 'ñ': 'n'
        }
        for old, new in replacements.items():
            slug = slug.replace(old, new)
        # Remplacer tout ce qui n'est pas alphanumérique par des tirets
        slug = re.sub(r'[^a-z0-9]+', '-', slug)
        # Enlever les tirets au début et à la fin
        slug = slug.strip('-')
        return slug

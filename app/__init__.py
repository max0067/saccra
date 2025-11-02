"""
Initialisation de l'application SACRA
"""
from flask import Flask
from flask_login import LoginManager
from config import Config
from app.models import db, User

login_manager = LoginManager()

def create_app(config_class=Config):
    """Factory pour créer l'application Flask"""
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialiser les extensions
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Connecte-toi pour accéder à cette page 🌙'

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Créer les tables
    with app.app_context():
        db.create_all()

    # Fonction helper pour les templates
    @app.context_processor
    def inject_site_content():
        """Injecte une fonction pour récupérer les contenus du site dans tous les templates"""
        from app.models import SiteContent
        from datetime import datetime

        def get_content(key, default=''):
            """Récupère un contenu par sa clé"""
            content = SiteContent.query.filter_by(key=key).first()
            return content.value if content else default

        return dict(get_content=get_content, now=datetime.utcnow)

    # Enregistrer les blueprints
    from app.routes.main import bp as main_bp
    from app.routes.auth import bp as auth_bp
    from app.routes.interpretations import bp as interpretations_bp
    from app.routes.premium import bp as premium_bp
    from app.routes.admin import bp as admin_bp
    from app.routes.chat import bp as chat_bp
    from app.routes.meditations import bp as meditations_bp
    from app.routes.journal import bp as journal_bp
    from app.routes.blog import bp as blog_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(interpretations_bp, url_prefix='/interpret')
    app.register_blueprint(premium_bp, url_prefix='/premium')
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(chat_bp)
    app.register_blueprint(meditations_bp)
    app.register_blueprint(journal_bp)
    app.register_blueprint(blog_bp)

    return app

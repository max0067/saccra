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

    # Enregistrer les blueprints
    from app.routes.main import bp as main_bp
    from app.routes.auth import bp as auth_bp
    from app.routes.interpretations import bp as interpretations_bp
    from app.routes.premium import bp as premium_bp
    from app.routes.admin import bp as admin_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(interpretations_bp, url_prefix='/interpret')
    app.register_blueprint(premium_bp, url_prefix='/premium')
    app.register_blueprint(admin_bp, url_prefix='/admin')

    return app

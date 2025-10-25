"""
Script pour initialiser la base de données et créer un compte admin
Usage: python init_admin.py
"""
from app import create_app
from app.models import db, User, PromoCode
from datetime import datetime, timedelta

def init_database():
    """Initialise la base de données et crée un compte admin"""
    app = create_app()

    with app.app_context():
        print("🌙 Initialisation de la base de données SACRA...")

        # Créer toutes les tables
        db.create_all()
        print("✅ Tables créées")

        # Vérifier s'il y a déjà un admin
        admin = User.query.filter_by(is_admin=True).first()

        if not admin:
            # Créer un compte admin par défaut
            admin = User(
                email='admin@sacra.fr',
                first_name='Admin',
                is_admin=True,
                is_premium=True,
                credits=100
            )
            admin.set_password('admin123')  # À CHANGER EN PRODUCTION !
            db.session.add(admin)
            db.session.commit()

            print("\n✨ Compte admin créé :")
            print("   Email    : admin@sacra.fr")
            print("   Password : admin123")
            print("   ⚠️  IMPORTANT : Change ce mot de passe en production !")

        else:
            print("\n✅ Un compte admin existe déjà")

        # Créer quelques codes promo d'exemple
        if PromoCode.query.count() == 0:
            promo1 = PromoCode(
                code='BIENVENUE',
                reward_type='credits',
                reward_value=5,
                max_uses=100,
                expires_at=datetime.utcnow() + timedelta(days=30),
                description='Code de bienvenue pour nouveaux utilisateurs',
                created_by=admin.id
            )

            promo2 = PromoCode(
                code='PREMIUM7J',
                reward_type='premium_days',
                reward_value=7,
                max_uses=50,
                expires_at=datetime.utcnow() + timedelta(days=30),
                description='7 jours de Premium gratuit',
                created_by=admin.id
            )

            db.session.add_all([promo1, promo2])
            db.session.commit()

            print("\n🎁 Codes promo créés :")
            print("   - BIENVENUE : 5 crédits")
            print("   - PREMIUM7J : 7 jours Premium")

        print("\n✅ Base de données initialisée avec succès !")
        print("\n🚀 Tu peux maintenant lancer l'application :")
        print("   python app.py")
        print("\n👑 Accède au dashboard admin sur :")
        print("   http://localhost:5000/admin/dashboard")


if __name__ == '__main__':
    init_database()

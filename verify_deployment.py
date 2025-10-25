#!/usr/bin/env python3
"""
Script de vérification pré-déploiement pour SACRA
Vérifie que tout est prêt avant de déployer sur o2switch
"""

import os
import sys
from pathlib import Path

# Couleurs pour le terminal
class Colors:
    GREEN = '\033[0;32m'
    YELLOW = '\033[1;33m'
    RED = '\033[0;31m'
    BLUE = '\033[0;34m'
    NC = '\033[0m'  # No Color

def success(msg):
    print(f"{Colors.GREEN}✓{Colors.NC} {msg}")

def warning(msg):
    print(f"{Colors.YELLOW}⚠{Colors.NC} {msg}")

def error(msg):
    print(f"{Colors.RED}✗{Colors.NC} {msg}")

def info(msg):
    print(f"{Colors.BLUE}ℹ{Colors.NC} {msg}")

def check_file_exists(filepath, required=True):
    """Vérifie qu'un fichier existe"""
    if os.path.exists(filepath):
        success(f"Fichier trouvé : {filepath}")
        return True
    else:
        if required:
            error(f"Fichier manquant : {filepath}")
        else:
            warning(f"Fichier optionnel manquant : {filepath}")
        return False

def check_env_file():
    """Vérifie le fichier .env"""
    print("\n📍 Vérification du fichier .env...")

    if not os.path.exists('.env'):
        error("Fichier .env manquant !")
        warning("Copie .env.example vers .env et complète les clés")
        return False

    # Lire le fichier .env
    with open('.env', 'r') as f:
        content = f.read()

    required_keys = [
        'SECRET_KEY',
        'OPENAI_API_KEY',
        'STRIPE_PUBLIC_KEY',
        'STRIPE_SECRET_KEY',
        'STRIPE_MONTHLY_PRICE_ID',
        'STRIPE_YEARLY_PRICE_ID'
    ]

    all_present = True
    for key in required_keys:
        if key in content and content.find(f'{key}=') != -1:
            # Vérifier que la valeur n'est pas vide
            line = [l for l in content.split('\n') if l.startswith(f'{key}=')]
            if line and len(line[0].split('=', 1)[1].strip()) > 0:
                success(f"Variable {key} présente")
            else:
                error(f"Variable {key} vide !")
                all_present = False
        else:
            error(f"Variable {key} manquante !")
            all_present = False

    return all_present

def check_python_files():
    """Vérifie les fichiers Python essentiels"""
    print("\n📍 Vérification des fichiers Python...")

    files = [
        'app.py',
        'passenger_wsgi.py',
        'config.py',
        'requirements.txt',
        'app/__init__.py',
        'app/models.py',
        'app/routes/main.py',
        'app/routes/auth.py',
        'app/routes/interpretations.py',
        'app/routes/premium.py',
        'app/services/ai_service.py'
    ]

    all_present = True
    for filepath in files:
        if not check_file_exists(filepath):
            all_present = False

    return all_present

def check_templates():
    """Vérifie les templates HTML"""
    print("\n📍 Vérification des templates...")

    templates = [
        'app/templates/base.html',
        'app/templates/index.html',
        'app/templates/dashboard.html',
        'app/templates/auth/login.html',
        'app/templates/auth/register.html',
        'app/templates/interpretations/dream.html',
        'app/templates/interpretations/sign.html',
        'app/templates/interpretations/tarot.html',
        'app/templates/premium/subscribe.html'
    ]

    all_present = True
    for template in templates:
        if not check_file_exists(template):
            all_present = False

    return all_present

def check_imports():
    """Vérifie que l'application peut être importée"""
    print("\n📍 Vérification des imports Python...")

    try:
        # Ajouter le répertoire actuel au path
        sys.path.insert(0, os.getcwd())

        from app import create_app
        success("Import de create_app réussi")

        app = create_app()
        success("Création de l'application Flask réussie")

        return True
    except Exception as e:
        error(f"Erreur lors de l'import : {str(e)}")
        return False

def check_requirements():
    """Vérifie que toutes les dépendances sont installées"""
    print("\n📍 Vérification des dépendances...")

    try:
        import flask
        success(f"Flask {flask.__version__} installé")
    except:
        error("Flask non installé !")
        return False

    try:
        import openai
        success("OpenAI installé")
    except:
        error("OpenAI non installé !")
        return False

    try:
        import stripe
        success("Stripe installé")
    except:
        error("Stripe non installé !")
        return False

    return True

def check_htaccess():
    """Vérifie le fichier .htaccess"""
    print("\n📍 Vérification du fichier .htaccess...")

    if not os.path.exists('.htaccess'):
        warning("Fichier .htaccess manquant (sera créé automatiquement)")
        return True

    with open('.htaccess', 'r') as f:
        content = f.read()

    if 'TON_USER' in content:
        error("Le fichier .htaccess contient toujours 'TON_USER' !")
        warning("Remplace /home/TON_USER/sacra.fr par le vrai chemin")
        return False

    if 'PassengerEnabled On' in content:
        success("Configuration Passenger présente")
    else:
        error("Configuration Passenger manquante dans .htaccess")
        return False

    return True

def main():
    """Fonction principale"""
    print("🌙 =====================================")
    print("   SACRA - Vérification pré-déploiement")
    print("=====================================")

    checks = {
        "Fichiers Python": check_python_files(),
        "Templates HTML": check_templates(),
        "Fichier .env": check_env_file(),
        "Dépendances": check_requirements(),
        "Imports Python": check_imports(),
        "Fichier .htaccess": check_htaccess()
    }

    # Résumé
    print("\n✨ =====================================")
    print("   Résumé de la vérification")
    print("=====================================\n")

    all_passed = True
    for check_name, passed in checks.items():
        if passed:
            success(f"{check_name} : OK")
        else:
            error(f"{check_name} : ÉCHEC")
            all_passed = False

    print("\n" + "="*40)
    if all_passed:
        success("🎉 Tout est prêt pour le déploiement !")
        print("\n📝 Prochaines étapes :")
        print("1. Uploader les fichiers sur o2switch (via FTP/SFTP)")
        print("2. Lancer setup_o2switch.sh sur le serveur")
        print("3. Configurer le domaine et SSL")
        print("4. Redémarrer Passenger : touch tmp/restart.txt")
        print("5. Tester sur https://sacra.fr\n")
        print("📖 Voir DEPLOY.md pour plus de détails")
        sys.exit(0)
    else:
        error("❌ Des problèmes doivent être résolus avant le déploiement")
        print("\n💡 Consulte les erreurs ci-dessus et corrige-les")
        sys.exit(1)

if __name__ == '__main__':
    main()

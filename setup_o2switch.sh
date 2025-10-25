#!/bin/bash

###############################################################################
# Script de setup automatique pour SACRA sur o2switch
# Usage: bash setup_o2switch.sh
###############################################################################

set -e  # Arrêter en cas d'erreur

echo "🌙 ====================================="
echo "   SACRA - Setup automatique o2switch"
echo "====================================="
echo ""

# Couleurs
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Fonctions utilitaires
success() {
    echo -e "${GREEN}✓${NC} $1"
}

warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

error() {
    echo -e "${RED}✗${NC} $1"
}

# 1. Vérifier Python
echo "📍 Étape 1/7 : Vérification de Python..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version)
    success "Python trouvé : $PYTHON_VERSION"
else
    error "Python 3 n'est pas installé !"
    exit 1
fi
echo ""

# 2. Créer l'environnement virtuel
echo "📍 Étape 2/7 : Création de l'environnement virtuel..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    success "Environnement virtuel créé"
else
    warning "Environnement virtuel existe déjà"
fi
echo ""

# 3. Activer et installer les dépendances
echo "📍 Étape 3/7 : Installation des dépendances..."
source venv/bin/activate
pip install --upgrade pip --quiet
pip install -r requirements.txt --quiet
success "Dépendances installées"
echo ""

# 4. Vérifier le fichier .env
echo "📍 Étape 4/7 : Vérification de la configuration..."
if [ ! -f ".env" ]; then
    if [ -f ".env.example" ]; then
        warning "Fichier .env manquant. Copie de .env.example..."
        cp .env.example .env
        warning "⚠️  IMPORTANT : Édite le fichier .env avec tes vraies clés API !"
    else
        error "Aucun fichier .env ou .env.example trouvé !"
        exit 1
    fi
else
    success "Fichier .env trouvé"
fi
echo ""

# 5. Initialiser la base de données
echo "📍 Étape 5/7 : Initialisation de la base de données..."
python3 -c "from app import create_app; app = create_app(); app.app_context().push()" 2>&1
if [ -f "instance/sacra.db" ]; then
    success "Base de données créée : instance/sacra.db"
else
    error "Échec de la création de la base de données"
    exit 1
fi
echo ""

# 6. Vérifier/créer les répertoires nécessaires
echo "📍 Étape 6/7 : Création des répertoires..."
mkdir -p tmp
mkdir -p logs
mkdir -p instance
success "Répertoires créés"
echo ""

# 7. Vérifier les permissions
echo "📍 Étape 7/7 : Configuration des permissions..."
chmod 755 passenger_wsgi.py
chmod 644 instance/sacra.db 2>/dev/null || true
chmod 755 instance
success "Permissions configurées"
echo ""

# Résumé
echo "✨ ====================================="
echo "   Setup terminé avec succès !"
echo "====================================="
echo ""
echo "📝 Prochaines étapes :"
echo ""
echo "1. 🔑 Éditer le fichier .env avec tes vraies clés API :"
echo "   - OPENAI_API_KEY"
echo "   - STRIPE_PUBLIC_KEY"
echo "   - STRIPE_SECRET_KEY"
echo "   - STRIPE_MONTHLY_PRICE_ID"
echo "   - STRIPE_YEARLY_PRICE_ID"
echo ""
echo "2. 🔧 Modifier le fichier .htaccess :"
echo "   - Remplacer /home/TON_USER/sacra.fr par le vrai chemin"
echo ""
echo "3. 🌐 Pointer le domaine sacra.fr vers ce répertoire"
echo ""
echo "4. 🔄 Redémarrer Passenger :"
echo "   touch tmp/restart.txt"
echo ""
echo "5. ✅ Tester le site sur https://sacra.fr"
echo ""
echo "📖 Pour plus de détails, consulte DEPLOY.md"
echo ""

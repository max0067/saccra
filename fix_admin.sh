#!/bin/bash
# Script de réparation pour la section admin de SACCRA

echo "🔧 Diagnostic et réparation de la section admin..."
echo ""

# 1. Vérifier qu'on est dans le bon dossier
if [ ! -f "passenger_wsgi.py" ]; then
    echo "❌ Erreur: pas dans le dossier saccra.fr"
    echo "Utilise: cd ~/saccra.fr"
    exit 1
fi

echo "✅ Dans le bon dossier: $(pwd)"
echo ""

# 2. Récupérer les derniers changements
echo "📥 Récupération des changements depuis GitHub..."
CURRENT_BRANCH=$(git branch --show-current)
git fetch origin $CURRENT_BRANCH
git pull origin $CURRENT_BRANCH

echo ""

# 3. Vérifier que le modèle SiteContent existe
echo "🔍 Vérification du modèle SiteContent..."
if grep -q "class SiteContent" app/models.py; then
    echo "✅ Modèle SiteContent trouvé dans models.py"
else
    echo "❌ Modèle SiteContent manquant!"
    exit 1
fi

echo ""

# 4. Activer l'environnement virtuel et mettre à jour la base de données
echo "💾 Mise à jour de la base de données..."
source venv/bin/activate

# Créer un script Python temporaire pour mettre à jour la DB
cat > /tmp/update_saccra_db.py << 'PYEOF'
import sys
sys.path.insert(0, '/home/wrbh3411/saccra.fr')

from app import create_app
from app.models import db

app = create_app()
with app.app_context():
    # Créer toutes les tables (inclut site_contents si elle n'existe pas)
    db.create_all()
    print("✅ Tables créées/vérifiées")

    # Vérifier que SiteContent est importable
    try:
        from app.models import SiteContent
        count = SiteContent.query.count()
        print("✅ Table site_contents OK ({} entrées)".format(count))
    except Exception as e:
        print("⚠️  Avertissement SiteContent: {}".format(e))
PYEOF

python3 /tmp/update_saccra_db.py
rm /tmp/update_saccra_db.py

echo ""

# 5. Redémarrer Passenger
echo "🔄 Redémarrage de Passenger..."
mkdir -p tmp
touch tmp/restart.txt

echo ""
echo "✅ Réparation terminée!"
echo ""
echo "🧪 Teste maintenant: https://saccra.fr/admin/dashboard"

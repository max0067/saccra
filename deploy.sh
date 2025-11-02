#!/bin/bash
# Script de déploiement automatique pour SACCRA sur o2switch
# Usage: ./deploy.sh

echo "🚀 Déploiement de SACCRA..."
echo "======================================"

# Aller dans le répertoire du projet
cd ~/saccra || exit 1

# Sauvegarder la branche actuelle
CURRENT_BRANCH=$(git branch --show-current)
echo "📍 Branche actuelle: $CURRENT_BRANCH"

# Pull les derniers changements
echo "📥 Récupération des derniers changements..."
git pull origin claude/sacra-mvp-development-011CUhLGumEoVuANcbz2osHe

# Vérifier si le pull a réussi
if [ $? -eq 0 ]; then
    echo "✅ Code mis à jour avec succès"
else
    echo "❌ Erreur lors du pull"
    exit 1
fi

# Redémarrer Passenger
echo "🔄 Redémarrage de Passenger..."
mkdir -p tmp
touch tmp/restart.txt

if [ $? -eq 0 ]; then
    echo "✅ Passenger redémarré"
else
    echo "❌ Erreur lors du redémarrage"
    exit 1
fi

echo "======================================"
echo "✨ Déploiement terminé à $(date '+%Y-%m-%d %H:%M:%S')"
echo "🌐 Site: https://saccra.fr"

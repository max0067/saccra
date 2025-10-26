#!/bin/bash
#
# Script de restauration pour SACRA
# Restaure une sauvegarde précédente
#

BACKUP_DIR="$HOME/saccra_backups"
APP_DIR="$HOME/saccra.fr"

echo "🔄 Script de Restauration SACRA"
echo "================================"
echo ""

# Vérifier si des backups existent
if [ ! -d "$BACKUP_DIR" ] || [ -z "$(ls -A $BACKUP_DIR/saccra_backup_*.tar.gz 2>/dev/null)" ]; then
    echo "❌ Aucun backup trouvé dans $BACKUP_DIR"
    exit 1
fi

# Lister les backups disponibles
echo "📋 Backups disponibles:"
echo ""
ls -1t "$BACKUP_DIR"/saccra_backup_*.tar.gz | nl
echo ""

# Demander quel backup restaurer
read -p "Quel backup veux-tu restaurer ? (numéro) : " BACKUP_NUM

# Récupérer le fichier correspondant
BACKUP_FILE=$(ls -1t "$BACKUP_DIR"/saccra_backup_*.tar.gz | sed -n "${BACKUP_NUM}p")

if [ -z "$BACKUP_FILE" ]; then
    echo "❌ Backup invalide"
    exit 1
fi

echo ""
echo "📦 Backup sélectionné: $(basename $BACKUP_FILE)"
echo ""
echo "⚠️  ATTENTION: Cette opération va ÉCRASER les fichiers actuels!"
echo ""
read -p "Es-tu SÛR de vouloir continuer ? (oui/non) : " CONFIRM

if [ "$CONFIRM" != "oui" ]; then
    echo "❌ Restauration annulée"
    exit 0
fi

echo ""
echo "🚀 Démarrage de la restauration..."

# Créer un dossier temporaire
TEMP_DIR="$BACKUP_DIR/restore_temp_$$"
mkdir -p "$TEMP_DIR"

# Extraire le backup
echo "📦 Extraction du backup..."
tar -xzf "$BACKUP_FILE" -C "$TEMP_DIR"
EXTRACT_DIR=$(ls -d "$TEMP_DIR"/temp_* | head -1)

# Restaurer la base de données
echo "💾 Restauration de la base de données..."
if [ -f "$EXTRACT_DIR/sacra.db" ]; then
    mkdir -p "$APP_DIR/instance"
    cp "$EXTRACT_DIR/sacra.db" "$APP_DIR/instance/sacra.db"
    echo "   ✅ Base de données restaurée dans instance/"
fi

if [ -f "$EXTRACT_DIR/sacra_root.db" ]; then
    cp "$EXTRACT_DIR/sacra_root.db" "$APP_DIR/sacra.db"
    echo "   ✅ Base de données restaurée à la racine"
fi

# Restaurer .env
echo "🔐 Restauration des variables d'environnement..."
if [ -f "$EXTRACT_DIR/.env" ]; then
    cp "$EXTRACT_DIR/.env" "$APP_DIR/.env"
    chmod 600 "$APP_DIR/.env"
    echo "   ✅ Fichier .env restauré"
fi

# Restaurer .htaccess
echo "⚙️  Restauration de la configuration Apache..."
if [ -f "$EXTRACT_DIR/.htaccess" ]; then
    cp "$EXTRACT_DIR/.htaccess" "$APP_DIR/.htaccess"
    echo "   ✅ Fichier .htaccess restauré"
fi

# Nettoyer
rm -rf "$TEMP_DIR"

echo ""
echo "✅ Restauration terminée avec succès!"
echo ""
echo "🔄 Pour appliquer les changements, redémarre l'application:"
echo "   cd $APP_DIR"
echo "   pkill -9 -u $(whoami) python"
echo "   sleep 3"
echo "   touch tmp/restart.txt"
echo ""
read -p "Veux-tu redémarrer l'application maintenant ? (oui/non) : " RESTART

if [ "$RESTART" = "oui" ]; then
    echo "🔄 Redémarrage de l'application..."
    cd "$APP_DIR"
    pkill -9 -u $(whoami) python
    sleep 3
    touch tmp/restart.txt
    echo "✅ Application redémarrée!"
fi

echo ""
echo "🎉 Restauration SACRA terminée!"

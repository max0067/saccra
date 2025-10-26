# 📦 Guide de Sauvegarde et Restauration SACRA

## 🎯 Vue d'ensemble

Ce guide explique comment sauvegarder et restaurer votre application SACRA.

**Fichiers inclus :**
- `backup.sh` - Script de sauvegarde automatique
- `restore.sh` - Script de restauration interactive
- Backups stockés dans `~/saccra_backups/`

---

## 💾 Créer une Sauvegarde

### Sauvegarde Manuelle

```bash
cd ~/saccra.fr
bash backup.sh
```

**Ce qui est sauvegardé :**
- ✅ Base de données SQLite (`sacra.db`)
- ✅ Variables d'environnement (`.env`)
- ✅ Configuration Apache (`.htaccess`)
- ✅ Informations du backup

**Résultat :**
Un fichier `.tar.gz` dans `~/saccra_backups/` avec le format :
```
saccra_backup_YYYYMMDD_HHMMSS.tar.gz
```

### Sauvegarde Automatique (Cron)

Pour sauvegarder automatiquement tous les jours à 3h du matin :

```bash
# Ouvrir le crontab
crontab -e

# Ajouter cette ligne :
0 3 * * * /home/wrbh3411/saccra.fr/backup.sh >> /home/wrbh3411/saccra_backups/backup.log 2>&1
```

**Exemples de fréquences :**
- Tous les jours à 3h : `0 3 * * *`
- Toutes les 6 heures : `0 */6 * * *`
- Tous les lundis à minuit : `0 0 * * 1`
- Toutes les heures : `0 * * * *`

---

## 🔄 Restaurer une Sauvegarde

### Restauration Interactive

```bash
cd ~/saccra.fr
bash restore.sh
```

Le script vous demandera :
1. **Quel backup restaurer** (liste numérotée)
2. **Confirmation** (tape "oui" pour confirmer)
3. **Redémarrage** (tape "oui" pour redémarrer automatiquement)

### Restauration Manuelle

Si tu préfères restaurer manuellement :

```bash
# 1. Extraire le backup
cd ~/saccra_backups
tar -xzf saccra_backup_YYYYMMDD_HHMMSS.tar.gz

# 2. Restaurer les fichiers
cd temp_YYYYMMDD_HHMMSS
cp sacra.db ~/saccra.fr/instance/
cp .env ~/saccra.fr/
cp .htaccess ~/saccra.fr/

# 3. Redémarrer l'application
cd ~/saccra.fr
pkill -9 -u wrbh3411 python
sleep 3
touch tmp/restart.txt
```

---

## 📋 Gestion des Backups

### Lister les Backups

```bash
ls -lh ~/saccra_backups/saccra_backup_*.tar.gz
```

### Voir le Contenu d'un Backup

```bash
tar -tzf ~/saccra_backups/saccra_backup_YYYYMMDD_HHMMSS.tar.gz
```

### Supprimer les Vieux Backups

Le script conserve automatiquement **les 10 backups les plus récents**.

Pour nettoyer manuellement :
```bash
cd ~/saccra_backups
# Garder seulement les 5 derniers
ls -t saccra_backup_*.tar.gz | tail -n +6 | xargs rm
```

---

## 🚨 Situations d'Urgence

### La base de données est corrompue

```bash
cd ~/saccra.fr
bash restore.sh
# Sélectionner le backup le plus récent
```

### Le site ne fonctionne plus

```bash
# 1. Restaurer tout
cd ~/saccra.fr
bash restore.sh

# 2. Vérifier les logs
tail -f ~/logs/error.log

# 3. Redémarrer
pkill -9 -u wrbh3411 python
touch tmp/restart.txt
```

### Perte du fichier .env

```bash
# Restaurer uniquement le .env d'un backup
cd ~/saccra_backups
tar -xzf saccra_backup_YYYYMMDD_HHMMSS.tar.gz
cp temp_*/. env ~/saccra.fr/.env
```

---

## 📥 Télécharger un Backup

### Via SCP (depuis ton ordinateur)

```bash
scp wrbh3411@ssh.o2switch.net:~/saccra_backups/saccra_backup_*.tar.gz ~/Downloads/
```

### Via FTP

1. Connecte-toi via FileZilla ou un client FTP
2. Navigue vers `/home/wrbh3411/saccra_backups/`
3. Télécharge les fichiers `.tar.gz`

---

## ✅ Bonnes Pratiques

1. **Sauvegarde régulière** - Configure un cron pour sauvegarder automatiquement
2. **Backups externes** - Télécharge un backup par semaine sur ton ordinateur
3. **Test de restauration** - Teste la restauration au moins une fois par mois
4. **Avant mise à jour** - Toujours faire un backup avant de modifier le code
5. **Avant migration** - Backup avant de changer de serveur

---

## 🔧 Dépannage

### Le script ne s'exécute pas

```bash
# Rendre le script exécutable
chmod +x ~/saccra.fr/backup.sh
chmod +x ~/saccra.fr/restore.sh
```

### Pas d'espace disque

```bash
# Vérifier l'espace disponible
df -h

# Nettoyer les vieux backups
cd ~/saccra_backups
ls -t saccra_backup_*.tar.gz | tail -n +3 | xargs rm
```

### Backup trop gros

Si les backups deviennent trop volumineux :
- Exclure les logs (modifie `backup.sh`)
- Compresser davantage avec `tar -czf` → `tar -cjf` (bzip2)

---

## 📞 Support

Pour toute question ou problème :
- Vérifier les logs : `~/saccra_backups/backup.log`
- Contacter le support o2switch
- Consulter la documentation SACRA

---

**Dernière mise à jour :** 2025-01-26
**Version :** 1.0

# 🚀 Guide de Déploiement SACCRA

## Configuration initiale sur o2switch

### 1. Configurer le fichier .htaccess

**IMPORTANT:** Le fichier `.htaccess` contient des chemins spécifiques à ton serveur et ne doit jamais être commité dans Git.

```bash
# Se connecter au serveur
ssh wrbh3411@ssh.o2switch.net
cd ~/saccra.fr

# Copier l'exemple et l'adapter
cp .htaccess.example .htaccess

# Éditer avec ton nom d'utilisateur
nano .htaccess
# Remplace TOUS les "TON_USER" par "wrbh3411"
# Remplace "sacra.fr" par "saccra.fr" si nécessaire

# Vérifier que le fichier est correct
cat .htaccess | grep PassengerAppRoot
# Doit afficher: PassengerAppRoot /home/wrbh3411/saccra.fr
```

**Contenu du .htaccess correct:**
```apache
PassengerEnabled On
PassengerAppRoot /home/wrbh3411/saccra.fr
PassengerPython /home/wrbh3411/saccra.fr/venv/bin/python3

RewriteEngine On
RewriteCond %{HTTPS} off
RewriteRule ^(.*)$ https://%{HTTP_HOST}%{REQUEST_URI} [L,R=301]
```

### 2. Configurer les variables d'environnement

```bash
# Créer/éditer le fichier .env
nano .env

# Ajouter ta clé API OpenAI
OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxxxxxxx
OPENAI_MODEL=gpt-4o-mini
SECRET_KEY=votre-secret-key-tres-securisee
```

### 3. Copier le script de déploiement sur le serveur

```bash
# Option A : Via SCP depuis ton ordinateur local
scp deploy.sh user@ssh.o2switch.net:~/saccra/

# Option B : Créer directement sur le serveur
ssh user@ssh.o2switch.net
cd ~/saccra
nano deploy.sh
# Coller le contenu du script
chmod +x deploy.sh
```

### 2. Tester le script

```bash
ssh user@ssh.o2switch.net
cd ~/saccra
./deploy.sh
```

## Utilisation quotidienne

### Après chaque commit/push depuis ton PC :

```bash
# 1. Push ton code (déjà fait automatiquement par Claude Code)
git push

# 2. Déployer sur o2switch
ssh user@ssh.o2switch.net "cd ~/saccra && ./deploy.sh"
```

### Ou en une seule commande depuis ton PC :

```bash
ssh user@ssh.o2switch.net "cd ~/saccra && ./deploy.sh"
```

## Automatisation complète (optionnel)

### Créer un alias sur ton PC

Ajouter dans `~/.bashrc` ou `~/.zshrc` :

```bash
alias deploy-saccra="ssh user@ssh.o2switch.net 'cd ~/saccra && ./deploy.sh'"
```

Ensuite tu peux juste taper :
```bash
deploy-saccra
```

## Vérifications

Après chaque déploiement, vérifie :
- ✅ https://saccra.fr (site accessible)
- ✅ https://saccra.fr/admin/dashboard (admin fonctionne)
- ✅ Logs : `tail -f ~/logs/passenger.log`

## Rollback en cas de problème

```bash
ssh user@ssh.o2switch.net
cd ~/saccra
git log --oneline  # Voir les commits
git reset --hard COMMIT_ID  # Revenir à un commit précédent
./deploy.sh
```

## Troubleshooting

### Le script ne s'exécute pas
```bash
chmod +x deploy.sh
```

### Erreur "Permission denied"
```bash
# Vérifier les droits
ls -la deploy.sh
# Doit afficher : -rwxr-xr-x
```

### Le site ne se met pas à jour
```bash
# Vérifier que Passenger a bien redémarré
ls -la tmp/restart.txt
# Forcer le redémarrage
touch tmp/restart.txt
```

### Voir les logs d'erreur
```bash
tail -50 ~/logs/passenger.log
tail -50 ~/logs/error.log
```

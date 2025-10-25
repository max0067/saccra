# 🚀 Guide de Déploiement SACCRA

## Installation du script sur o2switch

### 1. Copier le script sur le serveur

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

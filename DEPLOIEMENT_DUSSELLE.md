# Guide de déploiement sur dusselle.fr

## Informations du serveur
- **Serveur**: wrbh3411@down.dusselle.fr (ou votre serveur o2switch)
- **Chemin**: /home/wrbh3411/dusselle.fr
- **Branche**: claude/fix-dusselle-server-deployment-011CUph9wL2PPQTG8f6kykgU

## Étapes de déploiement

### 1. Connexion au serveur
```bash
ssh wrbh3411@down.dusselle.fr
# Ou via le terminal web d'o2switch si SSH n'est pas disponible
```

### 2. Aller dans le dossier du site
```bash
cd /home/wrbh3411/dusselle.fr
```

### 3. Récupérer les dernières modifications
```bash
# Récupérer la branche de déploiement
git fetch origin claude/fix-dusselle-server-deployment-011CUph9wL2PPQTG8f6kykgU

# Basculer sur cette branche
git checkout claude/fix-dusselle-server-deployment-011CUph9wL2PPQTG8f6kykgU

# Mettre à jour
git pull origin claude/fix-dusselle-server-deployment-011CUph9wL2PPQTG8f6kykgU
```

### 4. Créer l'environnement virtuel Python (si pas encore fait)
```bash
# Créer l'environnement virtuel
python3 -m venv venv

# Activer l'environnement virtuel
source venv/bin/activate

# Installer les dépendances
pip install --upgrade pip
pip install -r requirements.txt
```

### 5. Configurer les variables d'environnement
```bash
# Copier le fichier d'exemple
cp .env.example .env

# Éditer le fichier .env avec vos vraies clés
nano .env
```

**Variables à configurer dans .env :**
- `SECRET_KEY`: Générer une clé secrète aléatoire
- `OPENAI_API_KEY`: Votre clé API OpenAI
- `STRIPE_PUBLIC_KEY`: Clé publique Stripe
- `STRIPE_SECRET_KEY`: Clé secrète Stripe
- `STRIPE_WEBHOOK_SECRET`: Secret webhook Stripe
- `STRIPE_MONTHLY_PRICE_ID`: ID du prix mensuel
- `STRIPE_YEARLY_PRICE_ID`: ID du prix annuel

### 6. Initialiser la base de données (première fois seulement)
```bash
# Activer l'environnement virtuel si ce n'est pas déjà fait
source venv/bin/activate

# Lancer Python
python3

# Dans l'interpréteur Python :
from app import create_app, db
app = create_app()
with app.app_context():
    db.create_all()
exit()
```

### 7. Vérifier les permissions
```bash
# S'assurer que les permissions sont correctes
chmod 755 passenger_wsgi.py
chmod 644 .htaccess
chmod 600 .env
```

### 8. Redémarrer Passenger
```bash
# Créer/toucher le fichier restart.txt pour redémarrer l'application
mkdir -p tmp
touch tmp/restart.txt

# Ou via le panel o2switch : "Redémarrer l'application Python"
```

## Vérification du déploiement

1. Ouvrir https://dusselle.fr dans votre navigateur
2. Vérifier que la page d'accueil se charge correctement
3. Tester la création de compte
4. Tester le tirage de tarot

## Fichiers de logs (en cas de problème)

Les logs Passenger se trouvent généralement dans :
```bash
cat ~/logs/dusselle.fr/error_log
cat ~/logs/dusselle.fr/access_log
```

## Commandes utiles pour le debugging

### Voir les logs en temps réel
```bash
tail -f ~/logs/dusselle.fr/error_log
```

### Vérifier l'état de Passenger
```bash
passenger-status
```

### Forcer le redémarrage de Passenger
```bash
touch tmp/restart.txt
# ou
passenger-config restart-app /home/wrbh3411/dusselle.fr
```

## Problèmes courants

### L'application ne démarre pas
1. Vérifier que l'environnement virtuel existe : `ls -la venv/`
2. Vérifier que toutes les dépendances sont installées : `source venv/bin/activate && pip list`
3. Vérifier les logs : `tail -50 ~/logs/dusselle.fr/error_log`

### Erreur 500
1. Vérifier que le fichier .env existe et contient toutes les variables
2. Vérifier les permissions : .env doit être en 600
3. Consulter les logs d'erreur

### Module non trouvé
```bash
source venv/bin/activate
pip install -r requirements.txt
touch tmp/restart.txt
```

## Structure des fichiers importants

```
/home/wrbh3411/dusselle.fr/
├── .htaccess                 # Configuration Apache/Passenger
├── passenger_wsgi.py         # Point d'entrée Passenger
├── app.py                    # Point d'entrée de l'application
├── .env                      # Variables d'environnement (à créer)
├── .env.example              # Exemple de configuration
├── requirements.txt          # Dépendances Python
├── venv/                     # Environnement virtuel Python
├── app/                      # Code de l'application
│   ├── __init__.py
│   ├── models.py
│   ├── routes/
│   └── templates/
├── tmp/
│   └── restart.txt          # Touch ce fichier pour redémarrer
└── instance/
    └── sacra.db             # Base de données SQLite
```

## Notes importantes

- Le fichier `.htaccess` est déjà configuré avec les bons chemins pour dusselle.fr
- L'application utilise SQLite pour la base de données (fichier instance/sacra.db)
- Les fichiers statiques sont servis automatiquement depuis app/static/
- Le mode debug est désactivé en production

# 🚀 Guide de déploiement SACRA sur o2switch

Ce guide te permettra de déployer SACRA sur ton hébergement o2switch étape par étape.

---

## 📋 Prérequis

- [ ] Compte o2switch actif
- [ ] Accès FTP/SFTP (FileZilla, Cyberduck, ou panneau o2switch)
- [ ] Accès SSH (optionnel mais recommandé)
- [ ] Domaine `sacra.fr` pointé vers o2switch
- [ ] Clé API OpenAI
- [ ] Compte Stripe configuré

---

## 🔧 Étape 1 : Préparation locale

### 1.1 Vérifier que tout fonctionne
```bash
# Activer l'environnement virtuel
source venv/bin/activate

# Tester l'application
python app.py
```

Accède à `http://localhost:5000` et vérifie que tout marche.

### 1.2 Créer le fichier .env de production
```bash
cp .env.example .env.production
```

Éditer `.env.production` avec les vraies clés de production :
```env
# Flask
SECRET_KEY=GENERE-UNE-CLE-SECRETE-ALEATOIRE-ICI-32-CARACTERES

# OpenAI (PRODUCTION)
OPENAI_API_KEY=sk-proj-VOTRE-CLE-PRODUCTION

# Stripe (PRODUCTION - pas test!)
STRIPE_PUBLIC_KEY=pk_live_VOTRE_CLE_PUBLIQUE
STRIPE_SECRET_KEY=sk_live_VOTRE_CLE_SECRETE
STRIPE_WEBHOOK_SECRET=whsec_VOTRE_WEBHOOK_SECRET

# Prix Stripe (IDs de production)
STRIPE_MONTHLY_PRICE_ID=price_VOTRE_PRICE_ID_MENSUEL
STRIPE_YEARLY_PRICE_ID=price_VOTRE_PRICE_ID_ANNUEL
```

**⚠️ Important** : Ne jamais commiter le fichier `.env.production` !

---

## 📤 Étape 2 : Upload des fichiers sur o2switch

### Option A : Via FTP/SFTP (recommandé pour débutants)

1. **Connecte-toi via FileZilla** :
   - Hôte : `ftp.sacra.fr` (ou l'adresse donnée par o2switch)
   - Utilisateur : ton compte o2switch
   - Mot de passe : ton mot de passe o2switch
   - Port : 21 (FTP) ou 22 (SFTP)

2. **Naviguer vers le répertoire du site** :
   - Généralement : `/home/TON_USER/sacra.fr/` ou `/www/sacra.fr/`

3. **Uploader TOUS les fichiers du projet**, SAUF :
   - ❌ `venv/` (environnement virtuel local)
   - ❌ `instance/` (base de données locale)
   - ❌ `__pycache__/`
   - ❌ `.git/`
   - ✅ Tous les autres fichiers

4. **Renommer** `.env.production` en `.env` sur le serveur

### Option B : Via Git (si o2switch a Git)

```bash
# Sur le serveur o2switch (via SSH)
cd /home/TON_USER/sacra.fr
git clone https://github.com/TON_USER/saccra.git .
git checkout claude/sacra-mvp-development-011CUTwpK9Jt9EvPxAvnxTyp
```

---

## 🐍 Étape 3 : Installation de Python et dépendances

### 3.1 Connexion SSH à o2switch
```bash
ssh TON_USER@ssh.sacra.fr
# Ou depuis le panneau o2switch : Terminal
```

### 3.2 Vérifier la version Python
```bash
python3 --version  # Devrait être >= 3.8
```

Si Python 3 n'est pas disponible, contacte le support o2switch.

### 3.3 Créer l'environnement virtuel sur le serveur
```bash
cd ~/sacra.fr  # ou le chemin de ton site
python3 -m venv venv
```

### 3.4 Installer les dépendances
```bash
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

**⚠️ Si erreur de permissions** :
```bash
pip install -r requirements.txt --user
```

### 3.5 Initialiser la base de données
```bash
python3 -c "from app import create_app; app = create_app(); app.app_context().push()"
```

Cela créera automatiquement `instance/sacra.db` avec toutes les tables.

---

## ⚙️ Étape 4 : Configuration de Passenger (o2switch)

### 4.1 Vérifier passenger_wsgi.py
Le fichier `passenger_wsgi.py` est déjà configuré. Vérifie qu'il existe :
```bash
ls -la passenger_wsgi.py
```

### 4.2 Créer/modifier .htaccess
Le fichier `.htaccess` devrait déjà exister. Vérifie son contenu :
```apache
PassengerEnabled On
PassengerAppRoot /home/TON_USER/sacra.fr
PassengerPython /home/TON_USER/sacra.fr/venv/bin/python3

# Redirection HTTPS (recommandé)
RewriteEngine On
RewriteCond %{HTTPS} off
RewriteRule ^(.*)$ https://%{HTTP_HOST}%{REQUEST_URI} [L,R=301]
```

**Remplace `/home/TON_USER/sacra.fr`** par le vrai chemin !

### 4.3 Redémarrer Passenger
```bash
mkdir -p tmp
touch tmp/restart.txt
```

Ou depuis le panneau o2switch : **Redémarrer l'application**

---

## 🔐 Étape 5 : Configuration des variables d'environnement

### Option A : Fichier .env (plus simple)
Assure-toi que le fichier `.env` existe à la racine avec toutes les clés.

### Option B : Variables d'environnement système (plus sécurisé)
Dans le panneau o2switch, section **Variables d'environnement** :
```
SECRET_KEY=ta-cle-secrete
OPENAI_API_KEY=sk-proj-...
STRIPE_PUBLIC_KEY=pk_live_...
STRIPE_SECRET_KEY=sk_live_...
...
```

---

## 🌐 Étape 6 : Configuration du domaine

### 6.1 Pointer le domaine
Dans le panneau o2switch :
1. **Domaines** → **Ajouter un domaine**
2. Entrer `sacra.fr`
3. Répertoire cible : `/home/TON_USER/sacra.fr`

### 6.2 Activer SSL/HTTPS
Dans le panneau o2switch :
1. **SSL/TLS** → **Let's Encrypt**
2. Sélectionner `sacra.fr`
3. Cliquer sur **Installer le certificat SSL**

---

## 💳 Étape 7 : Configuration Stripe

### 7.1 Créer les produits Stripe (mode LIVE)
1. Aller sur https://dashboard.stripe.com/products
2. Passer en **mode Live** (toggle en haut à droite)
3. Créer 2 produits :
   - **SACRA Premium Mensuel** : 9,90 EUR/mois (récurrent)
   - **SACRA Premium Annuel** : 49 EUR/an (récurrent)
4. Copier les `price_id` dans `.env`

### 7.2 Configurer le webhook Stripe
1. Aller sur https://dashboard.stripe.com/webhooks
2. **Ajouter un endpoint** :
   - URL : `https://sacra.fr/premium/webhook`
   - Événements :
     - `checkout.session.completed`
     - `invoice.payment_succeeded`
     - `customer.subscription.deleted`
3. Copier le **Signing secret** (whsec_xxx) dans `.env`

### 7.3 Tester le paiement
- Utilise une carte de test Stripe : `4242 4242 4242 4242`
- Date : n'importe quelle date future
- CVC : n'importe quel 3 chiffres

---

## ✅ Étape 8 : Vérification finale

### 8.1 Tester les pages principales
- [ ] https://sacra.fr → Page d'accueil OK
- [ ] https://sacra.fr/auth/register → Inscription OK
- [ ] https://sacra.fr/auth/login → Connexion OK
- [ ] https://sacra.fr/dashboard → Dashboard OK
- [ ] https://sacra.fr/interpret/dream → Interprétation de rêve OK
- [ ] https://sacra.fr/interpret/sign → Signes OK
- [ ] https://sacra.fr/interpret/tarot → Tirage OK
- [ ] https://sacra.fr/premium/subscribe → Page Premium OK

### 8.2 Tester l'IA
1. Créer un compte test
2. Entrer un rêve
3. Vérifier que l'IA répond correctement
4. Vérifier que le compteur passe de 3/3 à 2/3

### 8.3 Tester Stripe (en mode test d'abord)
1. Cliquer sur "Passer en Premium"
2. Utiliser la carte de test : `4242 4242 4242 4242`
3. Vérifier la redirection après paiement
4. Vérifier que le compte est bien Premium

---

## 🐛 Résolution des problèmes courants

### Erreur 500 (Internal Server Error)
```bash
# Voir les logs
tail -f ~/logs/sacra.fr/error.log

# Ou
tail -f ~/sacra.fr/tmp/error.log
```

**Solutions courantes** :
- Vérifier que `venv/bin/python3` existe
- Vérifier les permissions : `chmod 755 passenger_wsgi.py`
- Vérifier le `.env` : toutes les clés sont présentes ?
- Redémarrer : `touch tmp/restart.txt`

### Base de données verrouillée
```bash
# Permissions de la BDD
chmod 644 instance/sacra.db
chmod 755 instance/
```

### OpenAI ne répond pas
- Vérifier que `OPENAI_API_KEY` est correcte
- Vérifier les quotas OpenAI sur https://platform.openai.com/usage
- Tester l'API manuellement :
```bash
curl https://api.openai.com/v1/models \
  -H "Authorization: Bearer $OPENAI_API_KEY"
```

### Stripe ne fonctionne pas
- Vérifier que tu es en **mode Live** (pas Test)
- Vérifier les `price_id` dans `.env`
- Vérifier le webhook : URL correcte ?

---

## 📊 Monitoring et maintenance

### Logs
```bash
# Voir les logs en temps réel
tail -f ~/logs/sacra.fr/error.log
tail -f ~/logs/sacra.fr/access.log
```

### Redémarrer l'app après une modification
```bash
touch ~/sacra.fr/tmp/restart.txt
```

### Backup de la base de données
```bash
# Créer un backup
cp instance/sacra.db instance/sacra_backup_$(date +%Y%m%d).db

# Automatiser (crontab)
0 3 * * * cp ~/sacra.fr/instance/sacra.db ~/backups/sacra_$(date +\%Y\%m\%d).db
```

### Mise à jour du code
```bash
cd ~/sacra.fr
git pull origin claude/sacra-mvp-development-011CUTwpK9Jt9EvPxAvnxTyp
touch tmp/restart.txt
```

---

## 🎯 Checklist finale avant lancement

- [ ] SSL/HTTPS activé et fonctionne
- [ ] Toutes les pages s'affichent correctement
- [ ] Inscription/Connexion fonctionnent
- [ ] L'IA répond correctement (OpenAI)
- [ ] Le compteur freemium fonctionne (3/mois)
- [ ] Stripe Checkout fonctionne (test puis prod)
- [ ] Les webhooks Stripe sont configurés
- [ ] La base de données est sauvegardée
- [ ] Les logs sont accessibles
- [ ] Le design est responsive (mobile)
- [ ] Les erreurs sont gérées proprement

---

## 📞 Support

### Problèmes o2switch
- Support o2switch : https://www.o2switch.fr/support
- Documentation : https://faq.o2switch.fr

### Problèmes OpenAI
- Documentation : https://platform.openai.com/docs
- Support : https://help.openai.com

### Problèmes Stripe
- Documentation : https://stripe.com/docs
- Support : https://support.stripe.com

---

## 🚀 C'est en ligne !

Une fois tout testé, ton site SACRA est **officiellement en ligne** sur https://sacra.fr ! 🌙✨

N'oublie pas de :
- Partager sur les réseaux sociaux
- Créer du contenu SEO (articles de blog)
- Surveiller les premiers utilisateurs
- Collecter les feedbacks

Bon lancement ! 💫

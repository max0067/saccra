# ⚡ Quick Start - Déploiement SACRA sur o2switch

Guide ultra-rapide en 5 étapes pour déployer SACRA.

---

## 🎯 Les 5 étapes essentielles

### 1️⃣ Préparer les clés API (15 min)

**OpenAI** → https://platform.openai.com/api-keys
- Créer une clé API
- Copier la clé : `sk-proj-...`

**Stripe** → https://dashboard.stripe.com
- Passer en mode **Live**
- Copier la clé publique : `pk_live_...`
- Copier la clé secrète : `sk_live_...`
- Créer 2 produits (9,90€/mois et 49€/an)
- Copier les `price_id` : `price_...`

---

### 2️⃣ Configurer le fichier .env (5 min)

Créer un fichier `.env` à la racine :

```bash
SECRET_KEY=$(python3 -c "import secrets; print(secrets.token_hex(32))")

OPENAI_API_KEY=sk-proj-TON_API_KEY

STRIPE_PUBLIC_KEY=pk_live_TON_API_KEY
STRIPE_SECRET_KEY=sk_live_TON_API_KEY
STRIPE_WEBHOOK_SECRET=whsec_TON_WEBHOOK_SECRET

STRIPE_MONTHLY_PRICE_ID=price_TON_PRICE_ID
STRIPE_YEARLY_PRICE_ID=price_TON_PRICE_ID
```

---

### 3️⃣ Uploader sur o2switch (10 min)

**Via FTP (FileZilla, Cyberduck...)** :

1. Connecter à `ftp.sacra.fr`
2. Aller dans `/home/TON_USER/sacra.fr/`
3. Uploader **tous les fichiers** sauf :
   - ❌ `venv/`
   - ❌ `instance/`
   - ❌ `__pycache__/`
   - ❌ `.git/`

---

### 4️⃣ Installer et configurer (10 min)

**Via SSH o2switch** :

```bash
# Se connecter
ssh TON_USER@ssh.sacra.fr

# Aller dans le répertoire
cd ~/sacra.fr

# Lancer le script de setup
bash setup_o2switch.sh

# Éditer .htaccess (remplacer TON_USER par ton vrai username)
nano .htaccess
# Remplace : /home/TON_USER/sacra.fr
# Par : /home/VRAI_USER/sacra.fr
# Ctrl+X pour sauvegarder

# Redémarrer
touch tmp/restart.txt
```

---

### 5️⃣ Configurer le domaine et SSL (5 min)

**Dans le panneau o2switch** :

1. **Domaines** → Ajouter `sacra.fr`
   - Répertoire : `/home/TON_USER/sacra.fr`

2. **SSL/TLS** → Let's Encrypt
   - Sélectionner `sacra.fr`
   - Installer le certificat

3. **Tester** : https://sacra.fr

---

## ✅ Checklist rapide

- [ ] Clés OpenAI et Stripe obtenues
- [ ] Fichier `.env` créé avec toutes les clés
- [ ] Fichiers uploadés sur o2switch
- [ ] `setup_o2switch.sh` exécuté
- [ ] `.htaccess` modifié (TON_USER remplacé)
- [ ] Domaine configuré
- [ ] SSL activé
- [ ] Site testé sur https://sacra.fr

---

## 🆘 Problème ?

**Erreur 500** :
```bash
tail -f ~/logs/sacra.fr/error.log
```

**L'IA ne répond pas** :
- Vérifier `OPENAI_API_KEY` dans `.env`
- Vérifier le crédit OpenAI

**Stripe ne fonctionne pas** :
- Vérifier mode **Live** (pas Test)
- Vérifier les `price_id`

---

## 📖 Documentation complète

- **Guide détaillé** : `DEPLOY.md`
- **Configuration env** : `ENV_CONFIG.md`
- **Vérification** : `python3 verify_deployment.py`

---

🚀 **C'est tout !** Ton site SACRA est en ligne ! 🌙✨

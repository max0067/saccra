# 🔐 Configuration des variables d'environnement - SACRA

Ce document détaille toutes les variables d'environnement nécessaires pour faire fonctionner SACRA.

---

## 📝 Fichier .env

Le fichier `.env` doit être placé à la racine du projet et contenir les clés suivantes :

```env
# ============================================
# FLASK
# ============================================

# Clé secrète pour les sessions Flask
# ⚠️ IMPORTANT : Génère une clé aléatoire et sécurisée !
# Exemple de génération : python3 -c "import secrets; print(secrets.token_hex(32))"
SECRET_KEY=ta-cle-secrete-aleatoire-de-64-caracteres-minimum

# ============================================
# OPENAI
# ============================================

# Clé API OpenAI
# Obtenir sur : https://platform.openai.com/api-keys
# Format : sk-proj-XXXXXXXXXXXXX
OPENAI_API_KEY=sk-proj-...

# Modèle à utiliser (optionnel, par défaut gpt-4o-mini)
OPENAI_MODEL=gpt-4o-mini

# ============================================
# STRIPE
# ============================================

# Clés API Stripe (MODE PRODUCTION)
# Obtenir sur : https://dashboard.stripe.com/apikeys
# ⚠️ Utilise pk_live_ et sk_live_ en production, pas pk_test_ !

# Clé publique (visible côté client)
STRIPE_PUBLIC_KEY=pk_live_XXXXXXXXXXXXXXXXXX

# Clé secrète (gardée sur le serveur)
STRIPE_SECRET_KEY=sk_live_XXXXXXXXXXXXXXXXXX

# Secret du webhook (pour vérifier les événements)
# Obtenir après création du webhook sur https://dashboard.stripe.com/webhooks
STRIPE_WEBHOOK_SECRET=whsec_XXXXXXXXXXXXXXXXXX

# ============================================
# PRODUITS STRIPE
# ============================================

# ID du prix mensuel (9,90€/mois)
# Créer sur : https://dashboard.stripe.com/products
# Format : price_XXXXXXXXXXXXX
STRIPE_MONTHLY_PRICE_ID=price_...

# ID du prix annuel (49€/an)
STRIPE_YEARLY_PRICE_ID=price_...

# ============================================
# EMAIL (OPTIONNEL pour le MVP)
# ============================================

# Configuration SMTP pour l'envoi d'emails
# Si tu n'utilises pas les emails, laisse vide

MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USERNAME=ton-email@gmail.com
MAIL_PASSWORD=ton-mot-de-passe-app
MAIL_DEFAULT_SENDER=noreply@sacra.fr
```

---

## 🔑 Comment obtenir chaque clé

### 1. SECRET_KEY

**Génération d'une clé aléatoire sécurisée** :

```bash
python3 -c "import secrets; print(secrets.token_hex(32))"
```

Exemple de sortie :
```
a8f5f167f44f4964e6c998dee827110c3fa0b6c7f6e4a0e6c5d8f2e3a9b1c4d5
```

Copie cette clé dans `.env` :
```env
SECRET_KEY=a8f5f167f44f4964e6c998dee827110c3fa0b6c7f6e4a0e6c5d8f2e3a9b1c4d5
```

---

### 2. OPENAI_API_KEY

**Étapes** :
1. Aller sur https://platform.openai.com/api-keys
2. Se connecter avec ton compte OpenAI
3. Cliquer sur **"Create new secret key"**
4. Nommer la clé : `SACRA Production`
5. Copier la clé (elle commence par `sk-proj-...`)
6. **⚠️ Important** : Tu ne pourras plus la voir après, sauvegarde-la !

**Dans .env** :
```env
OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

**💰 Coût estimé** :
- Modèle `gpt-4o-mini` : ~0,15$ par 1000 interprétations
- Budget recommandé : 10-20$/mois pour commencer

**Surveiller l'usage** : https://platform.openai.com/usage

---

### 3. STRIPE (Clés API)

**Étapes** :
1. Aller sur https://dashboard.stripe.com/register
2. Créer un compte Stripe
3. Activer le compte (vérification KYC)
4. Aller sur https://dashboard.stripe.com/apikeys
5. **⚠️ Passer en mode "Live"** (toggle en haut à droite)
6. Copier la **Publishable key** (pk_live_xxx)
7. Révéler et copier la **Secret key** (sk_live_xxx)

**Dans .env** :
```env
STRIPE_PUBLIC_KEY=pk_live_VOTRE_CLE_PUBLIQUE_STRIPE
STRIPE_SECRET_KEY=sk_live_VOTRE_CLE_SECRETE_STRIPE
```

---

### 4. STRIPE_MONTHLY_PRICE_ID et STRIPE_YEARLY_PRICE_ID

**Création des produits Stripe** :

1. Aller sur https://dashboard.stripe.com/products
2. **⚠️ Être en mode "Live"**
3. Cliquer sur **"Add product"**

**Produit 1 : Premium Mensuel**
- Name : `SACRA Premium Mensuel`
- Description : `Accès illimité à SACRA - Abonnement mensuel`
- Pricing model : `Recurring`
- Price : `9.90 EUR`
- Billing period : `Monthly`
- Cliquer sur **"Save product"**
- Copier le **Price ID** (commence par `price_xxx`)

**Produit 2 : Premium Annuel**
- Name : `SACRA Premium Annuel`
- Description : `Accès illimité à SACRA - Abonnement annuel (économie de 17%)`
- Pricing model : `Recurring`
- Price : `49.00 EUR`
- Billing period : `Yearly`
- Cliquer sur **"Save product"**
- Copier le **Price ID** (commence par `price_xxx`)

**Dans .env** :
```env
STRIPE_MONTHLY_PRICE_ID=price_VOTRE_ID_PRODUIT_MENSUEL
STRIPE_YEARLY_PRICE_ID=price_VOTRE_ID_PRODUIT_ANNUEL
```

---

### 5. STRIPE_WEBHOOK_SECRET

**Configuration du webhook Stripe** :

1. Aller sur https://dashboard.stripe.com/webhooks
2. **⚠️ Être en mode "Live"**
3. Cliquer sur **"Add endpoint"**
4. URL : `https://sacra.fr/premium/webhook`
5. Description : `SACRA Production Webhook`
6. Sélectionner les événements :
   - ✅ `checkout.session.completed`
   - ✅ `invoice.payment_succeeded`
   - ✅ `customer.subscription.deleted`
7. Cliquer sur **"Add endpoint"**
8. Copier le **Signing secret** (commence par `whsec_xxx`)

**Dans .env** :
```env
STRIPE_WEBHOOK_SECRET=whsec_VOTRE_WEBHOOK_SECRET_STRIPE
```

**💡 Tester le webhook localement** (optionnel) :
```bash
# Installer Stripe CLI
# https://stripe.com/docs/stripe-cli

# Écouter les événements
stripe listen --forward-to localhost:5000/premium/webhook
```

---

### 6. Email (optionnel)

**Si tu veux utiliser Gmail** :

1. Aller sur https://myaccount.google.com/security
2. Activer la **validation en deux étapes**
3. Générer un **mot de passe d'application** :
   - Aller sur https://myaccount.google.com/apppasswords
   - Nom : `SACRA`
   - Copier le mot de passe généré

**Dans .env** :
```env
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USERNAME=ton-email@gmail.com
MAIL_PASSWORD=xxxx xxxx xxxx xxxx  # Mot de passe d'application
MAIL_DEFAULT_SENDER=noreply@sacra.fr
```

**⚠️ Note** : L'email n'est pas utilisé dans le MVP actuel, tu peux laisser vide pour l'instant.

---

## 🔒 Sécurité

### ⚠️ IMPORTANT - À NE JAMAIS FAIRE :

❌ **Ne JAMAIS commiter le fichier `.env` sur Git**
❌ **Ne JAMAIS partager tes clés API publiquement**
❌ **Ne JAMAIS utiliser les clés de test en production**

### ✅ Bonnes pratiques :

✅ Garder `.env` dans `.gitignore`
✅ Utiliser des clés différentes pour dev/test/prod
✅ Régénérer les clés si elles sont compromises
✅ Utiliser des variables d'environnement système en production
✅ Limiter les permissions des clés API
✅ Surveiller l'usage et les logs

---

## 🔄 Rotation des clés

**Si une clé est compromise** :

1. **OpenAI** :
   - Révoquer la clé sur https://platform.openai.com/api-keys
   - Générer une nouvelle clé
   - Mettre à jour `.env`

2. **Stripe** :
   - Révoquer la clé sur https://dashboard.stripe.com/apikeys
   - Générer une nouvelle clé
   - Mettre à jour `.env`

3. **Redémarrer l'application** :
   ```bash
   touch tmp/restart.txt
   ```

---

## 📊 Monitoring

### Vérifier que les clés fonctionnent :

**OpenAI** :
```bash
curl https://api.openai.com/v1/models \
  -H "Authorization: Bearer $OPENAI_API_KEY"
```

**Stripe** :
```bash
curl https://api.stripe.com/v1/customers \
  -u $STRIPE_SECRET_KEY:
```

---

## 🆘 Problèmes fréquents

### "OpenAI API key not found"
- Vérifier que `OPENAI_API_KEY` est dans `.env`
- Vérifier que la clé commence par `sk-proj-`
- Vérifier que le compte OpenAI a du crédit

### "Stripe error: Invalid API Key"
- Vérifier que tu es en mode **Live** (pas Test)
- Vérifier que la clé commence par `sk_live_` (pas `sk_test_`)
- Vérifier que le compte Stripe est activé

### "Module not found"
- Vérifier que le venv est activé
- Réinstaller : `pip install -r requirements.txt`

---

## ✅ Checklist finale

Avant de déployer, vérifie que :

- [ ] `SECRET_KEY` est une clé aléatoire longue
- [ ] `OPENAI_API_KEY` commence par `sk-proj-`
- [ ] `STRIPE_PUBLIC_KEY` commence par `pk_live_` (pas `pk_test_`)
- [ ] `STRIPE_SECRET_KEY` commence par `sk_live_` (pas `sk_test_`)
- [ ] `STRIPE_WEBHOOK_SECRET` commence par `whsec_`
- [ ] Les 2 `STRIPE_*_PRICE_ID` commencent par `price_`
- [ ] Le fichier `.env` n'est pas commité dans Git
- [ ] Les clés sont différentes de `.env.example`

---

## 📞 Support

Si tu as des questions :
- OpenAI : https://help.openai.com
- Stripe : https://support.stripe.com
- o2switch : https://www.o2switch.fr/support

Bon déploiement ! 🌙✨

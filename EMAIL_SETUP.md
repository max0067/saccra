# 📧 Configuration des Emails SACRA

Guide pour configurer l'envoi d'emails de bienvenue lors de l'inscription.

---

## 🎯 Fonctionnalité

Lorsqu'un utilisateur s'inscrit sur SACRA, il reçoit automatiquement un **email de bienvenue** avec :
- Message de bienvenue personnalisé
- Présentation de SACRA
- Les premières étapes à suivre
- Lien vers le site

**Important :** L'envoi d'email est **non-bloquant**. Si l'email échoue, l'inscription fonctionne quand même.

---

## ⚙️ Configuration SMTP

### Option 1 : Gmail (Recommandé pour tester)

1. **Créer un mot de passe d'application Google**
   - Va sur https://myaccount.google.com/security
   - Active l'authentification à 2 facteurs si ce n'est pas déjà fait
   - Va dans "Mots de passe d'application"
   - Génère un mot de passe pour "Mail" / "Autre"
   - **Copie ce mot de passe** (16 caractères)

2. **Ajouter dans le fichier `.env` sur le serveur :**

```bash
# Configuration Email (Gmail)
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USERNAME=ton-email@gmail.com
MAIL_PASSWORD=xxxx xxxx xxxx xxxx
MAIL_DEFAULT_SENDER=noreply@saccra.fr
```

### Option 2 : o2switch Mail

Si tu as un compte email via o2switch :

```bash
# Configuration Email (o2switch)
MAIL_SERVER=mail.o2switch.net
MAIL_PORT=587
MAIL_USERNAME=noreply@saccra.fr
MAIL_PASSWORD=ton_mot_de_passe_email
MAIL_DEFAULT_SENDER=noreply@saccra.fr
```

### Option 3 : SendGrid (Production recommandé)

Pour un service professionnel :

1. Crée un compte sur https://sendgrid.com (Gratuit : 100 emails/jour)
2. Génère une clé API
3. Configure :

```bash
# Configuration Email (SendGrid)
MAIL_SERVER=smtp.sendgrid.net
MAIL_PORT=587
MAIL_USERNAME=apikey
MAIL_PASSWORD=ta_cle_api_sendgrid
MAIL_DEFAULT_SENDER=noreply@saccra.fr
```

---

## 📝 Configuration sur le Serveur

### Étape 1 : Éditer le fichier .env

```bash
ssh wrbh3411@ssh.o2switch.net

cd ~/saccra.fr
nano .env
```

### Étape 2 : Ajouter les variables SMTP

Ajoute ces lignes à la fin du fichier `.env` :

```bash
# Configuration SMTP
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USERNAME=ton-email@gmail.com
MAIL_PASSWORD=xxxx xxxx xxxx xxxx
MAIL_DEFAULT_SENDER=noreply@saccra.fr
```

**Remplace** `ton-email@gmail.com` et `xxxx xxxx xxxx xxxx` par tes vraies valeurs.

### Étape 3 : Sauvegarder et redémarrer

```bash
# Sauvegarder (Ctrl+O puis Entrée, puis Ctrl+X)

# Redémarrer l'application
pkill -9 -u wrbh3411 python
sleep 3
touch tmp/restart.txt
```

---

## ✅ Tester l'Envoi d'Email

### Test 1 : Créer un nouveau compte

1. Va sur https://saccra.fr/auth/register
2. Inscris-toi avec une adresse email valide
3. Vérifie ta boîte mail (et spam)

### Test 2 : Vérifier les logs

```bash
ssh wrbh3411@ssh.o2switch.net

cd ~/saccra.fr
tail -f tmp/error.log
```

Tu devrais voir :
- `Email de bienvenue envoyé à user@example.com` si ça fonctionne
- `SMTP non configuré` si les variables ne sont pas définies
- `Erreur lors de l'envoi` si il y a un problème

---

## 🔧 Dépannage

### L'email n'est pas reçu

**Vérifie :**
1. Les variables SMTP sont bien dans `.env`
2. Le mot de passe est correct (pas d'espaces)
3. Le port est 587 (pas 465)
4. L'email n'est pas dans les spams
5. Gmail : Vérifie que le mot de passe d'application est actif

**Commande de vérification :**

```bash
cd ~/saccra.fr
source venv/bin/activate
python3 << 'EOF'
import os
from dotenv import load_dotenv

load_dotenv()

print("MAIL_SERVER:", os.environ.get('MAIL_SERVER', 'NON DÉFINI'))
print("MAIL_PORT:", os.environ.get('MAIL_PORT', 'NON DÉFINI'))
print("MAIL_USERNAME:", os.environ.get('MAIL_USERNAME', 'NON DÉFINI'))
print("MAIL_PASSWORD:", '***' if os.environ.get('MAIL_PASSWORD') else 'NON DÉFINI')
EOF
```

### Erreur "Authentication failed"

- Gmail : Utilise un mot de passe d'application (pas ton mot de passe normal)
- Vérifie que l'email et le mot de passe sont corrects
- Essaie de te connecter manuellement avec ces identifiants

### Erreur "Connection refused"

- Vérifie le port (587 ou 465)
- Certains hébergeurs bloquent le port 25
- Essaie avec `MAIL_PORT=465` et SSL

---

## 📊 Limites d'Envoi

| Service | Limite Gratuite | Prix |
|---------|----------------|------|
| Gmail | 500/jour | Gratuit |
| SendGrid | 100/jour | Gratuit, puis payant |
| o2switch | Illimité | Inclus dans l'hébergement |
| Mailgun | 5000/mois | Gratuit, puis payant |

---

## 🎨 Personnaliser l'Email

Le template d'email se trouve dans :
`app/services/email_service.py`

Tu peux modifier :
- Le contenu HTML
- Le style CSS
- Le texte
- Les images (avec des URLs publiques)

**Après modification :**

```bash
git add app/services/email_service.py
git commit -m "Personnalisation email de bienvenue"
git push

# Sur le serveur
cd ~/saccra.fr
git pull
pkill -9 -u wrbh3411 python && touch tmp/restart.txt
```

---

## 📧 Ajouter d'Autres Types d'Emails

Tu peux créer d'autres fonctions dans `email_service.py` :

**Exemples :**
- `send_password_reset_email()` - Réinitialisation mot de passe
- `send_premium_confirmation()` - Confirmation abonnement Premium
- `send_monthly_summary()` - Récapitulatif mensuel
- `send_interpretation_ready()` - Notification quand l'interprétation est prête

---

## 🔒 Sécurité

**Bonnes pratiques :**

1. ✅ **Ne JAMAIS** commiter le `.env` sur GitHub
2. ✅ Utiliser des mots de passe d'application (pas le mot de passe principal)
3. ✅ Limiter les permissions de l'email (seulement envoi)
4. ✅ Utiliser un email dédié (`noreply@saccra.fr`)
5. ✅ Surveiller les logs d'envoi

---

## 📞 Support

**Problèmes courants :**

1. **"SMTP non configuré"** → Ajoute les variables dans `.env`
2. **"Authentication failed"** → Mot de passe d'application Gmail
3. **Emails dans spam** → Configure SPF/DKIM (o2switch peut t'aider)
4. **Emails non reçus** → Vérifie les logs serveur

**Besoin d'aide ?**
- Documentation Gmail : https://support.google.com/mail/answer/185833
- Documentation o2switch : https://www.o2switch.fr/support
- SendGrid : https://docs.sendgrid.com

---

**Créé le :** 2025-01-26
**Version :** 1.0

# Mise à jour Configuration SMTP o2switch 📧

## ⚠️ ACTION REQUISE

Tu dois mettre à jour le fichier `.env` sur le serveur de production avec les bonnes informations SMTP o2switch.

## Configuration SMTP o2switch ✅

```bash
# Serveur SMTP o2switch - SSL (port 465)
MAIL_SERVER=mail.saccra.fr
MAIL_PORT=465
MAIL_USERNAME=contact@saccra.fr
MAIL_PASSWORD=ton-mot-de-passe-email-ici
MAIL_DEFAULT_SENDER=contact@saccra.fr
ADMIN_EMAIL=contact@saccra.fr
```

## Comment mettre à jour sur le serveur

### Étape 1 : Connexion SSH

```bash
ssh ton-user@ton-serveur-o2switch.ovh
```

### Étape 2 : Éditer le fichier .env

```bash
cd ~/saccra.fr
nano .env
```

Ou avec vi :

```bash
vi .env
```

### Étape 3 : Modifier les lignes MAIL_*

Remplace :

```bash
# Anciennes valeurs (Gmail)
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USERNAME=test@sacra.fr
```

Par :

```bash
# Nouvelles valeurs (o2switch)
MAIL_SERVER=mail.saccra.fr
MAIL_PORT=465
MAIL_USERNAME=contact@saccra.fr
MAIL_PASSWORD=ton-vrai-mot-de-passe
MAIL_DEFAULT_SENDER=contact@saccra.fr
ADMIN_EMAIL=contact@saccra.fr
```

**⚠️ Important** : Remplace `ton-vrai-mot-de-passe` par le vrai mot de passe du compte email `contact@saccra.fr`

### Étape 4 : Sauvegarder

- Avec nano : `Ctrl+X` puis `Y` puis `Enter`
- Avec vi : `Esc` puis `:wq` puis `Enter`

### Étape 5 : Redémarrer l'application

```bash
touch tmp/restart.txt
```

Ou :

```bash
./deploy.sh
```

## Vérification de la configuration

### Depuis le serveur

```bash
cd ~/saccra.fr
grep MAIL_ .env
```

Tu devrais voir :

```
MAIL_SERVER=mail.saccra.fr
MAIL_PORT=465
MAIL_USERNAME=contact@saccra.fr
MAIL_PASSWORD=***
MAIL_DEFAULT_SENDER=contact@saccra.fr
```

## Pourquoi cette modification ?

**Avant** :
- Serveur : smtp.gmail.com (Gmail)
- Port : 587 (TLS)
- ❌ Ne fonctionnait pas car credentials Gmail incorrects

**Après** :
- Serveur : mail.saccra.fr (o2switch)
- Port : 465 (SSL)
- ✅ Utilise ton propre serveur email o2switch

## Différences techniques

### Port 465 (SSL) - o2switch
```python
# Connexion SSL directe
with smtplib.SMTP_SSL('mail.saccra.fr', 465) as server:
    server.login('contact@saccra.fr', password)
    server.send_message(message)
```

### Port 587 (TLS) - Gmail
```python
# Connexion TLS avec STARTTLS
with smtplib.SMTP('smtp.gmail.com', 587) as server:
    server.starttls()
    server.login(user, password)
    server.send_message(message)
```

**✅ Le code supporte les deux** : `email_service.py` détecte automatiquement le port et utilise la bonne méthode.

## Test après modification

### Option 1 : Via l'interface web

1. Va sur **https://saccra.fr/admin/emails**
2. Ajoute-toi comme contact via "Ajouter un contact"
3. Crée une campagne de test
4. Clique "Envoyer"
5. Vérifie ta boîte email

### Option 2 : Script Python direct

```bash
cd ~/saccra.fr
python3 << 'EOF'
from app.services.email_service import send_welcome_email
result = send_welcome_email('contact@saccra.fr', 'Test')
print('✅ Email envoyé!' if result else '❌ Échec')
EOF
```

## Problèmes potentiels

### ❌ "Authentication failed"

**Cause** : Mot de passe incorrect

**Solution** :
1. Vérifie le mot de passe dans cPanel o2switch
2. Teste la connexion avec un client email (Thunderbird, Outlook)
3. Si ça marche, copie exactement le même mot de passe dans `.env`

### ❌ "Connection refused"

**Cause** : Firewall ou port bloqué

**Solution** :
1. Vérifie que le port 465 est ouvert sur o2switch
2. Teste depuis le terminal : `telnet mail.saccra.fr 465`
3. Contact le support o2switch si nécessaire

### ❌ "SSL certificate error"

**Cause** : Certificat SSL invalide

**Solution** :
1. Vérifie que le domaine `mail.saccra.fr` est bien configuré
2. Teste avec : `openssl s_client -connect mail.saccra.fr:465`

## Avantages du serveur o2switch

✅ **Fiabilité** : Serveur email dédié pour ton domaine
✅ **Délivrabilité** : Meilleure réputation (pas de Gmail partagé)
✅ **SPF/DKIM** : Configuration DNS automatique par o2switch
✅ **Limites** : Généralement plus généreuses que Gmail (varie selon l'offre)
✅ **Contrôle** : Tu gères tout depuis cPanel

## Limites d'envoi o2switch

**Important** : Vérifie les limites de ton hébergement o2switch.

Généralement :
- **Offre Start** : ~100-500 emails/heure
- **Offre Perso** : ~500-1000 emails/heure
- **Offre Pro** : ~1000-2000 emails/heure

**Pour 55K contacts** :
- À 500 emails/heure = ~110 heures = ~4.5 jours
- À 1000 emails/heure = ~55 heures = ~2.3 jours

💡 **Solution** : Utiliser le script d'envoi automatique par batch que je peux créer !

## Prochaine étape

Une fois la configuration SMTP mise à jour :

1. ✅ Teste avec 1 email (toi-même)
2. ✅ Si ça marche, teste avec 10 emails
3. ✅ Si ça marche, je crée le système d'envoi automatique pour les 55K

**Veux-tu que je crée le script d'envoi automatique par batch maintenant ?**

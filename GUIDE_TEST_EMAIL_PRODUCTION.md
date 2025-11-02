# Guide de Test Email Marketing - Production 📧

## Statut actuel ✅

- ✅ 55 000 contacts importés sur production
- ✅ Système d'email marketing complet installé
- ✅ Configuration SMTP présente
- ⏳ Test d'envoi à faire sur production

## Comment tester l'envoi d'emails sur production

### Étape 1 : Déployer le code

```bash
# Via SSH sur o2switch
cd ~/saccra.fr
git pull origin claude/sacra-mvp-development-011CUhLGumEoVuANcbz2osHe
touch tmp/restart.txt
```

### Étape 2 : Créer une campagne de test

1. Va sur **https://saccra.fr/admin/emails**
2. Clique sur **"Nouvelle Campagne"**
3. Remplis le formulaire :
   - **Nom** : Test Envoi Email
   - **Type** : Newsletter (ou Test)
   - **Sujet** : 🧪 Test - Email Marketing SACRA
   - **Contenu** : Utilise le template ci-dessous
   - **Actif** : ✅ Coché

#### Template de test recommandé :

```html
<html>
<body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px;">
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; text-align: center; border-radius: 10px;">
        <h1>🧪 Test Email Marketing</h1>
    </div>

    <div style="background: #f9f9f9; padding: 30px; margin-top: 20px; border-radius: 10px;">
        <p>Bonjour {{first_name}},</p>

        <p>Ceci est un <strong>email de test</strong> pour vérifier que le système d'email marketing fonctionne.</p>

        <h3>✅ Si tu reçois cet email :</h3>
        <ul>
            <li>Configuration SMTP ✅</li>
            <li>Import CSV (55K contacts) ✅</li>
            <li>Envoi d'emails ✅</li>
            <li>Personnalisation ✅</li>
        </ul>

        <p>Ton email: <strong>{{email}}</strong></p>
    </div>

    <div style="text-align: center; margin-top: 30px; color: #999; font-size: 12px;">
        <p>SACRA - Email Marketing</p>
    </div>
</body>
</html>
```

### Étape 3 : Envoyer à un contact de test

**Option A : Ajoute-toi comme contact de test**

1. Va sur **https://saccra.fr/admin/emails/contacts/new**
2. Ajoute ton email personnel
3. Sauvegarde

**Option B : Utilise un contact existant**

1. Va sur **https://saccra.fr/admin/emails/contacts**
2. Vérifie qu'il y a au moins 1 contact abonné

### Étape 4 : Envoyer la campagne

1. Va sur **https://saccra.fr/admin/emails/campaigns**
2. Trouve ta campagne de test
3. Clique sur **"📨 Envoyer"**
4. Confirme l'envoi

**⚠️ Important** : L'envoi est limité à **100 emails maximum** par clic pour éviter de surcharger le serveur SMTP.

### Étape 5 : Vérifier la réception

1. Vérifie ta boîte email
2. Vérifie les dossiers :
   - Boîte de réception
   - Spam/Indésirables
   - Promotions (Gmail)

3. Vérifie que :
   - ✅ L'email est reçu
   - ✅ Le sujet est correct
   - ✅ Le HTML s'affiche bien
   - ✅ Les variables {{first_name}} et {{email}} sont remplacées

### Étape 6 : Vérifier les statistiques

1. Retourne sur **https://saccra.fr/admin/emails**
2. Regarde le dashboard :
   - Emails envoyés
   - Taux d'ouverture (si tracking activé)

## Problèmes courants et solutions

### ❌ "Aucun contact abonné"

**Solution** : Ajoute au moins un contact via :
- https://saccra.fr/admin/emails/contacts/new

### ❌ "SMTP non configuré"

**Solution** : Vérifie le fichier `.env` sur le serveur :
```bash
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USERNAME=ton-email@gmail.com
MAIL_PASSWORD=ton-mot-de-passe-app
MAIL_DEFAULT_SENDER=noreply@saccra.fr
```

### ❌ Email non reçu

**Vérifications** :
1. Vérifie les spams
2. Vérifie que le contact est "abonné" (pas désabonné)
3. Vérifie les logs sur le serveur : `tail -f logs/app.log`

### ⚠️ Limite de 100 emails par envoi

**Pourquoi ?** : Pour éviter de surcharger le serveur SMTP et être bloqué pour spam.

**Solution pour 55K contacts** : Il y a 3 options :

**Option 1 - Manuel** : Cliquer 550 fois sur "Envoyer" (pas pratique)

**Option 2 - Script d'envoi par batch** : Je peux créer un script qui envoie automatiquement par lots de 100 avec un délai entre chaque batch

**Option 3 - Celery (recommandé)** : Utiliser Celery pour envoyer en arrière-plan de manière asynchrone

## Test réussi ? ✅

Si tu as reçu l'email de test, ton système est **100% fonctionnel** !

Tu peux maintenant :
1. ✅ Créer des campagnes professionnelles
2. ✅ Envoyer à tes 55K contacts
3. ✅ Tracker les stats (envois, ouvertures)

## Prochaines étapes recommandées

### 1. Améliorer l'envoi en masse (IMPORTANT)

Pour envoyer à 55K contacts efficacement :

```python
# Je peux créer un script d'envoi automatique par batch
# Qui envoie 100 emails toutes les 5 minutes
# Soit 1200 emails/heure = ~46 heures pour 55K
```

**Veux-tu que je crée ce système ?**

### 2. Tracking des ouvertures (optionnel)

Ajouter un pixel de tracking pour savoir qui ouvre les emails :

```html
<img src="https://saccra.fr/api/track/open/{{log_id}}" width="1" height="1" />
```

### 3. Lien de désabonnement (RGPD)

Ajouter un lien de désabonnement dans chaque email :

```html
<a href="https://saccra.fr/unsubscribe/{{email}}">Se désabonner</a>
```

## Support

Si tu rencontres des problèmes :
1. Vérifie les logs : `tail -f logs/app.log`
2. Vérifie la config SMTP dans `.env`
3. Teste avec 1 seul email d'abord
4. Demande-moi de l'aide !

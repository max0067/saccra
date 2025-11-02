# Guide d'Envoi en Masse - 55K Contacts 📧

## ✅ Prérequis

- [x] 55 000 contacts importés
- [x] SMTP localhost:25 fonctionnel
- [x] Campagne créée et prête

## 🚀 Envoi Automatique par Batch

### Étape 1 : Créer ta campagne

1. Va sur **https://saccra.fr/admin/emails/campaigns**
2. Clique **"✨ Nouvelle Campagne"**
3. Remplis :
   - **Nom** : Ma Newsletter Février 2025
   - **Type** : Newsletter
   - **Sujet** : Découvre les nouveautés spirituelles 🌟
   - **Contenu** : Ton message HTML (utilise `{{first_name}}` et `{{email}}`)
   - **Actif** : ✅ Coché
4. Note l'**ID de la campagne** (visible dans l'URL ou la liste)

### Étape 2 : Exécuter le script d'envoi

```bash
cd ~/saccra.fr

# Active le venv si nécessaire
source venv/bin/activate

# Envoi standard (100 emails/minute)
python3 send_campaign_batch.py <CAMPAIGN_ID>
```

**Exemple** : Si ta campagne a l'ID 1
```bash
python3 send_campaign_batch.py 1
```

Le script va :
- Afficher les infos de la campagne
- Compter les contacts
- Estimer le temps total
- Demander confirmation
- Envoyer par lots de 100 avec pause de 60s

### Étape 3 : Surveiller la progression

Le script affiche en temps réel :
```
[Batch 1/550] Envoi de 100 emails...
   ✅ Envoyés: 100
   📊 Total: 100/55000 (1%)
   ⏳ Attente de 60s avant le prochain batch...
```

## ⚙️ Options Avancées

### Envoi Rapide (500 emails / 5 minutes)

```bash
python3 send_campaign_batch.py 1 --batch-size 500 --delay 300
```

**Temps estimé** : ~5.5 heures pour 55K

### Envoi Test (10 emails)

```bash
python3 send_campaign_batch.py 1 --batch-size 10 --max-total 10
```

Parfait pour tester avant l'envoi massif !

### Reprendre un Envoi Interrompu

Si tu arrêtes l'envoi (Ctrl+C) ou s'il y a une coupure :

```bash
python3 send_campaign_batch.py 1 --resume
```

Le script reprend exactement où il s'était arrêté ! ✨

## 📊 Scénarios d'Envoi

### Scénario 1 : Prudent (100/min)
```bash
python3 send_campaign_batch.py 1
```
- **Batch** : 100 emails
- **Délai** : 60 secondes
- **Vitesse** : 100 emails/minute
- **Temps** : ~9 heures pour 55K
- **Idéal** : Premier envoi, limites serveur strictes

### Scénario 2 : Standard (300/3min)
```bash
python3 send_campaign_batch.py 1 --batch-size 300 --delay 180
```
- **Batch** : 300 emails
- **Délai** : 3 minutes
- **Vitesse** : 100 emails/minute
- **Temps** : ~9 heures pour 55K
- **Idéal** : Équilibre performance/sécurité

### Scénario 3 : Rapide (500/5min)
```bash
python3 send_campaign_batch.py 1 --batch-size 500 --delay 300
```
- **Batch** : 500 emails
- **Délai** : 5 minutes
- **Vitesse** : 100 emails/minute
- **Temps** : ~9 heures pour 55K
- **Idéal** : Si tu connais les limites de ton serveur

### Scénario 4 : Très Rapide (1000/5min)
```bash
python3 send_campaign_batch.py 1 --batch-size 1000 --delay 300
```
- **Batch** : 1000 emails
- **Délai** : 5 minutes
- **Vitesse** : 200 emails/minute
- **Temps** : ~4.5 heures pour 55K
- **Idéal** : Serveur puissant, limites élevées
- **⚠️ Attention** : Risque de blocage si limites dépassées

## 🛑 Arrêter l'Envoi

Pour arrêter proprement l'envoi en cours :
- Appuie sur **Ctrl+C**
- Le script sauvegarde la progression
- Tu peux reprendre plus tard avec `--resume`

## 📝 Fichiers Générés

### campaign_progress.json
Sauvegarde automatique de la progression :
```json
{
  "campaign_id": 1,
  "sent_count": 5000,
  "failed_count": 12,
  "last_contact_id": 5012,
  "timestamp": "2025-02-15T14:30:00"
}
```

Ce fichier permet de reprendre l'envoi exactement où il s'est arrêté.

## 🔍 Vérifier les Résultats

### Via l'interface web

1. Va sur **https://saccra.fr/admin/emails**
2. Regarde le dashboard :
   - Total emails envoyés
   - Taux d'ouverture
   - Statistiques par campagne

### Via la base de données

```bash
python3 << 'EOF'
from app import create_app
from app.models import EmailLog, EmailCampaign

app = create_app()
with app.app_context():
    campaign_id = 1
    campaign = EmailCampaign.query.get(campaign_id)
    logs = EmailLog.query.filter_by(campaign_id=campaign_id).all()

    print(f"Campagne: {campaign.name}")
    print(f"Total envoyés: {len(logs)}")
    print(f"Taux de succès: {campaign.total_sent}")
EOF
```

## ⚠️ Limites o2switch

Vérifie les limites de ton hébergement o2switch avant l'envoi massif.

**Limites typiques** :
- **Start** : ~100-500 emails/heure
- **Perso** : ~500-1000 emails/heure
- **Pro** : ~1000-2000 emails/heure

**Comment savoir** :
1. Contacte le support o2switch
2. Vérifie dans cPanel → "Email" → "Limites"
3. Teste avec un petit batch d'abord

**Si tu dépasses les limites** :
- Le serveur peut bloquer temporairement (30min - 24h)
- Les emails sont rejetés avec erreur "quota exceeded"
- Ajuste `--batch-size` et `--delay` en conséquence

## 🎯 Recommandation pour 55K

Pour le premier envoi massif, je recommande :

```bash
# Test avec 100 emails d'abord
python3 send_campaign_batch.py 1 --batch-size 10 --max-total 100

# Si tout va bien, lance l'envoi complet
python3 send_campaign_batch.py 1 --batch-size 500 --delay 300
```

**Avantages** :
- Teste avant l'envoi complet
- Vérifie la délivrabilité
- Détecte les erreurs tôt
- Ajuste si nécessaire

## 💡 Conseils Pro

### 1. Lance l'envoi en arrière-plan

Pour que l'envoi continue même si tu fermes le terminal :

```bash
nohup python3 send_campaign_batch.py 1 --batch-size 500 --delay 300 > campaign.log 2>&1 &
```

Vérifie la progression :
```bash
tail -f campaign.log
```

### 2. Lance pendant la nuit

55K emails = 9 heures. Lance-le le soir avant de partir :
```bash
# À 22h, démarre l'envoi
python3 send_campaign_batch.py 1 --batch-size 500 --delay 300
```

Il sera terminé le lendemain matin ! 🌅

### 3. Surveille les bounces

Après l'envoi, vérifie les emails bounced :
```bash
python3 << 'EOF'
from app import create_app
from app.models import EmailLog

app = create_app()
with app.app_context():
    bounced = EmailLog.query.filter_by(status='bounced').all()
    print(f"Bounced: {len(bounced)}")
    for log in bounced[:10]:
        print(f"  - {log.email_to}: {log.error_message}")
EOF
```

### 4. Teste la délivrabilité

Avant l'envoi massif :
- Envoie à toi-même
- Vérifie les spams
- Teste sur Gmail, Outlook, Yahoo
- Assure-toi que le HTML s'affiche bien

## 🆘 Problèmes Fréquents

### "Authentication failed"
- ✅ **Résolu** : localhost:25 ne nécessite pas d'auth

### "Quota exceeded"
- Tu dépasses les limites o2switch
- Réduis `--batch-size` ou augmente `--delay`

### "Connection refused"
- Le serveur SMTP est indisponible
- Vérifie : `telnet localhost 25`
- Contacte le support o2switch

### Emails en spam
- Configure SPF/DKIM dans cPanel
- Évite les mots comme "GRATUIT", "URGENT"
- Ajoute un lien de désabonnement
- N'envoie pas tout d'un coup (utilise des batch)

## ✅ Checklist Avant Envoi

- [ ] Campagne créée et testée
- [ ] Contenu HTML vérifié
- [ ] Variables `{{first_name}}` et `{{email}}` utilisées
- [ ] Test envoyé à toi-même et reçu
- [ ] Email bien affiché (pas en spam)
- [ ] ID de la campagne noté
- [ ] Limites o2switch vérifiées
- [ ] Script testé avec `--max-total 10`
- [ ] Prêt à surveiller la progression

## 🎉 Après l'Envoi

1. ✅ Vérifie les stats sur https://saccra.fr/admin/emails
2. 📊 Analyse le taux d'ouverture (après 24-48h)
3. 🔍 Vérifie les bounces et désinscriptions
4. 📝 Note ce qui a bien fonctionné
5. 🚀 Prépare ta prochaine campagne !

---

**Questions ?** Demande-moi de t'aider ! 💬

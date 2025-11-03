# 🛡️ Guide Anti-Spam - SACRA Email Marketing

Ce guide te montre comment **éviter que tes emails finissent dans les spams** et **maintenir une bonne réputation d'expéditeur**.

---

## 📋 Checklist Rapide

Avant d'envoyer une campagne massive, vérifie :

- [ ] ✅ Footer avec désinscription (ajouté automatiquement)
- [ ] ✅ Configuration DNS (SPF, DKIM, DMARC)
- [ ] ✅ Warm-up progressif (10 jours minimum)
- [ ] ✅ Score spam < 40 (utilise `check_spam_score.py`)
- [ ] ✅ Email de test envoyé et reçu (pas dans spam)
- [ ] ✅ Liste nettoyée (pas de bounces)

---

## 🔧 1. Configuration DNS (CRITIQUE)

### Pourquoi ?
Les serveurs email vérifient que tu es bien autorisé à envoyer des emails depuis ton domaine.

### Comment configurer ?

Va dans **cPanel o2switch → Zone DNS** :

#### SPF Record
```
Type: TXT
Nom: @
Valeur: v=spf1 a mx include:_spf.o2switch.net ~all
TTL: 14400
```

#### DKIM (DomainKeys)
1. Va dans **cPanel → Email Deliverability**
2. Clique sur **Manage** à côté de ton domaine
3. Active DKIM si ce n'est pas déjà fait
4. Copie la clé publique générée

#### DMARC
```
Type: TXT
Nom: _dmarc
Valeur: v=DMARC1; p=quarantine; rua=mailto:contact@saccra.fr
TTL: 14400
```

### Vérifier la configuration

Après avoir ajouté les DNS, attends 24h puis vérifie sur :
- https://mxtoolbox.com/spf.aspx
- https://mxtoolbox.com/dkim.aspx
- https://mxtoolbox.com/dmarc.aspx

---

## 🚀 2. Warm-up Progressif (10-14 jours)

### Pourquoi ?
Envoyer 55K emails d'un coup depuis une nouvelle IP = **SPAM ASSURÉ**.

Les fournisseurs d'email (Gmail, Outlook, etc.) te considèrent comme spam si tu passes de 0 à 55K en un jour.

### Comment faire ?

Utilise le **script de warm-up automatique** :

```bash
# Jour 1
python3 warmup_campaign.py 1

# Jour 2 (lendemain)
python3 warmup_campaign.py 1

# Jour 3 (lendemain)
python3 warmup_campaign.py 1

# etc... pendant 10-14 jours
```

### Plan de warm-up

| Jour | Emails/jour | Cumulé |
|------|-------------|---------|
| 1-2  | 500         | 1,000   |
| 3-4  | 1,000       | 3,000   |
| 5-6  | 2,000       | 7,000   |
| 7-8  | 5,000       | 17,000  |
| 9-10 | 10,000      | 37,000  |
| 11+  | Volume complet | 55,000+ |

### Conseils
- Lance le script **une fois par jour** à la même heure
- Surveille le taux d'ouverture (doit rester > 10%)
- Si taux d'ouverture chute, **STOP** et attends 2 jours
- Nettoie les bounces après chaque envoi

---

## 📊 3. Vérifier le Score Spam

Avant CHAQUE campagne, vérifie ton score :

```bash
python3 check_spam_score.py 1
```

### Résultats

| Score | Risque | Action |
|-------|--------|--------|
| 0-20  | ✅ Faible | Prêt à envoyer |
| 21-40 | ⚠️ Modéré | Améliorations recommandées |
| 41-60 | ⚠️ Élevé | Corrections requises |
| 61+   | ❌ Très élevé | NE PAS ENVOYER |

### Corrections rapides

**Si ton score est élevé :**

1. **Retire les mots spam** :
   - ❌ URGENT, GRATUIT, ARGENT, CLIQUEZ ICI
   - ✅ Remplace par des termes neutres

2. **Ajoute plus de texte** :
   - Ratio idéal : 60% texte / 40% images
   - Minimum 500 caractères

3. **Retire les majuscules excessives** :
   - ❌ CECI EST IMPORTANT !!!
   - ✅ Ceci est important.

4. **Ajoute des attributs alt aux images** :
   ```html
   <img src="photo.jpg" alt="Description de l'image">
   ```

---

## 📧 4. Email de Test

**TOUJOURS** envoie un test avant l'envoi massif :

1. Va sur la page des campagnes
2. Clique sur **"📧 Email de Test"**
3. Entre ton email (défaut: maxenko06@gmail.com)
4. Vérifie :
   - ✅ Reçu dans la boîte de réception (pas spam)
   - ✅ Images affichées correctement
   - ✅ Liens fonctionnels
   - ✅ Footer de désinscription présent
   - ✅ Rendu correct sur mobile

Si l'email arrive en spam :
- Vérifie ton score spam (`check_spam_score.py`)
- Vérifie ta config DNS (SPF/DKIM/DMARC)
- Attends 24h pour que les DNS se propagent

---

## 🧹 5. Nettoyer ta Liste

### Bounces (emails invalides)

Après chaque envoi, retire les emails qui rebondissent :

```python
# Dans le terminal Flask
from app.models import EmailContact, db

# Marquer les bounces
bounced_contacts = EmailContact.query.filter_by(is_bounced=True).all()
print(f"Bounces: {len(bounced_contacts)}")

# Les retirer de la liste active
for contact in bounced_contacts:
    contact.is_subscribed = False

db.session.commit()
```

### Contacts inactifs

Retire les contacts qui n'ont **jamais ouvert** en 6 mois :

```python
from datetime import datetime, timedelta

# Dans le terminal Flask
inactive_threshold = datetime.now() - timedelta(days=180)

# Cette fonctionnalité sera ajoutée prochainement
```

---

## 📈 6. Surveiller les Métriques

### Taux d'ouverture normal

| Industrie | Taux d'ouverture moyen |
|-----------|------------------------|
| Spiritualité/Bien-être | 18-25% |
| Newsletter générale | 15-20% |

**Ton taux actuel :** Visible sur le dashboard

### Signes d'alerte

🚨 **STOP l'envoi si :**
- Taux d'ouverture < 5%
- Taux de bounce > 2%
- Taux de désinscription > 0.5%

### Actions correctives

Si tes stats sont mauvaises :
1. **Vérifie ton contenu** (check_spam_score.py)
2. **Ralentis l'envoi** (réduis batch size)
3. **Nettoie ta liste** (retire bounces)
4. **Attends 48h** avant de réessayer

---

## 🎯 7. Bonnes Pratiques

### ✅ À FAIRE

- Personnalise avec `{{first_name}}`
- Utilise un sujet clair et honnête
- Envoie du contenu de valeur
- Respecte la fréquence (max 2-3 emails/semaine)
- Segmente ta liste (prochainement disponible)
- Réponds aux emails (active l'adresse contact@saccra.fr)

### ❌ À ÉVITER

- Acheter des listes d'emails (illégal)
- Envoyer sans opt-in (illégal RGPD)
- Mentir dans le sujet
- Masquer le lien de désinscription
- Envoyer trop fréquemment (spam)
- Ignorer les désinscriptions

---

## 🛠️ 8. Outils Disponibles

### Scripts

```bash
# Vérifier le score spam
python3 check_spam_score.py <campaign_id>

# Warm-up progressif
python3 warmup_campaign.py <campaign_id>

# Envoi par batch (après warm-up)
python3 send_campaign_batch.py <campaign_id> --batch-size 500 --delay 120

# Synchroniser les stats
python3 sync_campaign_stats.py
```

### Interface Web

- **📧 Email de Test** : Teste le rendu avant envoi
- **🚀 Envoi par Batch** : Envoi massif avec contrôle
- **📊 Dashboard** : Stats en temps réel

---

## 🆘 Résolution de Problèmes

### Mes emails vont en spam

1. Vérifie ton score : `python3 check_spam_score.py 1`
2. Vérifie DNS : https://mxtoolbox.com/spf.aspx
3. Réduis le volume (warm-up)
4. Améliore le contenu (moins de mots spam)
5. Attends 48h entre les envois

### Taux d'ouverture très faible

- Vérifie le sujet (doit être engageant)
- Envoie aux heures optimales (10h-11h, 14h-15h)
- Nettoie ta liste (retire inactifs)
- Segmente (envoie aux plus engagés d'abord)

### Beaucoup de désinscriptions

- Contenu pas pertinent → Améliore
- Trop d'envois → Réduis la fréquence
- Sujet trompeur → Sois honnête
- Pas de valeur → Apporte de la valeur

---

## 📚 Ressources

- [Guide RGPD Email Marketing](https://www.cnil.fr/fr/la-prospection-commerciale-par-courrier-electronique)
- [Tester ton email](https://www.mail-tester.com/)
- [Vérifier SPF/DKIM](https://mxtoolbox.com/)

---

## ✅ Workflow Recommandé

**Pour une nouvelle campagne :**

1. Crée ta campagne dans l'interface
2. `python3 check_spam_score.py 1` → Corrige si > 40
3. Clique sur "📧 Email de Test" → Vérifie la réception
4. **JOUR 1** : `python3 warmup_campaign.py 1` (500 emails)
5. **JOUR 2** : `python3 warmup_campaign.py 1` (500 emails)
6. **JOUR 3** : `python3 warmup_campaign.py 1` (1000 emails)
7. Continue pendant 10 jours
8. **APRÈS WARM-UP** : Utilise "🚀 Envoi par Batch" dans l'interface

**Temps total : 10-14 jours pour 55K contacts**

C'est long, mais **ESSENTIEL** pour éviter le spam ! 🎯

---

*Guide créé pour SACRA Email Marketing - © 2025*

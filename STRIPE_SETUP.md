# 💳 Configuration Stripe pour SACCRA

## Étape 1: Créer un compte Stripe

1. Va sur https://dashboard.stripe.com/register
2. Crée ton compte Stripe
3. Active le mode Test pour commencer

## Étape 2: Créer les produits et prix

### Dans le Dashboard Stripe (mode Test):

1. **Va dans "Produits" → "Ajouter un produit"**

2. **Créer le produit SACCRA Premium:**
   - Nom: `SACCRA Premium`
   - Description: `Abonnement premium avec interprétations illimitées`

3. **Ajouter le prix mensuel:**
   - Modèle de tarification: `Récurrent`
   - Prix: `9.99 EUR`
   - Période de facturation: `Mensuel`
   - Copie le **Price ID** (commence par `price_xxx`)

4. **Ajouter le prix annuel (optionnel):**
   - Clique sur "Ajouter un autre prix"
   - Prix: `99.99 EUR` (ou ton prix annuel)
   - Période de facturation: `Annuel`
   - Copie le **Price ID**

## Étape 3: Récupérer les clés API

### Clés API (mode Test):

1. Va dans **Développeurs → Clés API**
2. Copie:
   - **Clé publique** (pk_test_xxx)
   - **Clé secrète** (sk_test_xxx) ⚠️ Garde-la secrète!

### Créer le webhook:

1. Va dans **Développeurs → Webhooks**
2. Clique sur **Ajouter un point de terminaison**
3. URL du point de terminaison: `https://saccra.fr/premium/webhook`
4. Sélectionne ces événements:
   - `checkout.session.completed`
   - `invoice.payment_succeeded`
   - `invoice.payment_failed`
   - `customer.subscription.deleted`
   - `customer.subscription.updated`
5. **Ajouter le point de terminaison**
6. Copie le **Secret de signature** (whsec_xxx)

## Étape 4: Configurer le .env sur le serveur

```bash
# Sur le serveur o2switch
ssh wrbh3411@ssh.o2switch.net
cd ~/saccra.fr
nano .env
```

Ajoute ces lignes dans `.env`:

```bash
# Stripe (mode TEST - à remplacer en production)
STRIPE_PUBLIC_KEY=pk_test_XXXXXXXXXXXXXXXXXXXXX
STRIPE_SECRET_KEY=sk_test_XXXXXXXXXXXXXXXXXXXXX
STRIPE_MONTHLY_PRICE_ID=price_XXXXXXXXXXXXX
STRIPE_YEARLY_PRICE_ID=price_XXXXXXXXXXXXX
STRIPE_WEBHOOK_SECRET=whsec_XXXXXXXXXXXXX
```

Sauvegarde avec `Ctrl+X`, `Y`, `Enter`

## Étape 5: Tester le paiement

```bash
# Redémarrer Passenger pour charger les nouvelles variables
pkill -9 -u wrbh3411 python
sleep 3
touch tmp/restart.txt
```

### Test sur le site:

1. Va sur https://saccra.fr/premium/subscribe
2. Clique sur "Passer Premium"
3. Tu seras redirigé vers Stripe Checkout
4. Utilise une **carte de test**:
   - Numéro: `4242 4242 4242 4242`
   - Date: n'importe quelle date future
   - CVC: n'importe quel 3 chiffres
   - Nom: n'importe quel nom

5. Complète le paiement
6. Tu dois être redirigé vers ton dashboard avec un message de succès
7. Ton compte devrait être Premium!

## Étape 6: Vérifier dans Stripe

1. Va dans le Dashboard Stripe → **Paiements**
2. Tu devrais voir ton paiement test
3. Va dans **Clients** → tu devrais voir ton compte créé
4. Va dans **Abonnements** → ton abonnement devrait être actif

## Étape 7: Passer en production (quand prêt)

### ⚠️ Important: Ne fais ça que quand tu es prêt à recevoir de vrais paiements!

1. **Active ton compte Stripe:**
   - Complète les informations de ton entreprise
   - Ajoute tes coordonnées bancaires
   - Vérifie ton identité

2. **Passe en mode Live:**
   - Dans le Dashboard Stripe, toggle "Test mode" → "Live mode"
   - Récupère les nouvelles clés (pk_live_xxx et sk_live_xxx)
   - Crée les mêmes produits/prix en mode Live
   - Configure un nouveau webhook en mode Live

3. **Met à jour le .env:**
   ```bash
   # Remplace les clés test par les clés live
   STRIPE_PUBLIC_KEY=pk_live_XXXXXXXXXXXXX
   STRIPE_SECRET_KEY=sk_live_XXXXXXXXXXXXX
   STRIPE_MONTHLY_PRICE_ID=price_live_XXXXX
   STRIPE_YEARLY_PRICE_ID=price_live_XXXXX
   STRIPE_WEBHOOK_SECRET=whsec_live_XXXXX
   ```

4. **Redémarre Passenger**

## Cartes de test Stripe

Pour tester différents scénarios:

| Scénario | Numéro de carte |
|----------|----------------|
| Paiement réussi | 4242 4242 4242 4242 |
| Paiement refusé | 4000 0000 0000 0002 |
| 3D Secure requis | 4000 0027 6000 3184 |

## Troubleshooting

### "Configuration Stripe incomplète"
- Vérifie que `STRIPE_MONTHLY_PRICE_ID` est bien défini dans `.env`
- Redémarre Passenger après modification du `.env`

### Le webhook ne fonctionne pas
- Vérifie l'URL du webhook: `https://saccra.fr/premium/webhook` (sans trailing slash)
- Vérifie que `STRIPE_WEBHOOK_SECRET` est correct
- Teste le webhook depuis le Dashboard Stripe

### L'abonnement ne s'active pas
- Vérifie les logs du webhook dans Stripe
- L'activation se fait dans la page success, pas le webhook

## Fonctionnalités disponibles

✅ **Paiement par carte** (Stripe Checkout)
✅ **Abonnement mensuel**
✅ **Abonnement annuel** (optionnel)
✅ **Annulation d'abonnement**
✅ **Codes promo** (crédits ou jours premium gratuits)
✅ **Webhooks** (renouvellement automatique)
✅ **Gestion des clients Stripe**

## Prochaines étapes (optionnel)

- [ ] Ajouter Apple Pay / Google Pay
- [ ] Emails de confirmation Stripe
- [ ] Facturation automatique
- [ ] Essai gratuit de 7 jours
- [ ] Offres promotionnelles saisonnières

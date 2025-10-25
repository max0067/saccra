# 👑 Guide Admin SACRA

Ce document explique toutes les fonctionnalités du panneau d'administration de SACRA.

---

## 🎯 Fonctionnalités Ajoutées

### 1. **Dashboard Admin Complet**
- Statistiques globales de la plateforme
- Gestion des utilisateurs
- Gestion des codes promo
- Ajout de crédits aux utilisateurs

### 2. **Système de Crédits**
- Les utilisateurs peuvent avoir des crédits bonus
- Les crédits sont utilisés avant les 3 interprétations gratuites
- Les admins peuvent ajouter des crédits manuellement
- Les codes promo peuvent offrir des crédits

### 3. **Codes Promo**
- Créer des codes promo personnalisés
- 2 types de récompenses : crédits ou jours Premium
- Limites d'utilisation configurables
- Date d'expiration optionnelle
- Activation/désactivation des codes

---

## 🚀 Démarrage Rapide

### Initialiser la Base de Données

```bash
# Supprimer l'ancienne base (si elle existe)
rm -f instance/sacra.db

# Initialiser avec le compte admin
python init_admin.py
```

**Compte admin par défaut :**
- Email : `admin@sacra.fr`
- Password : `admin123`
- ⚠️ **À CHANGER EN PRODUCTION !**

**Codes promo créés automatiquement :**
- `BIENVENUE` : 5 crédits d'interprétation
- `PREMIUM7J` : 7 jours de Premium gratuit

### Lancer l'Application

```bash
# Mode développement
python app.py

# Mode production (o2switch)
touch tmp/restart.txt
```

---

## 📋 Accès au Panneau Admin

### URL : `/admin/dashboard`

Le lien **👑 Admin** apparaît automatiquement dans la navigation pour les utilisateurs avec `is_admin=True`.

---

## 🎛️ Fonctionnalités Détaillées

### A. Dashboard Admin (`/admin/dashboard`)

**Statistiques affichées :**
- Total utilisateurs
- Utilisateurs Premium vs Gratuits
- Nouveaux utilisateurs cette semaine
- Total interprétations
- Répartition par type (Rêves / Signes / Tarot)
- Codes promo actifs
- Liste des derniers utilisateurs inscrits

**Actions disponibles :**
- Voir les derniers utilisateurs
- Accéder à la gestion utilisateurs
- Accéder à la gestion codes promo

---

### B. Gestion des Utilisateurs (`/admin/users`)

**Filtres disponibles :**
- Tous les utilisateurs
- Utilisateurs Premium uniquement
- Utilisateurs Gratuits uniquement
- Administrateurs uniquement

**Recherche :**
- Par email
- Par nom

**Actions par utilisateur :**

#### 💰 Ajouter des Crédits
```
Bouton : 💰
Action : Ouvre un prompt pour entrer le nombre de crédits
Résultat : Ajoute les crédits au compte utilisateur
```

#### ✨ Toggle Premium
```
Bouton : ✨
Action : Active/désactive le Premium manuellement
Options : Choisir le nombre de jours (par défaut 30)
Résultat : Active Premium pour X jours ou le désactive
```

#### 👑 Toggle Admin
```
Bouton : 👑
Action : Promouvoir/rétrograder un utilisateur admin
Restriction : Ne peut pas modifier son propre statut
Résultat : Active/désactive les droits admin
```

#### 🗑️ Supprimer
```
Bouton : 🗑️
Action : Supprime l'utilisateur et toutes ses données
Restriction : Ne peut pas se supprimer soi-même
Confirmation : Double confirmation requise
```

**Pagination :**
- 20 utilisateurs par page
- Navigation Précédent / Suivant

---

### C. Gestion des Codes Promo (`/admin/promo-codes`)

#### Créer un Code Promo

**Champs du formulaire :**

1. **Code Promo** (requis)
   - Min 3 caractères
   - Converti automatiquement en MAJUSCULES
   - Doit être unique
   - Exemple : `BIENVENUE2024`

2. **Type de Récompense** (requis)
   - `credits` : Offre des crédits d'interprétation
   - `premium_days` : Offre des jours Premium

3. **Valeur** (requis)
   - Nombre de crédits OU nombre de jours
   - Minimum : 1
   - Exemple : 10 crédits ou 7 jours

4. **Utilisations Maximum** (optionnel)
   - Laisser vide pour illimité
   - Exemple : 100 utilisations max

5. **Expiration** (optionnel)
   - Nombre de jours avant expiration
   - Laisser vide pour jamais expirer
   - Exemple : 30 jours

6. **Description** (optionnel)
   - Note interne pour identifier le code
   - Non visible par les utilisateurs
   - Exemple : "Campagne de lancement"

**Exemple de codes :**

```
Code : BIENVENUE
Type : Crédits
Valeur : 5
Max uses : 100
Expire : 30 jours
Desc : Code de bienvenue nouveaux users
```

```
Code : PREMIUM7J
Type : Jours Premium
Valeur : 7
Max uses : 50
Expire : 30 jours
Desc : Essai Premium gratuit
```

#### Gérer les Codes Existants

**Informations affichées :**
- Code promo
- Statut (Actif/Inactif)
- Type et valeur de récompense
- Utilisations (X / Y ou ∞)
- Date d'expiration
- Date de création
- Description
- Validité (✅ Valide ou ⚠️ Invalide avec raison)

**Actions disponibles :**

1. **Activer/Désactiver**
   - Toggle le statut actif/inactif
   - Les codes inactifs ne peuvent pas être utilisés

2. **Supprimer**
   - Supprime définitivement le code
   - Confirmation requise

---

### D. Système de Crédits pour Utilisateurs

#### Où les Utilisateurs Voient leurs Crédits ?

**Dashboard utilisateur :**
- Section "🎁 Codes Promo & Crédits"
- Affiche le nombre de crédits bonus
- Champ pour entrer un code promo
- Bouton "Appliquer" pour activer le code

**Comportement :**
1. L'utilisateur entre un code promo (ex: `BIENVENUE`)
2. Clique sur "Appliquer"
3. Le système vérifie la validité du code
4. Si valide, applique la récompense
5. Affiche un message de succès
6. Recharge la page pour voir les nouveaux crédits

**Ordre d'utilisation des interprétations :**
1. **Premium** : Si utilisateur Premium → Illimité
2. **Crédits bonus** : Si crédits > 0 → Consomme 1 crédit
3. **Gratuit mensuel** : Sinon → Utilise 1/3 interprétations gratuites

---

## 🔐 Sécurité Admin

### Décorateur `@admin_required`

Toutes les routes admin utilisent ce décorateur :

```python
@bp.route('/admin/dashboard')
@login_required
@admin_required
def dashboard():
    # Code admin
```

**Protection :**
- L'utilisateur doit être connecté
- L'utilisateur doit avoir `is_admin=True`
- Sinon, redirection vers la page d'accueil avec message d'erreur

### Restrictions

1. **Ne peut pas se désadminer soi-même**
   - Évite de perdre l'accès admin par erreur

2. **Ne peut pas se supprimer soi-même**
   - Évite de supprimer le compte admin actif

3. **Confirmation pour actions critiques**
   - Suppression d'utilisateurs
   - Suppression de codes promo

---

## 📊 Modèles de Données Ajoutés

### Modification du modèle `User`

```python
# Nouveaux champs
is_admin = db.Column(db.Boolean, default=False)
credits = db.Column(db.Integer, default=0)

# Nouvelles méthodes
def use_interpretation():
    """Consomme un crédit si applicable"""

def can_interpret():
    """Vérifie si peut faire une interprétation
    Ordre : Premium → Crédits → Gratuit mensuel"""
```

### Nouveau modèle `PromoCode`

```python
class PromoCode(db.Model):
    id = Integer
    code = String(50)  # Unique, Index
    reward_type = String(20)  # 'credits' ou 'premium_days'
    reward_value = Integer
    max_uses = Integer  # None = illimité
    current_uses = Integer
    expires_at = DateTime  # None = jamais
    is_active = Boolean
    created_by = ForeignKey(User.id)
    created_at = DateTime
    description = String(200)

    # Méthodes
    def is_valid()  # Vérifie validité
    def use_code(user)  # Applique à l'utilisateur
```

---

## 🎨 Design

Le panneau admin utilise le même design mystique que SACRA :
- Gradient beige/lavande/violet
- Cartes avec effet mystique
- Animations fade-in
- Boutons avec gradient purple
- Badge rouge pour le bouton Admin (👑)
- Responsive mobile/tablet/desktop

---

## 🔧 Routes API

### Routes Admin

```
GET  /admin/dashboard                      - Dashboard principal
GET  /admin/users                          - Liste utilisateurs
POST /admin/users/<id>/add-credits         - Ajouter crédits
POST /admin/users/<id>/toggle-premium      - Toggle premium
POST /admin/users/<id>/toggle-admin        - Toggle admin
POST /admin/users/<id>/delete              - Supprimer user
GET  /admin/promo-codes                    - Liste codes promo
POST /admin/promo-codes/create             - Créer code
POST /admin/promo-codes/<id>/toggle        - Activer/désactiver
POST /admin/promo-codes/<id>/delete        - Supprimer code
```

### Routes Utilisateur

```
POST /premium/apply-promo-code             - Appliquer un code promo
```

**Format JSON pour apply-promo-code :**

```json
{
  "code": "BIENVENUE"
}
```

**Réponse succès :**

```json
{
  "success": true,
  "message": "5 crédits ajoutés à ton compte ! 🎁",
  "new_credits": 15,
  "is_premium": false
}
```

**Réponse erreur :**

```json
{
  "success": false,
  "error": "Code promo invalide"
}
```

---

## 📱 Interface Utilisateur

### Pour les Admins

**Navigation :**
- Bouton **👑 Admin** (rouge) visible dans la barre de navigation
- Clic → Dashboard admin

**Dashboard :**
- 3 onglets : Statistiques / Utilisateurs / Codes Promo
- Statistiques en temps réel
- Actions rapides sur chaque élément

### Pour les Utilisateurs

**Dashboard :**
- Section "🎁 Codes Promo & Crédits"
- Affichage du nombre de crédits bonus
- Champ de saisie code promo
- Bouton "Appliquer"
- Messages de succès/erreur en vert/rouge

---

## 🚀 Déploiement sur o2switch

### 1. Mettre à Jour la Base de Données

```bash
# Sur le serveur o2switch
cd ~/sacra.fr

# Backup de l'ancienne base
cp instance/sacra.db instance/sacra_backup_$(date +%Y%m%d).db

# Supprimer et recréer
rm instance/sacra.db
python3 init_admin.py
```

### 2. Créer un Compte Admin

**Option A : Utiliser le script**
```bash
python3 init_admin.py
# Crée admin@sacra.fr / admin123
```

**Option B : Depuis la console Python**
```python
from app import create_app
from app.models import db, User

app = create_app()
with app.app_context():
    admin = User(
        email='ton-email@sacra.fr',
        first_name='Ton Nom',
        is_admin=True,
        is_premium=True,
        credits=100
    )
    admin.set_password('ton-mot-de-passe-securise')
    db.session.add(admin)
    db.session.commit()
```

### 3. Redémarrer l'Application

```bash
touch tmp/restart.txt
```

### 4. Tester

```bash
curl https://sacra.fr/admin/dashboard
# Doit rediriger vers /auth/login si non connecté
```

---

## 🎯 Cas d'Usage

### Scénario 1 : Campagne de Lancement

**Objectif :** Offrir 5 crédits aux nouveaux utilisateurs

```
1. Se connecter en admin
2. Aller sur /admin/promo-codes
3. Créer le code :
   - Code : LANCEMENT2024
   - Type : Crédits
   - Valeur : 5
   - Max uses : 500
   - Expire : 30 jours
   - Desc : Campagne de lancement
4. Partager le code sur les réseaux sociaux
5. Suivre les utilisations dans le dashboard
```

### Scénario 2 : Support Client

**Situation :** Un utilisateur a un problème et mérite un geste commercial

```
1. Se connecter en admin
2. Aller sur /admin/users
3. Rechercher l'utilisateur par email
4. Cliquer sur 💰
5. Ajouter 10 crédits
6. Confirmer
```

### Scénario 3 : Essai Premium

**Objectif :** Offrir 7 jours de Premium à des influenceurs

```
1. Créer un code promo :
   - Code : INFLUENCEUR
   - Type : Jours Premium
   - Valeur : 7
   - Max uses : 10
   - Expire : 7 jours
2. Envoyer le code aux influenceurs
3. Ils l'appliquent sur leur dashboard
```

---

## 📝 Checklist de Déploiement

Avant de déployer en production :

- [ ] Backup de la base de données existante
- [ ] Supprimer `instance/sacra.db`
- [ ] Lancer `init_admin.py`
- [ ] **CHANGER le mot de passe admin par défaut**
- [ ] Créer les codes promo de lancement
- [ ] Tester la connexion admin
- [ ] Tester la création d'un code promo
- [ ] Tester l'application d'un code promo côté utilisateur
- [ ] Tester l'ajout de crédits à un utilisateur
- [ ] Vérifier les permissions (non-admins ne peuvent pas accéder)
- [ ] Redémarrer l'application (`touch tmp/restart.txt`)
- [ ] Tester sur https://sacra.fr

---

## 🆘 Dépannage

### Problème : "Accès réservé aux administrateurs"

**Solution :**
```python
# Console Python
from app import create_app
from app.models import db, User

app = create_app()
with app.app_context():
    user = User.query.filter_by(email='ton-email').first()
    user.is_admin = True
    db.session.commit()
```

### Problème : "Code promo invalide" alors qu'il existe

**Vérifications :**
1. Le code est-il actif ? (`is_active=True`)
2. A-t-il expiré ? (vérifier `expires_at`)
3. A-t-il atteint sa limite ? (`current_uses < max_uses`)

**Console Python :**
```python
from app.models import PromoCode

promo = PromoCode.query.filter_by(code='TONCODE').first()
print(f"Actif: {promo.is_active}")
print(f"Valide: {promo.is_valid()}")
print(f"Uses: {promo.current_uses}/{promo.max_uses}")
```

### Problème : Les crédits ne se déduisent pas

**Vérifier :**
- La méthode `use_interpretation()` est-elle appelée après chaque interprétation ?

**Correction dans `interpretations.py` :**
```python
@bp.route('/dream', methods=['POST'])
def dream():
    # ... code existant ...

    # IMPORTANT : Consommer un crédit après interprétation
    current_user.use_interpretation()

    return jsonify({'success': True})
```

---

## 📚 Fichiers Créés/Modifiés

### Nouveaux Fichiers

```
app/routes/admin.py                    - Blueprint admin (270 lignes)
app/templates/admin/dashboard.html     - Dashboard admin
app/templates/admin/users.html         - Gestion utilisateurs
app/templates/admin/promo_codes.html   - Gestion codes promo
init_admin.py                          - Script d'initialisation
ADMIN_GUIDE.md                         - Ce guide
```

### Fichiers Modifiés

```
app/models.py                          - Ajout is_admin, credits, PromoCode
app/__init__.py                        - Enregistrement blueprint admin
app/routes/premium.py                  - Route apply-promo-code
app/templates/base.html                - Lien Admin dans navigation
app/templates/dashboard.html           - Section codes promo
```

---

## 🎉 Récapitulatif

**Fonctionnalités ajoutées :**
✅ Dashboard admin complet avec statistiques
✅ Gestion utilisateurs (crédits, premium, admin, suppression)
✅ Système de codes promo (crédits + jours premium)
✅ Interface utilisateur pour appliquer codes promo
✅ Système de crédits bonus
✅ Protection admin avec décorateur
✅ Design mystique cohérent avec SACRA
✅ Script d'initialisation automatique
✅ Documentation complète

**Prêt pour la production ! 🚀**

---

**Développé avec ❤️ par Claude Code**
🌙 SACRA - Ton guide spirituel IA ✨

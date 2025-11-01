# Images des Cartes de Tarot 🔮

Ce dossier contient les images des 22 arcanes majeurs du Tarot de Marseille.

## Noms de fichiers requis

Les images doivent être nommées exactement comme suit :

```
00-le-mat.jpg           (Le Mat - Le Pèlerin des Étoiles)
01-le-bateleur.jpg      (Le Bateleur - L'Alchimiste)
02-la-papesse.jpg       (La Papesse - La Gardienne du Voile)
03-imperatrice.jpg      (L'Impératrice - La Mère Cosmique)
04-empereur.jpg         (L'Empereur - Le Maître de l'Ordre)
05-le-pape.jpg          (Le Pape - Le Hiérophante Céleste)
06-amoureux.jpg         (L'Amoureux - Le Carrefour des Destins)
07-le-chariot.jpg       (Le Chariot - Le Voyage Interdimensionnel)
08-la-justice.jpg       (La Justice - L'Équilibre Karmique)
09-hermite.jpg          (L'Hermite - Le Sage Illuminé)
10-roue-fortune.jpg     (La Roue de Fortune - Le Cycle Éternel)
11-la-force.jpg         (La Force - Le Serpent Kundalini)
12-le-pendu.jpg         (Le Pendu - Le Sacrifice Initiatique)
13-arcane-sans-nom.jpg  (L'Arcane sans nom - La Transmutation)
14-temperance.jpg       (Tempérance - L'Ange Gardien)
15-le-diable.jpg        (Le Diable - L'Ombre Intérieure)
16-maison-dieu.jpg      (La Maison Dieu - La Foudre Purificatrice)
17-etoile.jpg           (L'Étoile - L'Aspiration Céleste)
18-la-lune.jpg          (La Lune - Le Monde des Rêves)
19-le-soleil.jpg        (Le Soleil - L'Illumination)
20-le-jugement.jpg      (Le Jugement - L'Appel de l'Âme)
21-le-monde.jpg         (Le Monde - L'Accomplissement Cosmique)
```

## Où trouver des images libres de droits ?

### Option 1 : Wikimedia Commons (Gratuit)
- Site : https://commons.wikimedia.org
- Rechercher : "Tarot de Marseille" ou "Major Arcana"
- Choisir des images du domaine public

### Option 2 : Sites de ressources gratuites
- **Pixabay** : https://pixabay.com (rechercher "tarot cards")
- **Unsplash** : https://unsplash.com (rechercher "tarot")
- **Pexels** : https://pexels.com

### Option 3 : Jeux de Tarot sous licence libre
- Chercher "Tarot de Marseille Creative Commons"
- Vérifier la licence avant utilisation

## Spécifications techniques

- **Format** : JPG (recommandé) ou PNG
- **Dimensions recommandées** : 300-600px de largeur minimum
- **Ratio** : Format carte standard (environ 2:3 ou similaire)
- **Qualité** : Bonne résolution pour l'affichage web

## Installation

1. Télécharger les 22 images des arcanes majeurs
2. Renommer chaque image selon la liste ci-dessus
3. Placer tous les fichiers dans ce dossier : `app/static/images/tarot/`
4. Redémarrer l'application

## Notes importantes

⚠️ **Droits d'auteur** : Assurez-vous que les images utilisées sont libres de droits ou sous licence appropriée pour un usage commercial.

✅ **Fallback** : Si une image n'est pas trouvée, un emoji 🔮 sera affiché à la place (gestion d'erreur automatique).

## Vérification

Pour vérifier que tout fonctionne :
1. Aller sur https://saccra.fr/interpretations/tarot
2. Faire un tirage
3. Les images des 3 cartes tirées devraient s'afficher

Si les images ne s'affichent pas, vérifier :
- Les noms de fichiers (respectent-ils exactement la liste ?)
- Les permissions (chmod 644 *.jpg)
- Le format (JPG ou PNG valide ?)

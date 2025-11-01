"""
Script pour remplacer les anciennes méditations par les nouvelles (plus longues)

Usage: python migrate_meditations.py
"""
from app import create_app
from app.models import db, Meditation

app = create_app()

# Nouvelles méditations (scripts beaucoup plus longs)
MEDITATIONS = [
    # CHAKRAS
    {
        'title': 'Équilibrage des 7 Chakras',
        'description': 'Voyage énergétique à travers tes 7 centres d\'énergie pour les harmoniser et les aligner.',
        'theme': 'chakras',
        'duration_minutes': 7,
        'script': """
Bienvenue dans cette méditation d'équilibrage des sept chakras.

Installe-toi confortablement, que tu sois assis en tailleur, sur une chaise, ou allongé sur le dos. Choisis la position qui te convient le mieux.

Ferme doucement les yeux. Prends un moment pour simplement arriver ici, maintenant, dans cet espace sacré que tu te crées.

Commence par porter ton attention sur ta respiration naturelle. Observe l'air qui entre par tes narines, frais et vivifiant. Observe l'air qui ressort, chaud et apaisant.

Prends maintenant trois grandes respirations conscientes. Inspire profondément par le nez, en comptant jusqu'à quatre. Un, deux, trois, quatre. Retiens quelques secondes. Et expire longuement par la bouche, en comptant jusqu'à six. Un, deux, trois, quatre, cinq, six.

Encore une fois. Grande inspiration. Un, deux, trois, quatre. Et longue expiration. Un, deux, trois, quatre, cinq, six.

Une dernière fois. Inspire. Remplis tes poumons complètement. Et expire. Relâche toutes les tensions, tous les soucis de la journée.

Maintenant, laisse ta respiration reprendre son rythme naturel. N'essaie plus de la contrôler. Observe-la simplement.

Nous allons maintenant voyager ensemble à travers tes sept centres d'énergie, du bas vers le haut de ton corps.

Porte ton attention tout en bas de ta colonne vertébrale, à la base de ton coccyx, entre tes jambes. C'est là que se trouve ton premier chakra, Muladhara, le chakra racine.

Visualise dans cette zone une sphère de lumière rouge, d'un rouge profond comme la terre, comme les racines d'un arbre puissant. Cette lumière rouge pulse doucement, elle respire avec toi.

À chaque inspiration, cette sphère rouge devient un peu plus grande, un peu plus lumineuse. À chaque expiration, elle tourne lentement sur elle-même, dans le sens des aiguilles d'une montre.

Ce chakra racine t'ancre à la terre. Il représente ta sécurité, ta stabilité, ton sentiment d'appartenance à ce monde. Sens des racines de lumière rouge qui descendent de ce chakra, qui traversent le sol, qui s'enfoncent profondément dans la terre.

Tu es ancré. Tu es en sécurité. Tu es stable. Tu es chez toi sur cette terre.

Répète mentalement trois fois: "Je suis en sécurité. Je suis ancré. Je suis stable."

Prends encore deux respirations dans ce chakra racine rouge.

Maintenant, laisse cette énergie rouge monter légèrement dans ton corps. Juste au-dessus de ton os pubien, quelques centimètres sous ton nombril. C'est là que se trouve ton deuxième chakra, Svadhisthana, le chakra sacré.

Visualise dans cette zone une sphère de lumière orange, d'un orange vif comme un coucher de soleil, comme une flamme dansante. Cette lumière orange tourbillonne doucement.

À chaque inspiration, ce chakra orange grandit. À chaque expiration, il rayonne sa lumière chaude tout autour.

Ce chakra sacré est le siège de ta créativité, de tes émotions, de ta sensualité, de ta joie de vivre. C'est l'eau qui coule en toi.

Visualise cette sphère orange comme de l'eau en mouvement, fluide, libre, expressive. Laisse les émotions circuler. Accueille ta créativité.

Répète mentalement trois fois: "Je ressens pleinement. Je crée librement. Je me permets d'être moi-même."

Respire encore deux fois dans ce chakra orange.

L'énergie monte encore. Elle arrive maintenant au niveau de ton plexus solaire, juste au-dessus de ton nombril, sous ta cage thoracique. C'est ton troisième chakra, Manipura, le chakra du plexus solaire.

Visualise dans cette zone une sphère de lumière jaune, d'un jaune doré éclatant comme le soleil du midi, comme de l'or liquide. Cette lumière jaune brille intensément.

À chaque inspiration, ce soleil intérieur devient plus brillant, plus puissant. À chaque expiration, ses rayons se diffusent dans tout ton corps.

Ce chakra est ton centre de pouvoir personnel, de confiance en toi, de volonté, de détermination. C'est le feu qui brûle en toi.

Sens la chaleur de ce soleil jaune dans ton ventre. Sens ta force, ton courage, ta capacité à agir. Tu es puissant. Tu es capable.

Répète mentalement trois fois: "Je suis fort. Je suis confiant. Je peux réaliser mes rêves."

Inspire, expire, dans cette lumière jaune dorée.

L'énergie continue son ascension. Elle arrive maintenant au centre de ta poitrine, au niveau de ton cœur. C'est ton quatrième chakra, Anahata, le chakra du cœur.

Visualise dans cette zone une sphère de lumière verte, d'un vert émeraude magnifique comme une forêt en printemps, comme le jade le plus pur. Cette lumière verte pulse au rythme de ton cœur.

À chaque battement de cœur, à chaque respiration, ce chakra vert s'épanouit comme une fleur qui s'ouvre.

Ce chakra est le siège de l'amour inconditionnel, de la compassion, du pardon, de la connexion aux autres. C'est l'air qui circule, qui relie tout.

Sens ton cœur s'ouvrir. Envoie de l'amour à toi-même d'abord. Tu mérites cet amour. Tu es digne de recevoir autant que de donner.

Puis envoie cet amour vert à ceux que tu aimes. À tous les êtres vivants. Ton cœur est un pont entre toi et le monde.

Répète mentalement trois fois: "J'aime et je suis aimé. Je pardonne et je me pardonne. Mon cœur est ouvert."

Respire profondément dans ce chakra vert du cœur.

Laisse maintenant cette énergie monter à ta gorge. C'est ton cinquième chakra, Vishuddha, le chakra de la gorge.

Visualise dans cette zone une sphère de lumière bleu ciel, d'un bleu clair comme le ciel d'été, comme l'océan sous le soleil. Cette lumière bleue vibre doucement.

À chaque inspiration et expiration, sens ce chakra bleu qui s'active, qui s'équilibre.

Ce chakra est le centre de ta communication, de ton expression personnelle, de ta vérité. C'est ton espace pour dire qui tu es vraiment.

Sens ta voix intérieure. Ta vérité unique. Ta capacité à t'exprimer authentiquement.

Répète mentalement trois fois: "Je m'exprime librement. Je dis ma vérité. Ma voix est importante."

Respire dans cette lumière bleue apaisante.

L'énergie monte encore, elle arrive entre tes sourcils, au centre de ton front. C'est ton sixième chakra, Ajna, le chakra du troisième œil.

Visualise dans cette zone une sphère de lumière indigo, d'un bleu violet profond comme le ciel nocturne, comme l'améthyste. Cette lumière indigo pulse avec une sagesse ancienne.

À chaque respiration, ce troisième œil s'ouvre un peu plus, se clarifie, voit plus loin.

Ce chakra est le siège de ton intuition, de ta vision intérieure, de ta sagesse spirituelle, de ta clairvoyance.

Fais confiance à ton intuition. Fais confiance à ta vision. Tu sais. Au fond de toi, tu sais.

Répète mentalement trois fois: "Je vois clairement. J'ai confiance en mon intuition. Je suis sage."

Respire dans cette lumière indigo mystique.

Enfin, l'énergie arrive au sommet de ton crâne. C'est ton septième chakra, Sahasrara, le chakra couronne.

Visualise au sommet de ta tête une sphère de lumière violette, ou blanche, ou dorée, selon ce qui vient naturellement. C'est une lumière divine, pure, transcendante.

À chaque respiration, ce chakra s'ouvre comme les pétales d'un lotus à mille pétales. Tu es connecté. Connecté à l'univers entier. À toute vie. À tout ce qui est.

Ce chakra est ta connexion au divin, à ta conscience supérieure, à l'unité cosmique.

Répète mentalement trois fois: "Je suis connecté. Je suis Un avec l'univers. Je suis conscience pure."

Maintenant, prends un moment pour visualiser tous tes chakras en même temps. Rouge à la base. Orange sous le nombril. Jaune au plexus. Vert au cœur. Bleu à la gorge. Indigo au front. Violet au sommet.

Tu es un arc-en-ciel de lumière. Une colonne de couleurs vibrantes qui va de la terre au ciel. Tous tes chakras sont alignés, équilibrés, en harmonie parfaite.

Respire dans cette harmonie. Dans cet équilibre. Dans cette complétude.

Sens l'énergie circuler librement de bas en haut et de haut en bas le long de ta colonne vertébrale.

Tu es équilibré. Tu es harmonieux. Tu es complet.

Reste encore un moment dans cette sensation. Savoure cet alignement.

Quand tu te sens prêt, commence doucement à ramener ta conscience dans la pièce. Bouge légèrement tes doigts. Bouge légèrement tes orteils.

Prends une grande inspiration. Et une longue expiration.

Ouvre les yeux en douceur, doucement, à ton rythme.

Prends le temps de t'étirer si tu en ressens le besoin.

Merci d'avoir pris ce temps pour toi. Merci d'avoir honoré tes centres d'énergie.

Porte cette harmonie avec toi tout au long de ta journée.

Namaste.
"""
    },
    {
        'title': 'Ancrage et Sécurité Intérieure',
        'description': 'Renforce ton chakra racine pour te sentir stable, en sécurité et ancré dans le moment présent.',
        'theme': 'chakras',
        'duration_minutes': 5,
        'script': """
Bienvenue dans cette méditation d'ancrage.

Assieds-toi confortablement, le dos droit mais sans rigidité. Si tu es sur une chaise, pose tes deux pieds bien à plat sur le sol. Si tu es par terre, assieds-toi en tailleur ou dans la position qui te convient.

Ferme doucement les yeux. Ou garde-les mi-clos si tu préfères.

Prends un instant pour t'installer, pour arriver vraiment ici, maintenant.

Porte ton attention sur ta respiration. Inspire par le nez. Expire par le nez. Observe simplement ce va-et-vient de ton souffle.

Maintenant, sens les points de contact entre ton corps et ce qui te soutient. Sens tes fesses sur la chaise ou sur le sol. Sens tes cuisses qui reposent. Sens tes pieds qui touchent la terre.

Prends conscience du poids de ton corps. Tu es ici. Tu es présent. Tu es solide.

Porte maintenant toute ton attention à la base de ta colonne vertébrale, entre tes jambes, au niveau de ton coccyx. C'est là que se trouve ton chakra racine, Muladhara.

Visualise dans cette zone une sphère de lumière rouge. Rouge comme la terre. Rouge comme les racines d'un chêne centenaire. Rouge comme le rubis.

Cette lumière rouge pulse doucement. Elle est chaude. Elle est stable. Elle est forte.

À chaque inspiration, imagine que tu respires directement dans cette sphère rouge. Elle grandit, elle s'illumine.

À chaque expiration, imagine que cette lumière rouge s'ancre encore plus profondément en toi.

Maintenant, visualise des racines de lumière rouge qui partent de ce chakra racine. Des racines puissantes, épaisses, solides. Elles descendent de ton corps, elles traversent le sol sous toi.

Ces racines continuent de descendre, de plus en plus profondément. Elles traversent les fondations du bâtiment. Elles pénètrent dans la terre. Dans la roche. Elles s'enfoncent, s'enfoncent, s'enfoncent.

Elles atteignent maintenant le cœur de la Terre. Ce noyau chaud, solide, stable, qui est là depuis des milliards d'années.

Tes racines s'enroulent autour de ce noyau. Tu es connecté au cœur de la Terre. Tu es ancré. Tu ne peux pas tomber. Tu ne peux pas être déstabilisé.

Sens la force de la Terre qui remonte maintenant le long de tes racines. Une énergie rouge, chaude, stable, sécurisante. Elle remonte, elle remonte, elle arrive à ton chakra racine.

Cette énergie de la Terre remplit ta sphère rouge. Tu absorbes la stabilité de la Terre. Sa patience. Sa force tranquille.

Répète mentalement, trois fois : "Je suis ancré. Je suis en sécurité. Je suis stable."

Inspire profondément. Expire complètement.

Encore une fois : "Je suis ancré. Je suis en sécurité. Je suis stable."

Continue de respirer. Sens tes racines profondément plantées dans la Terre.

Tu es comme un arbre. Tu peux plier dans le vent, mais tu ne romps pas. Tes racines te tiennent. Tu es solide.

Quoi qu'il se passe autour de toi, quoi qu'il se passe dans ta vie, tu as toujours ces racines. Tu as toujours cette connexion à la Terre. Tu es toujours en sécurité au fond de toi.

Prends encore quelques respirations dans cette sensation d'ancrage.

Sens le poids de ton corps. Tu es ici. Tu es présent. Tu es en sécurité.

Quand tu te sens prêt, commence à bouger légèrement les doigts, les orteils.

Prends une grande inspiration. Une longue expiration.

Ouvre les yeux doucement.

Emporte cet ancrage avec toi. Ces racines sont toujours là. Tu peux te reconnecter à elles à tout moment, simplement en fermant les yeux et en respirant.

Merci pour cette pratique.

Namaste.
"""
    },

    # MANIFESTATION
    {
        'title': 'Attirer l\'Abondance',
        'description': 'Élève ta vibration pour attirer l\'abondance sous toutes ses formes dans ta vie.',
        'theme': 'manifestation',
        'duration_minutes': 8,
        'script': """
Bienvenue dans cette méditation pour attirer l'abondance.

Installe-toi confortablement, que tu sois assis ou allongé. Choisis une position où tu peux rester sans bouger pendant quelques minutes.

Ferme les yeux. Prends quelques respirations profondes pour te centrer.

Inspire par le nez, lentement. Expire par la bouche, complètement. Inspire. Expire. Encore une fois. Inspire. Expire.

Maintenant, laisse ta respiration reprendre son rythme naturel.

L'abondance est ton état naturel. C'est ton droit de naissance. Tu es né dans un univers d'abondance infinie. Il y a assez pour tout le monde. Il y a assez pour toi.

Commence par prendre conscience de l'abondance qui est déjà présente dans ta vie en ce moment même.

Tu respires. L'air est abondant. Gratuit. Toujours disponible pour toi. Prends conscience de l'abondance de l'air qui entre dans tes poumons. Merci.

Tu as un corps. Un corps qui fonctionne. Un cœur qui bat. Des poumons qui respirent. Des yeux qui voient. Des oreilles qui entendent. Quelle abondance. Merci.

Tu as un lieu où vivre. Un toit. Des murs. Un espace rien que pour toi. Quelle abondance. Merci.

Tu as accès à de l'eau. À de la nourriture. À des vêtements. Quelle abondance. Merci.

Tu as des gens qui t'aiment. Des amis. De la famille. Des collègues. Des rencontres. Quelle abondance de connexions humaines. Merci.

Prends un moment pour ressentir cette gratitude pour l'abondance déjà présente. La gratitude est la clé qui ouvre la porte à encore plus d'abondance.

Maintenant, nous allons clarifier et magnétiser ce que tu souhaites attirer.

Pense à un domaine de ta vie où tu souhaites plus d'abondance. Peut-être l'argent. Peut-être l'amour. Peut-être les opportunités. Peut-être la santé. Peut-être la créativité. Choisis un domaine. Un seul pour cette méditation.

Visualise maintenant que tu as déjà cette abondance. Tu ne la désires plus. Tu ne l'espères plus. Tu l'AS. Elle est déjà là. Comment te sens-tu ? Que vois-tu ? Où es-tu ? Avec qui ?

Rends cette visualisation aussi réelle, aussi vivante que possible. Utilise tous tes sens.

Si c'est l'argent : visualise ton compte en banque. Vois le chiffre que tu désires. Ressens le soulagement. La liberté. La sécurité. Vois-toi payant tes factures facilement. T'offrant ce que tu veux. Aidant ceux que tu aimes.

Si c'est l'amour : visualise ton partenaire. Sens-toi dans ses bras. Entends ses mots d'amour. Vois son sourire. Ressens cette chaleur, cette connexion, cette joie d'être aimé et d'aimer.

Si c'est la santé : sens ton corps vital, énergique, fort. Vois-toi bougeant avec aisance. Ressens cette énergie qui circule. Cette vitalité. Cette force.

Quelle que soit ton abondance, vis-la maintenant. Dans ta visualisation, tu l'as déjà. C'est fait. C'est réel.

Maintenant, imagine qu'une lumière dorée descend du ciel. C'est la lumière de l'abondance universelle. Cette lumière dorée entre par le sommet de ta tête, descend dans tout ton corps.

Cette lumière dorée emplit chaque cellule. Tu deviens lumineux. Brillant. Magnétique.

Cette lumière dorée rayonne maintenant hors de ton corps. Elle crée un champ magnétique autour de toi. Un champ d'attraction puissant.

Tout ce qui vibre à la même fréquence que ton abondance est maintenant attiré vers toi. Comme un aimant.

Les opportunités te trouvent. L'argent te trouve. Les bonnes personnes te trouvent. Les bonnes occasions te trouvent.

Tu n'as pas à chercher. Tu n'as pas à forcer. Tu n'as qu'à rester dans cette vibration élevée. Tu n'as qu'à rester dans cette certitude. Cette abondance est tienne. Elle vient à toi. Maintenant.

Répète mentalement, avec conviction : "Je suis un aimant pour l'abondance. Tout ce dont j'ai besoin vient à moi facilement. L'univers conspire en ma faveur."

Encore une fois : "Je suis un aimant pour l'abondance. Tout ce dont j'ai besoin vient à moi facilement. L'univers conspire en ma faveur."

Sens cette vérité dans tout ton être. Ce n'est pas un espoir. C'est une certitude. C'est une loi universelle. Tu es abondance.

Maintenant, et c'est très important, envoie de la gratitude à l'univers. Merci pour ce qui vient. Merci pour ce qui est déjà en route vers toi. Merci pour cette abondance qui se manifeste maintenant dans ta vie.

Ressens cette gratitude dans ton cœur. Laisse-la rayonner.

La gratitude accélère la manifestation. La gratitude élève ta vibration encore plus haut.

Prends encore quelques respirations dans cette énergie d'abondance et de gratitude.

Sens-toi riche. Sens-toi béni. Sens-toi soutenu par l'univers.

Quand tu es prêt, commence à ramener ta conscience dans la pièce.

Bouge tes doigts. Bouge tes orteils.

Prends une grande inspiration. Une longue expiration.

Ouvre les yeux doucement.

Tout au long de ta journée, reste dans cette vibration d'abondance. Reste dans cette gratitude. Remarque tous les signes que l'univers t'envoie. Sois attentif aux opportunités. Dis oui à ce qui s'aligne avec ton abondance.

Et surtout, agis. L'abondance aime l'action. Fais un pas, même petit, dans la direction de ton abondance aujourd'hui.

Merci pour cette pratique.

Namaste.
"""
    },

    # GUÉRISON
    {
        'title': 'Libération des Blessures du Passé',
        'description': 'Libère les douleurs émotionnelles anciennes et retrouve ta paix intérieure.',
        'theme': 'guérison',
        'duration_minutes': 10,
        'script': """
Bienvenue dans cet espace sacré de guérison.

Allonge-toi confortablement, si possible. Ou assieds-toi dans une position qui te permet de vraiment lâcher prise.

Ferme les yeux. Prends une grande inspiration par le nez. Expire longuement par la bouche, en faisant un soupir si tu en as envie. Relâche.

Encore une fois. Grande inspiration. Longue expiration. Relâche tout.

Une dernière fois. Inspire profondément. Expire complètement. Laisse ton corps s'enfoncer dans le sol, dans la chaise, dans le lit. Abandonne-toi à ce support.

Maintenant, laisse ta respiration reprendre son rythme naturel. Observe-la simplement.

Dans cette méditation, nous allons visiter une blessure du passé. Une douleur émotionnelle que tu portes peut-être depuis longtemps. Quelque chose que tu as peut-être essayé d'ignorer, de repousser, d'oublier.

Mais aujourd'hui, nous allons l'accueillir. Nous allons la regarder avec compassion. Et nous allons la libérer.

Porte ton attention sur ton cœur, au centre de ta poitrine. Demande doucement à ton cœur : quelle est la blessure qui a le plus besoin de guérison aujourd'hui ?

Ne cherche pas. Ne force pas. Laisse venir ce qui vient. C'est peut-être une image. Un souvenir. Un sentiment. Un nom. Un âge que tu avais. Laisse venir.

Quelle que soit cette blessure, quelle que soit cette douleur, accueille-la maintenant. Dis-lui mentalement : "Je te vois. Je te reconnais. Tu as le droit d'exister. Tu as ta place ici."

Cette blessure a peut-être été ignorée pendant longtemps. Peut-être même par toi. Mais aujourd'hui, tu la vois. Tu la reconnais.

Maintenant, donne une forme à cette blessure dans ton esprit. Si elle était un objet, quelle forme aurait-elle ? Une pierre ? Un nœud ? Une tache sombre ? Ne juge pas. Observe simplement.

Donne-lui aussi une couleur. Quelle est la couleur de cette douleur ? Noir ? Gris ? Rouge ? Bleu ? Laisse venir.

Donne-lui une texture. Est-elle lisse ? Rugueuse ? Dure ? Molle ? Froide ? Chaude ?

Donne-lui même une taille. Est-elle petite comme un caillou ? Grande comme un rocher ? Immense ?

Maintenant que tu peux la voir, cette blessure, nous allons la guérir.

Imagine qu'une lumière dorée commence à descendre du ciel. C'est une lumière de pur amour. De pure compassion. De pure guérison.

Cette lumière dorée descend vers toi. Elle entre par le sommet de ta tête, comme une douce pluie de guérison.

Cette lumière descend dans ton corps. Elle arrive à ton cœur. Elle voit ta blessure.

Et avec tant de douceur, tant d'amour, cette lumière dorée enveloppe ta blessure. Elle ne la juge pas. Elle ne la rejette pas. Elle l'embrasse avec une compassion infinie.

La lumière dorée commence maintenant à pénétrer dans la blessure. Doucement. Respectueusement. Avec amour.

La blessure commence à se transformer. Peut-être qu'elle change de couleur. Peut-être qu'elle devient plus petite. Peut-être qu'elle se dissout. Peut-être qu'elle s'ouvre comme une fleur.

Laisse ce processus se faire naturellement. Ne force rien. Observe simplement. La guérison se fait à son propre rythme.

Si des émotions montent, c'est parfait. Laisse-les venir. Les larmes sont de la guérison liquide. La colère qui sort est de l'énergie qui se libère. La tristesse qui est accueillie peut enfin partir.

Respire dans ces émotions. Donne-leur de l'espace. Elles ont besoin d'être ressenties pour pouvoir être libérées.

La lumière dorée continue son travail. Elle dissout la douleur. Elle transforme la blessure en compréhension. En sagesse. En force.

Maintenant, parle à cette partie blessée de toi. Dis-lui ce qu'elle a besoin d'entendre depuis si longtemps.

Peut-être : "Ce n'était pas de ta faute."

Peut-être : "Tu as fait de ton mieux."

Peut-être : "Je suis désolé que tu aies vécu ça."

Peut-être : "Je te pardonne."

Peut-être : "Je me pardonne."

Dis-lui : "Tu peux te reposer maintenant. Je vais prendre soin de toi. Tu es en sécurité maintenant."

Sens la libération qui se produit. La blessure devient de plus en plus légère. De plus en plus lumineuse.

Maintenant, imagine que là où il y avait la blessure, il y a maintenant une belle lumière blanche. Pure. Paisible. Libre.

Cette lumière blanche rayonne dans tout ton corps. Elle remplit ton cœur. Elle se diffuse dans chaque cellule.

Tu es guéri un peu plus aujourd'hui. Tu es libéré un peu plus aujourd'hui.

Répète mentalement trois fois : "Je libère le passé. Je me pardonne. Je suis libre."

Encore : "Je libère le passé. Je me pardonne. Je suis libre."

Une dernière fois : "Je libère le passé. Je me pardonne. Je suis libre."

Prends un moment pour savourer cette liberté. Cette paix. Cette légèreté.

Envoie de la gratitude à ton corps pour avoir porté cette blessure jusqu'à aujourd'hui. Envoie de la gratitude à ton cœur pour son courage de visiter cette douleur. Envoie de la gratitude à toi-même pour avoir fait ce travail important.

Respire profondément dans cette paix nouvelle.

Quand tu te sens prêt, commence doucement à revenir. Bouge tes doigts. Bouge tes orteils.

Prends ton temps. Il n'y a pas de précipitation.

Grande inspiration. Longue expiration.

Ouvre les yeux en douceur quand tu es prêt.

Sois doux avec toi après cette méditation. Bois de l'eau. Repose-toi si tu en as besoin.

Tu as fait un travail magnifique aujourd'hui. Honore-le.

Merci pour ce moment de guérison.

Namaste.
"""
    },

    # SOMMEIL
    {
        'title': 'Voyage vers le Sommeil Profond',
        'description': 'Détente complète du corps et de l\'esprit pour t\'endormir paisiblement et dormir profondément.',
        'theme': 'sommeil',
        'duration_minutes': 12,
        'script': """
Bonsoir. Bienvenue dans ce voyage vers un sommeil profond et réparateur.

Tu es maintenant allongé dans ton lit, dans ta position préférée pour dormir. Arrange ton oreiller. Tire ta couverture. Trouve le confort parfait.

Ferme doucement les yeux. Tu peux les garder fermés jusqu'à ce que tu t'endormes. Il n'y a rien d'autre à faire que te laisser aller.

Prends une grande inspiration par le nez. Retiens un instant. Et expire longuement par la bouche, en faisant un grand soupir. Aaahhh.

Encore une fois. Grande inspiration. Retiens. Longue expiration. Aaahhh. Relâche toute la tension de la journée.

Une dernière fois. Inspire profondément. Retiens brièvement. Expire complètement. Relâche tout.

Maintenant, laisse ta respiration reprendre son rythme naturel. Lent. Régulier. Paisible. Tu n'as plus rien à contrôler. Observe simplement ton souffle qui entre et qui sort.

Nous allons maintenant détendre ton corps complètement, de la tête aux pieds.

Porte ton attention sur ton front. Ressens les muscles de ton front. Et maintenant, laisse-les se détendre complètement. Ton front devient lisse. Détendu. Lourd.

Tes sourcils se relâchent. L'espace entre tes sourcils s'adoucit.

Tes yeux, derrière tes paupières closes, se détendent. Tes globes oculaires deviennent lourds. Ils s'enfoncent doucement dans leurs orbites. Détendus. Si détendus.

Tes paupières sont lourdes. Si lourdes. Elles ne veulent plus bouger.

Tes joues se relâchent. Tes pommettes s'affaissent légèrement.

Ta mâchoire se détend. Laisse un petit espace entre tes dents du haut et tes dents du bas. Ta langue se détend dans ta bouche. Elle devient molle. Lourde.

Tes lèvres se relâchent. Légèrement entrouvertes peut-être.

Tout ton visage est maintenant complètement détendu. Sans tension. Sans expression. Paisible.

Ton cou se détend. Laisse ta tête s'enfoncer dans l'oreiller. Elle est lourde. Si lourde.

Tes épaules se relâchent. Elles s'affaissent. Elles descendent loin de tes oreilles. Toute la tension accumulée dans tes épaules se dissout. S'évapore.

Tes bras deviennent lourds. Ton bras droit est lourd. Ton bras gauche est lourd. Ils s'enfoncent dans le matelas.

Tes coudes se détendent. Tes avant-bras deviennent mous. Lourds.

Tes poignets se relâchent. Tes mains sont lourdes. Si lourdes qu'elles ne peuvent plus bouger.

Tes doigts sont détendus. Chaque doigt, l'un après l'autre. Lourd. Détendu. Abandonné.

Ton torse se détend maintenant. Ta poitrine s'affaisse légèrement à chaque expiration. Ton cœur bat calmement. Régulièrement.

Ton ventre se relâche complètement. Il n'y a plus besoin de le rentrer. Laisse-le être. Mou. Détendu.

Ton dos s'enfonce dans le matelas. Chaque vertèbre se détend. Du haut de ta colonne jusqu'au bas. Détente. Détente. Détente.

Ton bassin est lourd. Tes fesses s'enfoncent dans le matelas. Lourdes. Détendues.

Tes hanches se relâchent. Tes cuisses deviennent molles. Lourdes. Ton cuisse droite est lourde. Ta cuisse gauche est lourde.

Tes genoux se détendent. Tes mollets sont lourds. Ton mollet droit. Ton mollet gauche. Si lourds qu'ils s'enfoncent dans le matelas.

Tes chevilles se relâchent. Tes pieds sont lourds. Ton pied droit est lourd. Ton pied gauche est lourd.

Tes orteils se détendent. Chaque orteil. Lourd. Mou. Détendu.

Ton corps entier est maintenant complètement détendu. De la tête aux pieds. Lourd. Abandonné. Tu ne peux même plus bouger. Tu n'as même plus envie de bouger. C'est si agréable d'être si détendu.

Maintenant, nous allons apaiser ton esprit.

Imagine que tu es allongé sur une plage, au crépuscule. Le ciel est magnifique. Rose. Orange. Violet. Les derniers rayons du soleil réchauffent doucement ta peau.

Le sable sous toi est encore chaud de la journée. Il épouse parfaitement les courbes de ton corps. Tu t'enfonces légèrement dans ce sable doux.

Tu entends les vagues. Doucement. Régulièrement. Elles viennent caresser le rivage. Chuuuu. Et elles repartent. Shhhhh. Chuuuu. Shhhhh.

Ce rythme des vagues est hypnotique. Apaisant. Il ralentit naturellement ta respiration. Ton cœur bat au rythme des vagues.

Chaque vague qui se retire emporte avec elle les pensées de ta journée. Les soucis. Les préoccupations. Tout s'en va avec l'eau. Chuuuu. Parti. Shhhhh.

L'air est doux. Agréable. Une légère brise caresse ton visage. Tes cheveux. Si agréable.

Le soleil descend doucement vers l'horizon. Le ciel devient de plus en plus sombre. De plus en plus apaisant.

Les premières étoiles apparaissent. Une. Puis deux. Puis trois. Elles scintillent doucement dans le ciel qui s'assombrit.

Tu te sens en parfaite sécurité sur cette plage. Rien ni personne ne peut te déranger. C'est ton sanctuaire. Ton havre de paix.

La lune commence à se lever. Une belle lune pleine. Argentée. Elle illumine doucement la plage. L'océan. Toi.

Cette lumière de lune est apaisante. Douce. Elle enveloppe ton corps d'une couverture invisible de paix.

Les vagues continuent leur danse. Chuuuu. Shhhhh. Chuuuu. Shhhhh. Elles murmurent : "Dors. Dors. Dors."

Ton corps s'enfonce encore plus profondément dans le sable chaud. Tu es si lourd maintenant. Si détendu. Si paisible.

Tes pensées deviennent de plus en plus lentes. De plus en plus espacées. Comme les vagues. Qui viennent. De temps en temps. Et repartent.

Tu es entre la veille et le sommeil. Dans cet espace doux. Agréable. Paisible.

Laisse-toi glisser. Il n'y a rien à faire. Juste se laisser aller.

Les vagues continuent. Chuuuu. Shhhhh.

La lune brille doucement.

Les étoiles scintillent.

Tu es en sécurité.

Tu es aimé.

Tu es paisible.

Dors maintenant.

Doux rêves.

Bonne nuit.

Namaste.
"""
    },

    {
        'title': 'Calmer l\'Anxiété du Soir',
        'description': 'Apaise ton mental agité et retrouve la sérénité pour une nuit paisible.',
        'theme': 'sommeil',
        'duration_minutes': 6,
        'script': """
Bonsoir. Si tu écoutes cette méditation, c'est peut-être que ton esprit est agité ce soir. Que les pensées tournent en boucle. Que l'anxiété est présente.

C'est ok. Tu es au bon endroit.

Installe-toi confortablement dans ton lit. Allonge-toi dans ta position préférée pour dormir.

Ferme les yeux doucement.

Prends une grande inspiration par le nez. Et expire longuement par la bouche. Relâche.

Encore. Inspire. Expire. Relâche.

Une dernière fois. Inspire profondément. Expire complètement. Laisse tout partir.

Maintenant, observe simplement ta respiration naturelle. N'essaie pas de la changer. Observe-la juste.

Je sais que ton esprit est peut-être en ébullition en ce moment. Les pensées se bousculent. Les inquiétudes sont là.

Mais ici, maintenant, tu es en sécurité. Dans ton lit. Sous ta couverture. À l'abri. Protégé.

Ici, maintenant, rien ne peut t'arriver. Les soucis de demain sont pour demain. Les regrets d'hier sont passés. Ici, maintenant, tu es en sécurité.

Répète mentalement : "Je suis en sécurité. Ici et maintenant, je suis en sécurité."

Encore : "Je suis en sécurité."

Imagine maintenant que chaque pensée anxieuse est comme un nuage dans le ciel de ton esprit.

Ces nuages passent. Ils viennent. Ils passent. Ils s'en vont. Ils reviennent peut-être. Ils repartent. C'est leur nature.

Tu n'as pas besoin de les retenir. Tu n'as pas besoin de les combattre. Laisse-les passer. Comme des nuages dans le ciel.

Toi, tu es le ciel. Vaste. Paisible. Infini. Les nuages passent mais le ciel reste. Toujours là. Toujours paisible.

À chaque expiration, imagine que tu relâches un nuage. Il s'en va. Il s'éloigne. Il disparaît à l'horizon.

Expire. Relâche. Le nuage part.

Encore. Expire. Relâche. Un autre nuage s'en va.

Continue. À ton rythme. Chaque expiration libère un nuage de pensée anxieuse.

Imagine maintenant qu'une lumière douce, d'un bleu clair apaisant, descend vers toi. Comme la lumière de la lune. Douce. Apaisante. Sécurisante.

Cette lumière bleue t'enveloppe complètement. Comme une couverture de paix. De sérénité. De calme.

Tu es en sécurité dans cette lumière. L'anxiété ne peut pas t'atteindre ici.

Cette lumière bleue entre maintenant dans ton corps. Par le sommet de ta tête. Elle descend. Doucement. Lentement.

Elle arrive à ton front. Ton front se détend. Les rides d'inquiétude s'effacent.

Elle descend à tes yeux. Tes paupières deviennent lourdes. Si lourdes.

Elle arrive à ta poitrine. À ton cœur. Ton cœur se calme. Les battements ralentissent. Tout va bien.

Elle descend à ton ventre. Ce nœud dans ton ventre commence à se défaire. À se dissoudre dans la lumière bleue.

Respire dans ton ventre. Laisse-le se gonfler à l'inspiration. Se dégonfler à l'expiration. Détends ton ventre. Tout va bien.

La lumière bleue continue de descendre dans tout ton corps. Jusqu'au bout de tes orteils.

Tu es complètement enveloppé. À l'intérieur et à l'extérieur. Dans cette lumière bleue apaisante.

Répète mentalement : "Je lâche prise. Je fais confiance. Tout va bien."

Encore : "Je lâche prise. Je fais confiance. Tout va bien."

Tu n'as pas besoin de tout comprendre ce soir. Tu n'as pas besoin de tout résoudre ce soir. Ce soir, tu as juste besoin de te reposer.

Demain, tu verras les choses plus clairement. Demain, tu trouveras des solutions. Mais ce soir, maintenant, repose-toi.

Confie tes soucis à l'univers. À ton inconscient. À ta sagesse intérieure. Ils vont s'en occuper pendant que tu dors.

Toi, maintenant, tu peux te reposer.

Sens ton corps devenir de plus en plus lourd. De plus en plus détendu.

Ton esprit devient de plus en plus calme. De plus en plus paisible.

Les pensées ralentissent. S'espacent. Comme les vagues qui se calment après la tempête.

Laisse-toi glisser maintenant vers le sommeil.

Tu es en sécurité.

Tu es aimé.

Tu es paisible.

Tout va bien.

Dors maintenant.

Bonne nuit.

Namaste.
"""
    }
]


def migrate_meditations():
    """Remplace les anciennes méditations par les nouvelles"""
    with app.app_context():
        print('🔄 Migration des méditations...\n')

        # Compter les anciennes méditations
        old_count = Meditation.query.count()
        print(f'📊 Anciennes méditations trouvées: {old_count}')

        if old_count > 0:
            print('🗑️  Suppression des anciennes méditations...')
            Meditation.query.delete()
            db.session.commit()
            print('✅ Anciennes méditations supprimées\n')

        # Ajouter les nouvelles méditations
        print('➕ Ajout des nouvelles méditations (scripts longs)...\n')
        for med_data in MEDITATIONS:
            meditation = Meditation(
                title=med_data['title'],
                description=med_data['description'],
                theme=med_data['theme'],
                duration_minutes=med_data['duration_minutes'],
                script=med_data['script']
            )
            db.session.add(meditation)
            print(f'✅ {med_data["title"]} ({med_data["theme"]} - {med_data["duration_minutes"]}min)')

        db.session.commit()

        new_count = Meditation.query.count()
        print(f'\n✨ Migration terminée ! {new_count} méditations en base.')
        print('📝 Les nouvelles méditations ont des scripts beaucoup plus longs et réalistes.')


if __name__ == '__main__':
    migrate_meditations()

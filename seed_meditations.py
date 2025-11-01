"""
Script pour peupler la base de données avec des méditations initiales

Usage: python seed_meditations.py
"""
from app import create_app
from app.models import db, Meditation

app = create_app()

# Définir les méditations initiales
MEDITATIONS = [
    # CHAKRAS
    {
        'title': 'Équilibrage des 7 Chakras',
        'description': 'Voyage énergétique à travers tes 7 centres d\'énergie pour les harmoniser et les aligner.',
        'theme': 'chakras',
        'duration_minutes': 20,
        'script': """
Installe-toi confortablement, assis ou allongé. Ferme doucement les yeux.

Commence par prendre trois respirations profondes... Inspire par le nez... Expire par la bouche...

Visualise maintenant une lumière rouge éclatante à la base de ta colonne vertébrale... C'est ton chakra racine, Muladhara... Il t'ancre à la terre... Sens cette énergie rouge tourner et briller...

Laisse maintenant cette lumière monter légèrement... Elle devient orange, juste sous ton nombril... C'est Svadhisthana, ton chakra sacré... Centre de ta créativité et de tes émotions... Laisse cette lumière orange danser et circuler librement...

L'énergie continue de monter... Au niveau de ton plexus solaire, elle devient d'un jaune doré éclatant... Manipura, ton centre de pouvoir personnel... Sens ta confiance grandir avec cette lumière jaune qui rayonne...

Cette lumière monte encore... Au centre de ta poitrine, elle devient d'un vert émeraude magnifique... Anahata, ton chakra du cœur... Ressens l'amour inconditionnel qui émane de ce centre... Envoie-toi de la compassion...

Maintenant, la lumière arrive à ta gorge, devenant d'un bleu azur... Vishuddha, ton chakra de la communication... Sens ta vérité personnelle prête à s'exprimer...

Cette énergie monte à ton troisième œil, entre tes sourcils, devenant indigo profond... Ajna, ton centre d'intuition... Fais confiance à ta sagesse intérieure...

Enfin, au sommet de ta tête, la lumière devient d'un violet ou blanc étincelant... Sahasrara, ton chakra couronne... Tu es connecté à l'univers tout entier...

Maintenant, visualise toutes ces couleurs qui brillent ensemble, formant un arc-en-ciel de lumière à travers ton corps... Tous tes chakras sont alignés, équilibrés, en harmonie parfaite...

Reste dans cette sensation d'équilibre quelques instants...

Quand tu es prêt, ramène doucement ta conscience dans la pièce... Bouge tes doigts et tes orteils... Ouvre les yeux en douceur...

Namaste.
"""
    },
    {
        'title': 'Activation du Chakra du Cœur',
        'description': 'Méditation centrée sur Anahata pour cultiver l\'amour de soi et la compassion.',
        'theme': 'chakras',
        'duration_minutes': 10,
        'script': """
Assieds-toi confortablement, le dos droit mais détendu. Ferme les yeux.

Porte ton attention sur ta respiration naturelle... Observe l'air qui entre et qui sort...

Maintenant, place ta main droite sur ton cœur... Sens la chaleur de ta paume sur ta poitrine...

Inspire profondément et imagine une lumière verte émeraude qui commence à briller au centre de ta poitrine... C'est ton chakra du cœur, Anahata...

À chaque inspiration, cette lumière verte grandit, devient plus brillante... À chaque expiration, elle rayonne autour de toi...

Répète mentalement : "Je suis amour... Je mérite l'amour... Je donne et je reçois l'amour librement..."

Pense à quelqu'un que tu aimes profondément... Ressens cet amour grandir dans ton cœur, comme une chaleur douce...

Maintenant, dirige cet amour vers toi-même... Envoie-toi la même compassion, la même tendresse...

Si des émotions surgissent, accueille-les avec bienveillance... Ton cœur est un espace sûr...

Visualise cette lumière verte qui s'étend maintenant dans tout ton corps... Puis au-delà de ton corps, remplissant la pièce... Ton amour touche tout ce qui t'entoure...

Prends encore trois respirations profondes dans cette énergie d'amour...

Doucement, ramène ta conscience ici et maintenant... Enlève ta main de ton cœur...

Ouvre les yeux quand tu es prêt... Garde cette lumière d'amour avec toi aujourd'hui...

Namaste.
"""
    },

    # MANIFESTATION
    {
        'title': 'Manifester tes Intentions',
        'description': 'Utilise la loi de l\'attraction pour clarifier et attirer tes désirs les plus profonds.',
        'theme': 'manifestation',
        'duration_minutes': 15,
        'script': """
Installe-toi dans une position confortable... Ferme les yeux et prends plusieurs respirations profondes...

Laisse ton corps se détendre complètement... Relâche toutes les tensions...

Commence par clarifier ton intention... Qu'est-ce que tu souhaites manifester dans ta vie ? Ne censure pas, laisse venir...

Visualise maintenant cette intention déjà réalisée... Tu ES déjà là où tu veux être... Que vois-tu autour de toi ? Qui est avec toi ?

Ressens les émotions de cette réalisation... La joie, la gratitude, la fierté, l'amour... Laisse ces émotions remplir tout ton être...

Maintenant, imagine une lumière dorée qui descend du ciel et t'enveloppe complètement... C'est l'énergie de l'univers qui soutient ta manifestation...

Répète mentalement : "Je suis aligné avec mes désirs... L'univers conspire en ma faveur... Tout vient à moi au moment parfait..."

Visualise des portes qui s'ouvrent sur ton chemin... Des opportunités qui se présentent... Des rencontres qui se font...

Ressens la certitude que ce que tu désires est déjà en route vers toi... Pas d'espoir, pas de doute... Juste la certitude...

Prends un moment pour remercier l'univers... Merci pour ce qui vient... Merci pour ce qui est... Merci pour ce qui était...

Cette gratitude amplifie ta vibration et accélère ta manifestation...

Prends trois respirations profondes... Ancre cette énergie de manifestation dans ton corps...

Quand tu te sens prêt, ouvre doucement les yeux... Agis aujourd'hui comme si ta manifestation était déjà en cours...

Et ainsi soit-il.
"""
    },
    {
        'title': 'Élever ta Vibration',
        'description': 'Augmente ta fréquence énergétique pour attirer des expériences positives et alignées.',
        'theme': 'manifestation',
        'duration_minutes': 10,
        'script': """
Assieds-toi confortablement et ferme les yeux...

Commence par scanner ton corps... Où sens-tu des tensions ? Des lourdeurs ? Prends-en simplement conscience...

Maintenant, imagine que tu es comme une note de musique... Quelle est ta fréquence en ce moment ? Grave, aiguë, quelque part entre les deux ?

À chaque inspiration, imagine que tu montes d'une note... Ta vibration s'élève... Tu deviens plus léger...

Pense à quelque chose qui te remplit de joie... Un souvenir heureux, un être aimé, un lieu magique... Ressens cette joie vibrer dans ton corps...

Cette joie élève naturellement ta fréquence... Tu deviens comme une lumière qui brille de plus en plus fort...

Répète : "Je choisis la joie... Je choisis l'amour... Je choisis la lumière... Ma vibration est élevée et positive..."

Visualise maintenant que tu attires à toi des choses et des personnes qui vibrent à la même fréquence... Comme un aimant puissant...

Reste dans cette haute vibration quelques instants... Savoure cette sensation...

Prends l'intention de garder cette fréquence élevée tout au long de ta journée... Dès que tu te sens lourd, rappelle-toi cette méditation...

Respire profondément trois fois... Ancre cette vibration haute...

Ouvre les yeux doucement... Souris... Ta vibration est élevée... Tout est possible...

Namaste.
"""
    },

    # GUÉRISON
    {
        'title': 'Guérison Intérieure Profonde',
        'description': 'Libère les blessures émotionnelles et retrouve ta lumière intérieure.',
        'theme': 'guérison',
        'duration_minutes': 20,
        'script': """
Allonge-toi confortablement... Ferme les yeux... Laisse ton corps s'enfoncer dans le sol...

Prends plusieurs respirations profondes... À chaque expiration, relâche un peu plus...

Porte maintenant ton attention sur ton cœur... Y a-t-il une tristesse ? Une douleur ? Une blessure ? Ne la rejette pas... Accueille-la avec douceur...

Donne une forme à cette blessure dans ton esprit... Une couleur... Une texture... Observe-la sans jugement...

Dis mentalement à cette partie blessée de toi : "Je te vois... Je t'accepte... Tu as le droit d'exister..."

Imagine maintenant une lumière dorée et chaude qui descend du ciel... C'est une lumière de guérison pure...

Cette lumière entre par le sommet de ta tête et descend lentement dans ton corps... Elle arrive à ton cœur...

La lumière enveloppe ta blessure avec tant d'amour, tant de compassion... Elle ne la juge pas, elle la berce doucement...

Ta blessure commence à se transformer... La douleur se dissout peu à peu dans la lumière... Laisse ce processus se faire naturellement...

Si des larmes viennent, laisse-les couler... Elles sont la libération dont tu as besoin...

Répète : "Je me pardonne... Je libère le passé... Je mérite de guérir... Je mérite d'être heureux..."

La lumière dorée remplit maintenant tout ton être... Là où il y avait de la douleur, il y a maintenant de la paix...

Ressens cette paix profonde... Cette liberté nouvelle... Tu as fait un travail important aujourd'hui...

Prends trois respirations de gratitude... Merci à ton corps, à ton cœur, à ton âme...

Quand tu es prêt, bouge doucement... Ouvre les yeux en douceur...

Tu es guéri un peu plus aujourd'hui... Continue ce chemin avec patience et amour...

Namaste.
"""
    },
    {
        'title': 'Libération Émotionnelle',
        'description': 'Relâche les émotions bloquées et retrouve ta légèreté intérieure.',
        'theme': 'guérison',
        'duration_minutes': 12,
        'script': """
Assieds-toi confortablement, le dos droit... Ferme les yeux...

Commence par scanner ton corps... Où sens-tu des tensions ? Des nœuds ? Des blocages ?

Ces zones sont souvent des émotions non exprimées... De la colère, de la tristesse, de la peur qui se sont logées dans ton corps...

Choisis une zone qui attire ton attention... Respire dans cette zone... Envoie ton souffle directement là où c'est tendu...

Demande mentalement à cette tension : "Que veux-tu me dire ? Quelle émotion portes-tu ?"

Écoute la réponse... Elle peut venir sous forme d'image, de mot, de sensation...

Quelle que soit cette émotion, dis-lui : "Bienvenue... Tu peux sortir maintenant... Je te libère avec amour..."

À chaque expiration, imagine que cette émotion s'évacue de ton corps comme une fumée sombre... Elle part, doucement mais sûrement...

À chaque inspiration, imagine une lumière blanche pure qui remplit cet espace libéré... Fraîcheur... Légèreté...

Continue ce processus... Expire la lourdeur... Inspire la lumière...

Sens ton corps devenir plus léger... Plus libre... Comme si des chaînes invisibles se brisaient...

Place une main sur ton cœur et répète : "Je libère ce qui ne me sert plus... Je fais de la place pour la joie... Je suis libre..."

Prends un moment pour apprécier cette nouvelle légèreté... Souris intérieurement...

Trois respirations profondes pour ancrer cette libération...

Ouvre les yeux quand tu te sens prêt... Tu es plus léger... Tu es libre...

Namaste.
"""
    },

    # SOMMEIL
    {
        'title': 'Voyage vers un Sommeil Profond',
        'description': 'Détends complètement ton corps et ton esprit pour t\'endormir paisiblement.',
        'theme': 'sommeil',
        'duration_minutes': 25,
        'script': """
Allonge-toi confortablement dans ton lit... Arrange tes oreillers... Trouve ta position préférée pour dormir...

Ferme doucement les yeux... Tu n'as rien d'autre à faire qu'à te laisser porter...

Commence par prendre trois respirations très lentes et profondes... Inspire par le nez... Expire longuement par la bouche...

Maintenant, laisse ta respiration reprendre son rythme naturel... Observe-la simplement, sans la contrôler...

Porte ton attention sur tes orteils... Contracte-les légèrement... Et relâche complètement... Sens-les devenir lourds, si lourds...

Tes pieds maintenant... Contracte... Et relâche... Ils s'enfoncent dans le matelas...

Tes mollets... Contracte... Relâche... Une vague de détente monte dans tes jambes...

Tes cuisses... Contracte... Relâche... Tes jambes sont complètement abandonnées...

Ton bassin, ton ventre... Contracte légèrement... Et laisse tout s'assouplir... Ta respiration est douce et calme...

Ta poitrine, tes épaules... Contracte... Relâche... Sens les tensions s'évacuer...

Tes bras, tes mains, tes doigts... Contracte... Relâche... Ils sont lourds, si lourds...

Ton cou, ta mâchoire... Contracte... Relâche... Laisse ta langue se détendre dans ta bouche...

Ton visage, ton front... Contracte... Relâche... Toute expression disparaît de ton visage...

Ton corps entier est maintenant complètement détendu... Lourd... Abandonné au matelas...

Imagine-toi maintenant sur une plage au coucher du soleil... Le ciel est rose et orange... Le sable est chaud sous toi...

Tu entends le bruit des vagues... Chaque vague qui se retire emporte avec elle tes pensées, tes soucis...

Le rythme des vagues est apaisant... Régulier... Comme une berceuse naturelle...

Tu es en parfaite sécurité... Rien ni personne ne peut te déranger ici... C'est ton sanctuaire de paix...

Les étoiles commencent à apparaître dans le ciel... Une à une... Elles scintillent doucement...

Tu te sens entouré par l'amour de l'univers... Protégé... En paix...

Ta respiration ralentit encore... Ton corps s'enfonce plus profondément dans le sable chaud...

Chaque vague qui arrive murmure : "Dors... Dors... Dors..."

Laisse-toi glisser dans le sommeil... Il n'y a rien à faire... Juste se laisser aller...

Doux rêves... Namaste...

(Silence prolongé pour permettre l'endormissement)
"""
    },
    {
        'title': 'Relaxation du Corps et de l\'Esprit',
        'description': 'Calme ton mental et prépare ton corps à une nuit réparatrice.',
        'theme': 'sommeil',
        'duration_minutes': 15,
        'script': """
Installe-toi confortablement dans ton lit... Éteins toutes les lumières...

Ferme les yeux et prends une grande inspiration... Expire longuement en laissant sortir toutes les tensions de la journée...

Imagine qu'une lumière douce et apaisante, comme celle de la lune, entre dans ta chambre...

Cette lumière argentée descend lentement sur ton corps, comme un voile de soie...

Elle touche d'abord ton front... Ton front se détend complètement... Toutes les pensées se calment...

La lumière descend sur tes yeux... Tes paupières deviennent si lourdes... Si lourdes...

Elle continue sur tes joues, ta mâchoire... Ton visage est paisible, sans expression...

La lumière argentée enveloppe maintenant ta gorge, tes épaules... Elles s'affaissent, libérées de tout poids...

Elle descend sur ta poitrine... Ta respiration est lente, profonde, apaisée...

Sur ton ventre... Ton ventre se détend à chaque expiration...

Sur tes jambes... Elles sont lourdes, si lourdes qu'elles s'enfoncent dans le matelas...

Sur tes pieds... Tes pieds se réchauffent doucement...

Ton corps entier est maintenant enveloppé dans cette lumière argentée apaisante... Tu es comme dans un cocon de douceur...

Si des pensées arrivent, laisse-les passer comme des nuages dans le ciel... Ne les retiens pas... Laisse-les s'éloigner...

Compte lentement à rebours de dix à un... À chaque nombre, tu t'enfonces plus profondément dans la détente...

Dix... Neuf... Huit... Sept... Six... Cinq... Quatre... Trois... Deux... Un...

Tu es prêt pour une nuit de sommeil profond et réparateur...

Bonne nuit... Namaste...
"""
    }
]


def seed_meditations():
    """Ajoute les méditations initiales en base de données"""
    with app.app_context():
        print('🧘 Ajout des méditations initiales...')

        # Vérifier si des méditations existent déjà
        existing_count = Meditation.query.count()
        if existing_count > 0:
            print('⚠️  Il y a déjà {} méditation(s) en base.'.format(existing_count))
            response = input('Voulez-vous quand même ajouter ces méditations ? (y/n): ')
            if response.lower() != 'y':
                print('❌ Annulé.')
                return

        # Ajouter chaque méditation
        added = 0
        for med_data in MEDITATIONS:
            # Vérifier si cette méditation existe déjà (par titre)
            existing = Meditation.query.filter_by(title=med_data['title']).first()
            if existing:
                print('⏭️  "{}" existe déjà, ignorée.'.format(med_data['title']))
                continue

            meditation = Meditation(
                title=med_data['title'],
                description=med_data['description'],
                theme=med_data['theme'],
                duration_minutes=med_data['duration_minutes'],
                script=med_data['script']
            )
            db.session.add(meditation)
            added += 1
            print('✅ Ajoutée: {} ({} - {}min)'.format(
                med_data['title'],
                med_data['theme'],
                med_data['duration_minutes']
            ))

        if added > 0:
            db.session.commit()
            print('\n✨ {} méditation(s) ajoutée(s) avec succès !'.format(added))
        else:
            print('\n💡 Aucune nouvelle méditation ajoutée.')


if __name__ == '__main__':
    seed_meditations()

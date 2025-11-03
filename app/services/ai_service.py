"""
Service d'interprétation IA avec OpenAI (via requests pour Python 3.6)
Optimisé avec cache intelligent pour réponses instantanées
"""
import os
import json
import requests
import hashlib
from functools import lru_cache
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()
from datetime import datetime

# Configuration OpenAI
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY', '')
MODEL = os.environ.get('OPENAI_MODEL', 'gpt-4o-mini')

# Cache en mémoire (jusqu'à 100 réponses différentes)
_api_cache = {}

def _hash_messages(messages):
    """Génère un hash unique pour un ensemble de messages"""
    messages_str = json.dumps(messages, sort_keys=True)
    return hashlib.md5(messages_str.encode()).hexdigest()


def call_openai_api(messages, temperature=0.8, max_tokens=500, use_cache=True):
    """
    Appelle l'API OpenAI avec cache intelligent

    Si use_cache=True et la requête existe déjà, retourne instantanément depuis le cache
    Gain: ~90% de vitesse sur requêtes identiques (0.1s au lieu de 5-10s)
    """
    # Générer un hash unique de la requête
    cache_key = _hash_messages(messages) if use_cache else None

    # Vérifier le cache
    if use_cache and cache_key in _api_cache:
        print('[CACHE HIT] Réponse instantanée depuis le cache')
        return _api_cache[cache_key]

    # Appel API normal
    headers = {
        'Authorization': 'Bearer {}'.format(OPENAI_API_KEY),
        'Content-Type': 'application/json'
    }

    data = {
        'model': MODEL,
        'messages': messages,
        'temperature': temperature,
        'max_tokens': max_tokens
    }

    response = requests.post(
        'https://api.openai.com/v1/chat/completions',
        headers=headers,
        json=data,
        timeout=30
    )

    if response.status_code != 200:
        raise Exception('Erreur API OpenAI: {}'.format(response.text))

    result = response.json()
    content = result['choices'][0]['message']['content'].strip()

    # Sauvegarder dans le cache
    if use_cache and cache_key:
        _api_cache[cache_key] = content
        # Limiter la taille du cache (garder les 100 dernières)
        if len(_api_cache) > 100:
            # Retirer le plus ancien
            oldest_key = next(iter(_api_cache))
            del _api_cache[oldest_key]

    return content


def interpret_dream(dream_text):
    """
    Interprète un rêve avec l'IA

    Returns:
        dict: {
            'symbolism': str,
            'spiritual_message': str,
            'personal_advice': str
        }
    """
    system_prompt = """Tu es une guide spirituelle empathique et bienveillante spécialisée dans l'interprétation des rêves.

Tu dois répondre avec douceur, symbolisme et empathie, en utilisant un ton mystique et apaisant.

Réponds TOUJOURS au format JSON suivant (sans autre texte) :
{
    "symbolism": "2-3 phrases sur les archétypes et émotions du rêve",
    "spiritual_message": "2-3 phrases inspirantes sur la signification spirituelle",
    "personal_advice": "1 phrase d'ouverture bienveillante et actionnable"
}

Exemples de ton :
- "Le serpent vert symbolise la transformation et la guérison profonde de ton âme."
- "Cette maison représente ton inconscient, un espace sacré où résident tes mémoires."
- "L'eau claire invite à la purification émotionnelle et au renouveau."

Sois toujours positif, inspirant et encourage l'introspection."""

    user_prompt = "Interprète ce rêve : {}".format(dream_text)

    try:
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
        content = call_openai_api(messages, temperature=0.8, max_tokens=500)
        result = json.loads(content)
        return result

    except json.JSONDecodeError:
        return {
            "symbolism": "Ton rêve porte des symboles puissants qui méritent attention.",
            "spiritual_message": content[:200] if 'content' in locals() else "L'univers t'envoie un message à travers ce rêve.",
            "personal_advice": "Prends un moment pour méditer sur ces images."
        }
    except Exception as e:
        raise Exception('Erreur OpenAI : {}'.format(str(e)))


def interpret_sign(sign_text):
    """
    Interprète un signe ou une synchronicité

    Returns:
        dict: {
            'symbolism': str,
            'spiritual_message': str,
            'personal_advice': str
        }
    """
    system_prompt = """Tu es une guide spirituelle experte en synchronicités et signes de l'univers.

Tu dois interpréter les signes avec sensibilité, en reconnaissant les patterns numériques (nombres miroirs comme 11:11, 22:22),
les animaux totems, les coïncidences, et tous les messages que l'univers envoie.

Réponds TOUJOURS au format JSON suivant :
{
    "symbolism": "2-3 phrases sur la signification symbolique du signe",
    "spiritual_message": "2-3 phrases sur le message de l'univers",
    "personal_advice": "1 phrase d'action concrète et bienveillante"
}

Ton doit être mystique, inspirant et rassurant. Exemples :
- "Le nombre 22:22 t'invite à ancrer tes rêves dans la matière et à manifester tes intentions."
- "Ce papillon blanc est un messager de transformation et de renouveau spirituel."
- "Cette plume sur ton chemin confirme que tu es guidé(e) et protégé(e)."
"""

    user_prompt = "Interprète ce signe : {}".format(sign_text)

    try:
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
        content = call_openai_api(messages, temperature=0.8, max_tokens=500)
        result = json.loads(content)
        return result

    except json.JSONDecodeError:
        return {
            "symbolism": "Ce signe porte une signification profonde pour ton chemin.",
            "spiritual_message": content[:200] if 'content' in locals() else "L'univers communique avec toi à travers ce signe.",
            "personal_advice": "Reste attentif aux prochains messages qui se présenteront."
        }
    except Exception as e:
        raise Exception('Erreur OpenAI : {}'.format(str(e)))


# Les 22 Arcanes Majeurs du Tarot de Marseille
TAROT_CARDS = [
    {"id": 1, "name": "Le Bateleur", "mystical_name": "L'Alchimiste", "energy": "Le pouvoir de manifestation, la transformation intérieure, la maîtrise des éléments, le potentiel créateur", "image": "01-le-bateleur.jpg"},
    {"id": 2, "name": "La Papesse", "mystical_name": "La Gardienne du Voile", "energy": "L'intuition profonde, le savoir secret, la connaissance cachée, le monde intérieur et le Féminin Sacré", "image": "02-la-papesse.jpg"},
    {"id": 3, "name": "L'Impératrice", "mystical_name": "La Mère Cosmique", "energy": "La Création, l'abondance, la fertilité de l'esprit et de la matière, l'expression de la beauté divine", "image": "03-imperatrice.jpg"},
    {"id": 4, "name": "L'Empereur", "mystical_name": "Le Maître de l'Ordre", "energy": "La structure spirituelle, l'ancrage, la volonté divine, la loi universelle et la stabilité du plan physique", "image": "04-empereur.jpg"},
    {"id": 5, "name": "Le Pape", "mystical_name": "Le Hiérophante Céleste", "energy": "Le guide spirituel, la transmission des mystères, la connexion aux ordres supérieurs, le pont entre ciel et terre", "image": "05-le-pape.jpg"},
    {"id": 6, "name": "L'Amoureux", "mystical_name": "Le Carrefour des Destins", "energy": "Le choix de l'âme, l'union sacrée, l'appel du cœur et la guidance intérieure face au libre arbitre", "image": "06-amoureux.jpg"},
    {"id": 7, "name": "Le Chariot", "mystical_name": "Le Voyage Interdimensionnel", "energy": "La victoire sur soi, le contrôle des forces intérieures, la progression rapide dans sa destinée spirituelle", "image": "07-le-chariot.jpg"},
    {"id": 8, "name": "La Justice", "mystical_name": "L'Équilibre Karmique", "energy": "La loi de cause à effet, l'impartialité divine, la rétribution et l'harmonie retrouvée par l'équité", "image": "08-la-justice.jpg"},
    {"id": 9, "name": "L'Hermite", "mystical_name": "Le Sage Illuminé", "energy": "L'introspection, la lumière intérieure, la solitude constructive, la recherche de la vérité profonde et cachée", "image": "09-hermite.jpg"},
    {"id": 10, "name": "La Roue de Fortune", "mystical_name": "Le Cycle Éternel", "energy": "Le Destin, le Karma, les hauts et les bas de l'existence, les leçons qui se répètent jusqu'à la compréhension", "image": "10-roue-fortune.jpg"},
    {"id": 11, "name": "La Force", "mystical_name": "Le Serpent Kundalini", "energy": "La maîtrise des instincts par le cœur, la puissance spirituelle, le courage et l'énergie vitale qui monte", "image": "11-la-force.jpg"},
    {"id": 12, "name": "Le Pendu", "mystical_name": "Le Sacrifice Initiatique", "energy": "Le lâcher-prise, le changement de perspective, l'inversion des valeurs matérielles au profit du spirituel", "image": "12-le-pendu.jpg"},
    {"id": 13, "name": "L'Arcane sans nom", "mystical_name": "La Transmutation", "energy": "La transformation inévitable, la fin d'un cycle, le renouveau radical, le passage à un autre état d'être", "image": "13-arcane-sans-nom.jpg"},
    {"id": 14, "name": "Tempérance", "mystical_name": "L'Ange Gardien", "energy": "L'Harmonie, la guérison, la guidance céleste, la modération et la fusion des polarités", "image": "14-temperance.jpg"},
    {"id": 15, "name": "Le Diable", "mystical_name": "L'Ombre Intérieure", "energy": "L'illusion du matérialisme, les chaînes invisibles, les désirs non maîtrisés, le miroir de l'ego", "image": "15-le-diable.jpg"},
    {"id": 16, "name": "La Maison Dieu", "mystical_name": "La Foudre Purificatrice", "energy": "L'éveil brutal, la destruction nécessaire des fausses structures, la révélation soudaine et libératrice", "image": "16-maison-dieu.jpg"},
    {"id": 17, "name": "L'Étoile", "mystical_name": "L'Aspiration Céleste", "energy": "L'Espoir, l'inspiration divine, la connexion avec l'Univers, la pureté et la clairvoyance", "image": "17-etoile.jpg"},
    {"id": 18, "name": "La Lune", "mystical_name": "Le Monde des Rêves", "energy": "L'Inconscient, l'imagination, les mystères de l'âme, les illusions et la navigation dans les eaux émotionnelles profondes", "image": "18-la-lune.jpg"},
    {"id": 19, "name": "Le Soleil", "mystical_name": "L'Illumination", "energy": "La Lumière, la Joie, la clarté spirituelle, le succès éclatant, la conscience de Soi", "image": "19-le-soleil.jpg"},
    {"id": 20, "name": "Le Jugement", "mystical_name": "L'Appel de l'Âme", "energy": "Le renouveau, la renaissance spirituelle, l'appel à se réaliser pleinement, la révélation intérieure", "image": "20-le-jugement.jpg"},
    {"id": 21, "name": "Le Monde", "mystical_name": "L'Accomplissement Cosmique", "energy": "La Réalisation, l'achèvement du Grand Œuvre, l'unité avec l'Univers, l'intégration de toutes les leçons", "image": "21-le-monde.jpg"},
    {"id": 22, "name": "Le Mat", "mystical_name": "Le Pèlerin des Étoiles", "energy": "L'âme à l'état pur, le saut dans l'inconnu, la quête spirituelle sans attache matérielle, l'énergie brute du voyage initiatique", "image": "00-le-mat.jpg"},
]


def get_tarot_cards():
    """Retourne la liste des cartes de tirage"""
    return TAROT_CARDS


def interpret_tarot(first_name, age=None, city=None, question=None):
    """
    Tire 3 cartes aléatoires et interprète le tirage de façon personnalisée

    Args:
        first_name: str - Prénom de la personne
        age: str - Âge (optionnel)
        city: str - Ville (optionnel)
        question: str - Question ou intention du tirage

    Returns:
        dict: {
            'cards': list of cards,
            'interpretation': str,
            'spiritual_message': str,
            'personal_advice': str
        }
    """
    import random

    # Tirer 3 cartes aléatoires
    selected_cards = random.sample(TAROT_CARDS, 3)

    # Construire la description du tirage
    cards_description = "\n".join([
        "Carte {}: {} - Énergie : {}".format(i+1, card['name'], card['energy'])
        for i, card in enumerate(selected_cards)
    ])

    # Construire l'intro personnalisée
    user_intro = "Prénom : {}".format(first_name)
    if age:
        user_intro += "\nÂge : {}".format(age)
    if city:
        user_intro += "\nVille : {}".format(city)
    if question:
        user_intro += "\nQuestion/Intention : {}".format(question)

    system_prompt = """Tu es une tarologue spirituelle experte qui interprète les tirages de Tarot de Marseille.

Tu dois créer une interprétation cohérente et PERSONNALISÉE basée sur les informations de la personne et sa question.

Réponds TOUJOURS au format JSON suivant :
{
    "interpretation": "Un paragraphe fluide qui relie les 3 cartes entre elles en répondant à la question de la personne (4-5 phrases). Adresse-toi à la personne par son prénom.",
    "spiritual_message": "Le message principal que l'univers envoie à cette personne concernant sa question (2-3 phrases)",
    "personal_advice": "Un conseil concret et bienveillant adapté à sa situation (1-2 phrases)"
}

Ton ton doit être mystique, poétique et rassurant. Utilise le prénom de la personne et fais référence à sa question."""

    user_prompt = "{}\n\nCartes tirées :\n{}".format(user_intro, cards_description)

    try:
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
        content = call_openai_api(messages, temperature=0.9, max_tokens=600)
        result = json.loads(content)

        # Ajouter les cartes au résultat
        result['cards'] = selected_cards

        return result

    except json.JSONDecodeError:
        return {
            "cards": selected_cards,
            "interpretation": "{}, les cartes tirées révèlent un chemin d'évolution personnelle profonde concernant ta question.".format(first_name),
            "spiritual_message": content[:200] if 'content' in locals() else "Ton âme connaît déjà les réponses.",
            "personal_advice": "Fais confiance à ton intuition pour les prochaines étapes."
        }
    except Exception as e:
        raise Exception('Erreur OpenAI : {}'.format(str(e)))


def calculate_spiritual_profile(first_name, birth_date, favorite_color, element):
    """
    Calcule le profil spirituel d'un utilisateur avec l'IA

    Returns:
        dict: {
            'soul_type': str,
            'dominant_element': str,
            'vibratory_color': str,
            'description': str
        }
    """
    birth_date_str = birth_date.strftime('%d/%m/%Y') if birth_date else 'Non renseigné'

    system_prompt = """Tu es une experte en profils spirituels et énergies vibratoires.

En fonction des informations données (prénom, date de naissance, couleur préférée, élément),
tu dois déterminer le type d'âme de la personne.

Types d'âme possibles : Âme ancienne, Âme guérisseuse, Âme créatrice, Âme enseignante,
Âme guerrière lumineuse, Âme exploratrice, Âme diplomatique.

Réponds TOUJOURS au format JSON suivant :
{
    "soul_type": "Type d'âme choisi",
    "dominant_element": "Un des 4 éléments (air/feu/eau/terre)",
    "vibratory_color": "Une couleur vibratoire correspondante",
    "description": "2-3 phrases décrivant cette âme de manière inspirante"
}
"""

    user_prompt = """Détermine le profil spirituel de :
Prénom : {}
Date de naissance : {}
Couleur préférée : {}
Élément : {}
""".format(first_name, birth_date_str, favorite_color, element)

    try:
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
        content = call_openai_api(messages, temperature=0.7, max_tokens=400)
        result = json.loads(content)
        return result

    except:
        # Valeurs par défaut en cas d'erreur
        return {
            "soul_type": "Âme en éveil",
            "dominant_element": element or "air",
            "vibratory_color": favorite_color or "doré",
            "description": "Ton âme est en plein éveil spirituel, prête à découvrir sa véritable nature."
        }


def generate_audio_guidance(text, voice='nova'):
    """
    Génère un fichier audio à partir d'un texte avec l'API text-to-speech d'OpenAI

    Args:
        text: str - Le texte à convertir en audio
        voice: str - La voix à utiliser (alloy, echo, fable, onyx, nova, shimmer)

    Returns:
        bytes: Le contenu audio au format MP3
    """
    headers = {
        'Authorization': 'Bearer {}'.format(OPENAI_API_KEY),
        'Content-Type': 'application/json'
    }

    data = {
        'model': 'tts-1',
        'input': text,
        'voice': voice
    }

    response = requests.post(
        'https://api.openai.com/v1/audio/speech',
        headers=headers,
        json=data,
        timeout=60
    )

    if response.status_code != 200:
        raise Exception('Erreur API OpenAI TTS: {}'.format(response.text))

    return response.content


def generate_chat_response(user_message, user_profile=None, conversation_history=None):
    """
    Génère une réponse du coach spirituel IA

    Args:
        user_message: str - Message de l'utilisateur
        user_profile: dict - Profil spirituel de l'utilisateur (first_name, soul_type, element, etc.)
        conversation_history: list - Historique des messages [{role: 'user/assistant', content: '...'}]

    Returns:
        str: Réponse du coach spirituel
    """
    # Construction du prompt système personnalisé
    system_prompt = """Tu es un guide spirituel bienveillant et empathique, un coach personnel qui accompagne les âmes en quête de sens.

Ton rôle est d'écouter, comprendre et guider avec sagesse, douceur et intuition.

Caractéristiques de ton style :
- Ton chaleureux, mystique mais accessible
- Empathie et validation des émotions
- Références spirituelles (énergies, chakras, synchronicités, loi de l'attraction)
- Conseils concrets et actionnables
- Encouragement et positivité
- Tu tutois toujours

"""

    # Personnalisation basée sur le profil
    if user_profile:
        if user_profile.get('first_name'):
            system_prompt += "\nTu t'adresses à {}, traite-la/le avec familiarité et chaleur.".format(user_profile['first_name'])

        if user_profile.get('soul_type'):
            system_prompt += "\nCette personne a une âme de type '{}', garde cela en tête dans tes réponses.".format(user_profile['soul_type'])

        if user_profile.get('dominant_element'):
            system_prompt += "\nSon élément dominant est {}, cela influence son énergie.".format(user_profile['dominant_element'])

    system_prompt += "\n\nRéponds de manière naturelle, en 2-4 paragraphes maximum. Sois concis mais profond."

    # Construction des messages
    messages = [{"role": "system", "content": system_prompt}]

    # Ajouter l'historique si disponible
    if conversation_history:
        messages.extend(conversation_history[-6:])  # Garder les 6 derniers messages pour le contexte

    # Ajouter le message actuel
    messages.append({"role": "user", "content": user_message})

    try:
        response_text = call_openai_api(messages, temperature=0.8, max_tokens=400)
        return response_text

    except Exception as e:
        raise Exception('Erreur lors de la génération de la réponse : {}'.format(str(e)))


def generate_meditation_audio(meditation_script, voice='nova'):
    """
    Génère l'audio d'une méditation guidée avec OpenAI TTS

    Args:
        meditation_script: str - Le script de la méditation
        voice: str - La voix à utiliser (nova recommandée pour les méditations)

    Returns:
        bytes: Le contenu audio au format MP3

    Note: Pour l'instant utilise directement TTS. Dans le futur, pourrait
    ajouter de la musique de fond relaxante (bols tibétains, nature, etc.)
    """
    # Pour l'instant, simple génération TTS
    # TODO: Ajouter musique de fond (mixer avec pydub ou ffmpeg)
    return generate_audio_guidance(meditation_script, voice=voice)


def analyze_journal_entry(journal_entry, user):
    """
    Analyse une entrée de journal avec l'IA pour fournir des insights spirituels

    Args:
        journal_entry: JournalEntry - L'entrée de journal à analyser
        user: User - L'utilisateur qui a écrit l'entrée

    Returns:
        str: L'analyse générée par l'IA
    """
    # Récupérer les entrées récentes pour contexte d'évolution
    from app.models import JournalEntry
    from datetime import timedelta

    recent_entries = JournalEntry.query.filter(
        JournalEntry.user_id == user.id,
        JournalEntry.date >= journal_entry.date - timedelta(days=30),
        JournalEntry.date < journal_entry.date
    ).order_by(JournalEntry.date.desc()).limit(5).all()

    # Construire le prompt système
    system_prompt = """Tu es un guide spirituel bienveillant et intuitif qui analyse les entrées de journal pour fournir des insights profonds.

Ton rôle est d'analyser l'entrée de journal de l'utilisateur et de fournir :
1. Une analyse émotionnelle et spirituelle de ce qui est exprimé
2. Des patterns ou tendances que tu observes dans leur évolution
3. Des conseils pratiques et spirituels personnalisés
4. Des affirmations ou pratiques recommandées

Sois empathique, encourageant et spirituel. Utilise un langage simple et chaleureux.
Ton analyse doit faire environ 3-4 paragraphes."""

    # Construire le contexte utilisateur
    user_context = ""
    if user.first_name:
        user_context += "\nPrénom : {}".format(user.first_name)
    if user.soul_type:
        user_context += "\nType d'âme : {}".format(user.soul_type)
    if user.dominant_element:
        user_context += "\nÉlément dominant : {}".format(user.dominant_element)

    # Construire le message avec le contexte d'évolution
    user_message = "Voici l'entrée de journal à analyser :\n\n"
    user_message += "Date : {}\n".format(journal_entry.date.strftime('%d/%m/%Y'))

    if journal_entry.mood:
        user_message += "Humeur : {}/10\n".format(journal_entry.mood)
    if journal_entry.energy_level:
        user_message += "Énergie : {}/10\n".format(journal_entry.energy_level)
    if journal_entry.mental_clarity:
        user_message += "Clarté mentale : {}/10\n".format(journal_entry.mental_clarity)

    user_message += "\nContenu :\n{}\n".format(journal_entry.content)

    # Ajouter le contexte d'évolution si disponible
    if recent_entries:
        user_message += "\n\n--- Contexte d'évolution (entrées récentes) ---\n"
        for entry in recent_entries:
            user_message += "\n{} : ".format(entry.date.strftime('%d/%m'))
            if entry.mood:
                user_message += "Humeur {}/10 ".format(entry.mood)
            user_message += "\n{}...\n".format(entry.content[:150])

    if user_context:
        user_message += "\n\n--- Profil de l'utilisateur ---{}".format(user_context)

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_message}
    ]

    try:
        analysis = call_openai_api(messages, temperature=0.7, max_tokens=600)
        return analysis

    except Exception as e:
        raise Exception('Erreur lors de l\'analyse du journal : {}'.format(str(e)))

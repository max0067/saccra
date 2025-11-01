"""
Service d'interprétation IA avec OpenAI (via requests pour Python 3.6)
"""
import os
import json
import requests
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()
from datetime import datetime

# Configuration OpenAI
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY', '')
MODEL = os.environ.get('OPENAI_MODEL', 'gpt-4o-mini')


def call_openai_api(messages, temperature=0.8, max_tokens=500):
    """
    Appelle l'API OpenAI directement avec requests (compatible Python 3.6)
    """
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
    return result['choices'][0]['message']['content'].strip()


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
    {"id": 1, "name": "Le Bateleur", "energy": "commencement, créativité, potentiel"},
    {"id": 2, "name": "La Papesse", "energy": "intuition, mystère, sagesse intérieure"},
    {"id": 3, "name": "L'Impératrice", "energy": "abondance, fertilité, créativité"},
    {"id": 4, "name": "L'Empereur", "energy": "autorité, structure, stabilité"},
    {"id": 5, "name": "Le Pape", "energy": "tradition, enseignement, spiritualité"},
    {"id": 6, "name": "L'Amoureux", "energy": "choix, union, amour"},
    {"id": 7, "name": "Le Chariot", "energy": "victoire, volonté, maîtrise"},
    {"id": 8, "name": "La Justice", "energy": "équilibre, vérité, karma"},
    {"id": 9, "name": "L'Hermite", "energy": "sagesse, introspection, solitude"},
    {"id": 10, "name": "La Roue de Fortune", "energy": "cycles, destinée, changement"},
    {"id": 11, "name": "La Force", "energy": "courage, patience, maîtrise intérieure"},
    {"id": 12, "name": "Le Pendu", "energy": "lâcher-prise, sacrifice, perspective"},
    {"id": 13, "name": "L'Arcane sans nom", "energy": "transformation, fin, renaissance"},
    {"id": 14, "name": "Tempérance", "energy": "équilibre, modération, guérison"},
    {"id": 15, "name": "Le Diable", "energy": "attachement, passion, matérialité"},
    {"id": 16, "name": "La Maison Dieu", "energy": "révélation, bouleversement, libération"},
    {"id": 17, "name": "L'Étoile", "energy": "espoir, inspiration, guidance"},
    {"id": 18, "name": "La Lune", "energy": "illusion, intuition, inconscient"},
    {"id": 19, "name": "Le Soleil", "energy": "joie, succès, vitalité"},
    {"id": 20, "name": "Le Jugement", "energy": "renaissance, révélation, pardon"},
    {"id": 21, "name": "Le Monde", "energy": "accomplissement, totalité, voyage"},
    {"id": 22, "name": "Le Mat", "energy": "liberté, spontanéité, nouveau départ"},
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

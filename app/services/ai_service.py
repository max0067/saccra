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


# Base de données de cartes pour le tirage intuitif
TAROT_CARDS = [
    {"id": 1, "name": "La Lumière", "energy": "clarté, révélation, éveil"},
    {"id": 2, "name": "L'Ancrage", "energy": "stabilité, enracinement, sécurité"},
    {"id": 3, "name": "La Transformation", "energy": "changement, renaissance, métamorphose"},
    {"id": 4, "name": "L'Amour", "energy": "connexion, compassion, ouverture du cœur"},
    {"id": 5, "name": "La Sagesse", "energy": "connaissance intérieure, intuition, guidance"},
    {"id": 6, "name": "La Force", "energy": "courage, volonté, persévérance"},
    {"id": 7, "name": "La Paix", "energy": "harmonie, sérénité, équilibre"},
    {"id": 8, "name": "L'Abondance", "energy": "prospérité, gratitude, générosité"},
    {"id": 9, "name": "La Protection", "energy": "sécurité spirituelle, bouclier énergétique"},
    {"id": 10, "name": "Le Renouveau", "energy": "nouveau départ, espoir, fraîcheur"},
    {"id": 11, "name": "La Créativité", "energy": "expression, inspiration, manifestation"},
    {"id": 12, "name": "La Guérison", "energy": "soin, régénération, libération"},
]


def get_tarot_cards():
    """Retourne la liste des cartes de tirage"""
    return TAROT_CARDS


def interpret_tarot(card_ids):
    """
    Interprète un tirage de 3 cartes

    Args:
        card_ids: list of int (3 IDs de cartes)

    Returns:
        dict: {
            'cards': list of cards,
            'interpretation': str,
            'spiritual_message': str,
            'personal_advice': str
        }
    """
    # Récupérer les cartes sélectionnées
    selected_cards = [card for card in TAROT_CARDS if card['id'] in card_ids]

    if len(selected_cards) != 3:
        raise ValueError("Il faut exactement 3 cartes")

    # Construire la description du tirage
    cards_description = "\n".join([
        "Carte {}: {} - Énergie : {}".format(i+1, card['name'], card['energy'])
        for i, card in enumerate(selected_cards)
    ])

    system_prompt = """Tu es une tarologue spirituelle experte qui interprète les tirages intuitifs.

Tu dois créer une interprétation cohérente et fluide du tirage de 3 cartes, en les reliant entre elles pour créer un message unifié.

Réponds TOUJOURS au format JSON suivant :
{
    "interpretation": "Un paragraphe fluide qui relie les 3 cartes entre elles (4-5 phrases)",
    "spiritual_message": "Le message principal que l'univers t'envoie (2-3 phrases)",
    "personal_advice": "Un conseil concret et bienveillant pour avancer (1-2 phrases)"
}

Ton doit être mystique, poétique et rassurant. Crée une histoire avec les 3 cartes."""

    user_prompt = "Interprète ce tirage de 3 cartes :\n\n{}".format(cards_description)

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
            "interpretation": "Les cartes tirées révèlent un chemin d'évolution personnelle profonde.",
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

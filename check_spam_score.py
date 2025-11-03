#!/usr/bin/env python3
"""
Vérificateur de spam score pour une campagne email
Analyse le contenu et donne des recommandations pour éviter les filtres anti-spam

Usage:
    python3 check_spam_score.py <campaign_id>
"""
import sys
import os
import re
import argparse

# Ajouter le répertoire parent au path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from app.models import EmailCampaign

# Mots spam courants (pondération)
SPAM_WORDS = {
    'urgent': 2,
    'gratuit': 3,
    'free': 3,
    'argent': 3,
    'money': 3,
    'casino': 5,
    'viagra': 5,
    'crypto': 2,
    'bitcoin': 2,
    'gagner': 2,
    'win': 2,
    'jackpot': 4,
    'cliquez ici': 3,
    'click here': 3,
    'act now': 3,
    'agissez maintenant': 3,
    'limité': 2,
    'limited': 2,
    '!!!': 3,
    '???': 2,
    '100%': 2,
    'congratulations': 3,
    'félicitations': 3,
    'garanti': 2,
    'guaranteed': 2,
}

def check_spam_score(html_content, subject):
    """
    Calcule un score de spam (0-100, 0 = meilleur)

    Returns:
        tuple: (score, warnings, suggestions)
    """
    score = 0
    warnings = []
    suggestions = []

    # 1. Vérifier le sujet
    subject_lower = subject.lower()

    # Sujet tout en majuscules
    if subject.isupper() and len(subject) > 3:
        score += 10
        warnings.append("❌ Sujet en MAJUSCULES")
        suggestions.append("Utilise des minuscules dans le sujet")

    # Mots spam dans le sujet
    for word, points in SPAM_WORDS.items():
        if word in subject_lower:
            score += points * 2  # Double pénalité dans le sujet
            warnings.append(f"❌ Mot spam dans sujet: '{word}'")
            suggestions.append(f"Remplace '{word}' par un terme plus neutre")

    # Exclamations excessives dans le sujet
    if subject.count('!') > 1:
        score += 5
        warnings.append(f"❌ Trop d'exclamations dans le sujet ({subject.count('!')})")
        suggestions.append("Limite à 1 exclamation maximum")

    # 2. Vérifier le contenu HTML
    content_lower = html_content.lower()

    # Mots spam dans le contenu
    spam_words_found = []
    for word, points in SPAM_WORDS.items():
        count = content_lower.count(word)
        if count > 0:
            score += points * count
            spam_words_found.append((word, count))

    if spam_words_found:
        warnings.append(f"⚠️  Mots spam trouvés: {len(spam_words_found)}")
        for word, count in spam_words_found[:5]:  # Top 5
            suggestions.append(f"Réduis l'usage de '{word}' (trouvé {count}x)")

    # Ratio texte/HTML
    text_content = re.sub('<[^<]+?>', '', html_content)  # Retirer les tags HTML
    text_length = len(text_content.strip())
    html_length = len(html_content)

    if html_length > 0:
        text_ratio = (text_length / html_length) * 100
        if text_ratio < 30:
            score += 10
            warnings.append(f"❌ Peu de texte ({text_ratio:.0f}% texte/HTML)")
            suggestions.append("Ajoute plus de texte (idéal: 60%+)")

    # Images sans texte alternatif
    img_tags = re.findall(r'<img[^>]+>', html_content, re.IGNORECASE)
    img_without_alt = [img for img in img_tags if 'alt=' not in img.lower()]

    if img_without_alt:
        score += len(img_without_alt) * 2
        warnings.append(f"⚠️  {len(img_without_alt)} images sans attribut alt")
        suggestions.append("Ajoute des attributs alt à toutes les images")

    # Liens raccourcis (bit.ly, tinyurl, etc.)
    shortened_urls = re.findall(r'(bit\.ly|tinyurl|goo\.gl|t\.co)', content_lower)
    if shortened_urls:
        score += len(shortened_urls) * 5
        warnings.append(f"❌ Liens raccourcis trouvés ({len(shortened_urls)})")
        suggestions.append("Utilise des URLs complètes au lieu de liens raccourcis")

    # Lien de désinscription manquant
    if 'unsubscribe' not in content_lower and 'désinscrire' not in content_lower and 'désinscription' not in content_lower:
        score += 15
        warnings.append("❌ Pas de lien de désinscription visible")
        suggestions.append("✅ Le footer automatique ajoute ce lien (déjà fait !)")

    # Formulaires dans l'email
    if '<form' in content_lower:
        score += 10
        warnings.append("❌ Formulaire HTML détecté")
        suggestions.append("Remplace les formulaires par des liens vers ton site")

    # JavaScript dans l'email
    if '<script' in content_lower:
        score += 20
        warnings.append("❌ JavaScript détecté (bloqué par la plupart des clients)")
        suggestions.append("Retire tout JavaScript des emails")

    # Majuscules excessives
    caps_words = re.findall(r'\b[A-Z]{4,}\b', text_content)
    if len(caps_words) > 3:
        score += 5
        warnings.append(f"⚠️  Trop de MAJUSCULES ({len(caps_words)} mots)")
        suggestions.append("Réduis l'usage des MAJUSCULES")

    # Longueur du contenu
    if text_length < 200:
        score += 5
        warnings.append("⚠️  Contenu court (< 200 caractères)")
        suggestions.append("Ajoute plus de contenu (idéal: 500+ caractères)")

    return min(score, 100), warnings, suggestions

def analyze_campaign(campaign_id):
    """Analyse une campagne et affiche le rapport"""
    app = create_app()

    with app.app_context():
        campaign = EmailCampaign.query.get(campaign_id)
        if not campaign:
            print(f"❌ Campagne ID {campaign_id} introuvable")
            return

        print("=" * 70)
        print("VÉRIFICATEUR DE SPAM SCORE - SACRA")
        print("=" * 70)
        print(f"\n📧 Campagne: {campaign.name}")
        print(f"   Sujet: {campaign.subject}")
        print(f"   Type: {campaign.campaign_type}")

        # Analyser
        score, warnings, suggestions = check_spam_score(
            campaign.html_content,
            campaign.subject
        )

        # Afficher le score
        print(f"\n📊 SPAM SCORE: {score}/100")

        if score <= 20:
            print("   ✅ EXCELLENT - Faible risque de spam")
            emoji = "✅"
            color = "vert"
        elif score <= 40:
            print("   ⚠️  BON - Risque modéré, quelques améliorations possibles")
            emoji = "⚠️"
            color = "orange"
        elif score <= 60:
            print("   ⚠️  MOYEN - Risque élevé, améliorations recommandées")
            emoji = "⚠️"
            color = "orange"
        else:
            print("   ❌ MAUVAIS - Très haut risque de finir en spam")
            emoji = "❌"
            color = "rouge"

        # Afficher les warnings
        if warnings:
            print(f"\n⚠️  PROBLÈMES DÉTECTÉS ({len(warnings)}):")
            for i, warning in enumerate(warnings, 1):
                print(f"   {i}. {warning}")

        # Afficher les suggestions
        if suggestions:
            print(f"\n💡 SUGGESTIONS D'AMÉLIORATION ({len(suggestions)}):")
            for i, suggestion in enumerate(suggestions, 1):
                print(f"   {i}. {suggestion}")

        # Recommandations générales
        print(f"\n📚 RECOMMANDATIONS GÉNÉRALES:")
        print(f"   1. ✅ Footer avec désinscription (déjà ajouté automatiquement)")
        print(f"   2. Utilise le warm-up progressif (warmup_campaign.py)")
        print(f"   3. Nettoie ta liste (retire les bounces)")
        print(f"   4. Personnalise avec {{{{first_name}}}}")
        print(f"   5. Configure SPF/DKIM/DMARC dans ton DNS")

        print(f"\n💾 PROCHAINES ÉTAPES:")
        if score > 40:
            print(f"   1. Corrige les problèmes listés ci-dessus")
            print(f"   2. Relance ce script pour vérifier")
            print(f"   3. Envoie un test à toi-même")
        else:
            print(f"   1. Envoie un test avec le bouton '📧 Email de Test'")
            print(f"   2. Lance le warm-up: python3 warmup_campaign.py {campaign_id}")
            print(f"   3. Vérifie que l'email n'est pas dans les spams")

        print("\n" + "=" * 70)

def main():
    parser = argparse.ArgumentParser(
        description='Vérificateur de spam score',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )

    parser.add_argument('campaign_id', type=int, help='ID de la campagne')

    args = parser.parse_args()

    analyze_campaign(args.campaign_id)

if __name__ == '__main__':
    main()

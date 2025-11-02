#!/usr/bin/env python3
"""
Test SMTP o2switch - À exécuter sur le serveur de production
Usage: python3 test_smtp_o2switch.py
"""
import os
import sys
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

# Vérifier qu'on est bien configuré pour o2switch
smtp_server = os.environ.get('MAIL_SERVER', '')
smtp_port = int(os.environ.get('MAIL_PORT', '0'))
smtp_user = os.environ.get('MAIL_USERNAME', '')
smtp_password = os.environ.get('MAIL_PASSWORD', '')
sender_email = os.environ.get('MAIL_DEFAULT_SENDER', '')

print("=" * 70)
print("TEST SMTP O2SWITCH - SACRA EMAIL MARKETING")
print("=" * 70)

print("\n📧 Configuration actuelle:")
print(f"   Serveur : {smtp_server}")
print(f"   Port    : {smtp_port}")
print(f"   User    : {smtp_user}")
print(f"   Sender  : {sender_email}")
print(f"   Password: {'*' * 10} {'✅ Configuré' if smtp_password else '❌ MANQUANT'}")

# Vérifications
errors = []

if smtp_server != 'mail.saccra.fr':
    errors.append(f"❌ MAIL_SERVER devrait être 'mail.saccra.fr' (actuellement: {smtp_server})")

if smtp_port != 465:
    errors.append(f"❌ MAIL_PORT devrait être 465 (actuellement: {smtp_port})")

if smtp_user != 'contact@saccra.fr':
    errors.append(f"❌ MAIL_USERNAME devrait être 'contact@saccra.fr' (actuellement: {smtp_user})")

if not smtp_password or len(smtp_password) < 8:
    errors.append("❌ MAIL_PASSWORD manquant ou trop court")

if sender_email != 'contact@saccra.fr':
    errors.append(f"⚠️ MAIL_DEFAULT_SENDER recommandé: 'contact@saccra.fr' (actuellement: {sender_email})")

if errors:
    print("\n⚠️  PROBLÈMES DE CONFIGURATION DÉTECTÉS:")
    for error in errors:
        print(f"   {error}")
    print("\n💡 Voir le guide: MISE_A_JOUR_SMTP.md")
    print("\n❌ Test d'envoi annulé (configuration incorrecte)")
    sys.exit(1)

print("\n✅ Configuration correcte pour o2switch!")

# Demander confirmation avant d'envoyer
print("\n" + "=" * 70)
print("PRÊT POUR LE TEST D'ENVOI")
print("=" * 70)

destination = input(f"\n📬 Email de destination (Enter pour {smtp_user}): ").strip()
if not destination:
    destination = smtp_user

print(f"\n🚀 Envoi d'un email de test à: {destination}")
print("   Cela va utiliser le serveur SMTP o2switch...")

# Importer après les vérifications
try:
    from app.services.email_service import _send_email
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart
    import datetime
except ImportError as e:
    print(f"\n❌ Erreur d'import: {e}")
    print("   Assure-toi d'être dans le bon répertoire")
    sys.exit(1)

try:
    # Créer le message
    message = MIMEMultipart('alternative')
    message['Subject'] = '🧪 Test SMTP o2switch - SACRA'
    message['From'] = sender_email
    message['To'] = destination

    # Contenu HTML
    html_content = f"""
    <html>
    <head>
        <meta charset="UTF-8">
    </head>
    <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px;">
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; text-align: center; border-radius: 10px;">
            <h1>✅ Test SMTP Réussi!</h1>
        </div>

        <div style="background: #f9f9f9; padding: 30px; margin-top: 20px; border-radius: 10px;">
            <p>Félicitations ! 🎉</p>

            <p>Ton serveur SMTP <strong>o2switch</strong> fonctionne parfaitement!</p>

            <h3 style="color: #667eea;">📊 Informations de test:</h3>
            <table style="width: 100%; border-collapse: collapse;">
                <tr style="border-bottom: 1px solid #ddd;">
                    <td style="padding: 10px; font-weight: bold;">Serveur:</td>
                    <td style="padding: 10px;">{smtp_server}</td>
                </tr>
                <tr style="border-bottom: 1px solid #ddd;">
                    <td style="padding: 10px; font-weight: bold;">Port:</td>
                    <td style="padding: 10px;">{smtp_port} (SSL)</td>
                </tr>
                <tr style="border-bottom: 1px solid #ddd;">
                    <td style="padding: 10px; font-weight: bold;">Expéditeur:</td>
                    <td style="padding: 10px;">{sender_email}</td>
                </tr>
                <tr>
                    <td style="padding: 10px; font-weight: bold;">Date:</td>
                    <td style="padding: 10px;">{datetime.datetime.now().strftime('%d/%m/%Y à %H:%M:%S')}</td>
                </tr>
            </table>

            <div style="margin-top: 30px; padding: 20px; background: #e7f5ff; border-left: 4px solid #667eea; border-radius: 5px;">
                <h4 style="margin-top: 0; color: #667eea;">🚀 Prochaines étapes:</h4>
                <ol style="margin-bottom: 0;">
                    <li>✅ Configuration SMTP validée</li>
                    <li>📥 Import de tes 55 000 contacts (déjà fait!)</li>
                    <li>✉️ Création de ta première vraie campagne</li>
                    <li>📤 Envoi automatique par batch (script à créer)</li>
                </ol>
            </div>

            <p style="margin-top: 30px; color: #666; font-size: 12px;">
                <strong>Note:</strong> Si tu reçois cet email, ton système d'email marketing est 100% opérationnel!
                Tu es prêt à envoyer des campagnes à tes contacts.
            </p>
        </div>

        <div style="text-align: center; margin-top: 30px; color: #999; font-size: 12px;">
            <p>SACRA - Email Marketing System</p>
            <p>Serveur: {smtp_server}:{smtp_port}</p>
        </div>
    </body>
    </html>
    """

    # Contenu texte
    text_content = f"""
    Test SMTP o2switch - SACRA

    Félicitations ! Ton serveur SMTP o2switch fonctionne parfaitement!

    Informations de test:
    - Serveur: {smtp_server}
    - Port: {smtp_port} (SSL)
    - Expéditeur: {sender_email}
    - Date: {datetime.datetime.now().strftime('%d/%m/%Y à %H:%M:%S')}

    Prochaines étapes:
    1. Configuration SMTP validée ✅
    2. Import de tes 55 000 contacts (déjà fait!) ✅
    3. Création de ta première vraie campagne
    4. Envoi automatique par batch (script à créer)

    Si tu reçois cet email, ton système est 100% opérationnel!

    SACRA - Email Marketing System
    """

    # Attacher les contenus
    part1 = MIMEText(text_content, 'plain', 'utf-8')
    part2 = MIMEText(html_content, 'html', 'utf-8')
    message.attach(part1)
    message.attach(part2)

    # Envoyer
    print("\n📤 Connexion au serveur SMTP...")
    _send_email(message, smtp_server, smtp_port, smtp_user, smtp_password)

    print("\n" + "=" * 70)
    print("✅ EMAIL ENVOYÉ AVEC SUCCÈS!")
    print("=" * 70)
    print(f"\n📬 Vérifie ta boîte email: {destination}")
    print("\n💡 Si tu as reçu l'email:")
    print("   ✅ Configuration SMTP o2switch validée")
    print("   ✅ Système d'email marketing opérationnel")
    print("   ✅ Prêt à envoyer des campagnes aux 55K contacts")
    print("\n📝 Prochaine étape:")
    print("   - Crée une vraie campagne via https://saccra.fr/admin/emails")
    print("   - Ou demande-moi de créer le script d'envoi automatique par batch")
    print("\n" + "=" * 70)

except Exception as e:
    print("\n" + "=" * 70)
    print("❌ ERREUR LORS DE L'ENVOI")
    print("=" * 70)
    print(f"\nErreur: {str(e)}")
    print("\n🔍 Vérifications à faire:")
    print("   1. Le mot de passe est-il correct dans .env?")
    print("   2. Le compte email existe-t-il dans cPanel o2switch?")
    print("   3. Le serveur mail.saccra.fr est-il accessible?")
    print("   4. Le port 465 est-il ouvert?")
    print("\n💡 Pour tester la connexion:")
    print(f"   telnet {smtp_server} {smtp_port}")
    print("\n📖 Voir le guide: MISE_A_JOUR_SMTP.md")
    sys.exit(1)

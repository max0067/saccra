"""
Script de test SMTP pour diagnostiquer les problèmes d'envoi d'emails
"""
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv

load_dotenv()

def test_smtp_connection():
    """Test la connexion SMTP et l'envoi d'un email simple"""

    # Configuration depuis .env
    smtp_server = os.environ.get('MAIL_SERVER', 'localhost')
    smtp_port = int(os.environ.get('MAIL_PORT', '25'))
    smtp_user = os.environ.get('MAIL_USERNAME', '')
    smtp_password = os.environ.get('MAIL_PASSWORD', '')
    sender_email = os.environ.get('MAIL_DEFAULT_SENDER', 'noreply@saccra.fr')

    print("=" * 60)
    print("TEST CONFIGURATION SMTP")
    print("=" * 60)
    print(f"Serveur SMTP: {smtp_server}")
    print(f"Port SMTP: {smtp_port}")
    print(f"Utilisateur: {smtp_user if smtp_user else '(aucun)'}")
    print(f"Mot de passe: {'***' if smtp_password else '(aucun)'}")
    print(f"Email expéditeur: {sender_email}")
    print("=" * 60)

    # Email de test
    test_email = "maxenko06@gmail.com"

    try:
        # Créer le message
        message = MIMEMultipart('alternative')
        message['Subject'] = 'TEST SMTP - SACRA'
        message['From'] = sender_email
        message['To'] = test_email

        html_content = """
        <html>
        <body>
            <h2>🔧 Test SMTP - SACRA</h2>
            <p>Si tu reçois cet email, la configuration SMTP fonctionne correctement !</p>
            <p><strong>Configuration utilisée:</strong></p>
            <ul>
                <li>Serveur: {server}</li>
                <li>Port: {port}</li>
            </ul>
            <p>Email envoyé depuis le script test_smtp.py</p>
        </body>
        </html>
        """.format(server=smtp_server, port=smtp_port)

        part = MIMEText(html_content, 'html', 'utf-8')
        message.attach(part)

        print("\n📧 Tentative d'envoi d'un email test à:", test_email)
        print("Connexion au serveur SMTP...")

        # Cas spécial: localhost:25 (relay SMTP local o2switch)
        if smtp_server in ['localhost', '127.0.0.1'] and smtp_port == 25:
            print("Mode: Relay local (localhost:25) - pas d'authentification")
            with smtplib.SMTP(smtp_server, smtp_port, timeout=10) as server:
                server.set_debuglevel(1)  # Mode debug pour voir ce qui se passe
                print("Envoi du message...")
                server.send_message(message)
                print("\n✅ Email envoyé avec succès!")

        # Port 465 = SSL direct
        elif smtp_port == 465:
            print("Mode: SMTP_SSL (port 465)")
            with smtplib.SMTP_SSL(smtp_server, smtp_port, timeout=10) as server:
                server.set_debuglevel(1)
                if smtp_user and smtp_password:
                    print("Authentification...")
                    server.login(smtp_user, smtp_password)
                print("Envoi du message...")
                server.send_message(message)
                print("\n✅ Email envoyé avec succès!")

        # Port 587 ou autre = TLS avec STARTTLS
        else:
            print(f"Mode: SMTP avec STARTTLS (port {smtp_port})")
            with smtplib.SMTP(smtp_server, smtp_port, timeout=10) as server:
                server.set_debuglevel(1)
                print("Activation STARTTLS...")
                server.starttls()
                if smtp_user and smtp_password:
                    print("Authentification...")
                    server.login(smtp_user, smtp_password)
                print("Envoi du message...")
                server.send_message(message)
                print("\n✅ Email envoyé avec succès!")

        print("\n" + "=" * 60)
        print("✅ TEST RÉUSSI")
        print("=" * 60)
        print(f"Vérifie ta boîte mail: {test_email}")
        print("(Regarde aussi dans les spams)")

        return True

    except smtplib.SMTPAuthenticationError as e:
        print(f"\n❌ ERREUR D'AUTHENTIFICATION: {e}")
        print("Les identifiants SMTP sont incorrects ou manquants")
        return False

    except smtplib.SMTPConnectError as e:
        print(f"\n❌ ERREUR DE CONNEXION: {e}")
        print("Impossible de se connecter au serveur SMTP")
        return False

    except smtplib.SMTPException as e:
        print(f"\n❌ ERREUR SMTP: {e}")
        return False

    except Exception as e:
        print(f"\n❌ ERREUR GÉNÉRALE: {type(e).__name__}")
        print(f"Détails: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    test_smtp_connection()

"""
Service d'envoi d'emails pour SACRA
Compatible Python 3.6
"""
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv

load_dotenv()

def send_welcome_email(user_email, user_name):
    """
    Envoie un email de bienvenue au nouvel utilisateur

    Args:
        user_email: str - Email de l'utilisateur
        user_name: str - Prénom de l'utilisateur

    Returns:
        bool: True si envoyé, False sinon
    """
    # Configuration SMTP depuis les variables d'environnement
    smtp_server = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
    smtp_port = int(os.environ.get('MAIL_PORT', '587'))
    smtp_user = os.environ.get('MAIL_USERNAME', '')
    smtp_password = os.environ.get('MAIL_PASSWORD', '')
    sender_email = os.environ.get('MAIL_DEFAULT_SENDER', 'noreply@saccra.fr')

    # Si pas de configuration SMTP, ne pas envoyer (mode silencieux)
    if not smtp_user or not smtp_password:
        print('SMTP non configuré - Email de bienvenue non envoyé')
        return False

    try:
        # Créer le message
        message = MIMEMultipart('alternative')
        message['Subject'] = 'Bienvenue dans SACRA'
        message['From'] = sender_email
        message['To'] = user_email

        # Contenu HTML de l'email
        html_content = """
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }}
                .content {{ background: #f9f9f9; padding: 30px; border-radius: 0 0 10px 10px; }}
                .button {{ display: inline-block; padding: 12px 30px; background: #667eea; color: white; text-decoration: none; border-radius: 5px; margin-top: 20px; }}
                .footer {{ text-align: center; margin-top: 30px; color: #999; font-size: 12px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🌙 Bienvenue dans SACRA</h1>
                </div>
                <div class="content">
                    <p>Bonjour {name},</p>

                    <p>Ton compte a été créé avec succès ! Nous sommes ravis de t'accueillir dans la communauté SACRA.</p>

                    <p><strong>Qu'est-ce que SACRA ?</strong></p>
                    <p>SACRA est ton guide spirituel personnel propulsé par l'IA. Explore tes rêves, décode les signes de l'univers, et reçois des interprétations profondes à travers le tarot.</p>

                    <p><strong>Tes premières étapes :</strong></p>
                    <ul>
                        <li>🔮 Complète ton profil spirituel</li>
                        <li>🌙 Interprète tes rêves</li>
                        <li>🃏 Tire tes premières cartes de tarot</li>
                        <li>✨ Décode les signes et synchronicités</li>
                    </ul>

                    <p style="text-align: center;">
                        <a href="https://saccra.fr" class="button">Commencer mon voyage spirituel</a>
                    </p>

                    <p style="margin-top: 30px; color: #666;">En tant que membre gratuit, tu as accès à <strong>3 interprétations par mois</strong>. Passe en Premium pour des interprétations illimitées !</p>
                </div>
                <div class="footer">
                    <p>SACRA - Ton guide spirituel personnel</p>
                    <p>Cet email a été envoyé à {email}</p>
                </div>
            </div>
        </body>
        </html>
        """.format(name=user_name or 'ami spirituel', email=user_email)

        # Contenu texte alternatif
        text_content = """
        Bienvenue dans SACRA !

        Bonjour {name},

        Ton compte a été créé avec succès ! Nous sommes ravis de t'accueillir dans la communauté SACRA.

        SACRA est ton guide spirituel personnel propulsé par l'IA. Explore tes rêves, décode les signes de l'univers, et reçois des interprétations profondes à travers le tarot.

        Tes premières étapes :
        - Complète ton profil spirituel
        - Interprète tes rêves
        - Tire tes premières cartes de tarot
        - Décode les signes et synchronicités

        Commence ton voyage : https://saccra.fr

        En tant que membre gratuit, tu as accès à 3 interprétations par mois. Passe en Premium pour des interprétations illimitées !

        SACRA - Ton guide spirituel personnel
        """.format(name=user_name or 'ami spirituel', email=user_email)

        # Attacher les deux versions
        part1 = MIMEText(text_content, 'plain', 'utf-8')
        part2 = MIMEText(html_content, 'html', 'utf-8')
        message.attach(part1)
        message.attach(part2)

        # Envoyer l'email
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_user, smtp_password)
            server.send_message(message)

        print('Email de bienvenue envoyé à {}'.format(user_email))
        return True

    except Exception as e:
        print('Erreur lors de l\'envoi de l\'email : {}'.format(str(e)))
        return False


def send_password_reset_email(user_email, reset_url):
    """
    Envoie un email de réinitialisation de mot de passe

    Args:
        user_email: str - Email de l'utilisateur
        reset_url: str - URL de réinitialisation avec le token

    Returns:
        bool: True si envoyé, False sinon
    """
    # Configuration SMTP depuis les variables d'environnement
    smtp_server = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
    smtp_port = int(os.environ.get('MAIL_PORT', '587'))
    smtp_user = os.environ.get('MAIL_USERNAME', '')
    smtp_password = os.environ.get('MAIL_PASSWORD', '')
    sender_email = os.environ.get('MAIL_DEFAULT_SENDER', 'noreply@saccra.fr')

    # Si pas de configuration SMTP, ne pas envoyer (mode silencieux)
    if not smtp_user or not smtp_password:
        print('SMTP non configuré - Email de réinitialisation non envoyé')
        return False

    try:
        # Créer le message
        message = MIMEMultipart('alternative')
        message['Subject'] = 'Réinitialisation de ton mot de passe SACRA'
        message['From'] = sender_email
        message['To'] = user_email

        # Contenu HTML de l'email
        html_content = """
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }}
                .content {{ background: #f9f9f9; padding: 30px; border-radius: 0 0 10px 10px; }}
                .button {{ display: inline-block; padding: 12px 30px; background: #667eea; color: white; text-decoration: none; border-radius: 5px; margin-top: 20px; }}
                .footer {{ text-align: center; margin-top: 30px; color: #999; font-size: 12px; }}
                .warning {{ background: #fff3cd; border: 1px solid #ffc107; padding: 15px; border-radius: 5px; margin-top: 20px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🔑 Réinitialisation de mot de passe</h1>
                </div>
                <div class="content">
                    <p>Bonjour,</p>

                    <p>Tu as demandé à réinitialiser ton mot de passe SACRA.</p>

                    <p><strong>Clique sur le bouton ci-dessous pour créer un nouveau mot de passe :</strong></p>

                    <p style="text-align: center;">
                        <a href="{reset_url}" class="button">Réinitialiser mon mot de passe</a>
                    </p>

                    <div class="warning">
                        <p style="margin: 0;"><strong>⚠️ Important :</strong></p>
                        <ul style="margin: 10px 0 0 0; padding-left: 20px;">
                            <li>Ce lien est valide pendant <strong>30 minutes</strong></li>
                            <li>Si tu n'as pas demandé cette réinitialisation, ignore cet email</li>
                            <li>Ne partage jamais ce lien avec personne</li>
                        </ul>
                    </div>

                    <p style="margin-top: 30px; color: #666; font-size: 12px;">Si le bouton ne fonctionne pas, copie-colle ce lien dans ton navigateur :<br>
                    <a href="{reset_url}" style="color: #667eea; word-break: break-all;">{reset_url}</a></p>
                </div>
                <div class="footer">
                    <p>SACRA - Ton guide spirituel personnel</p>
                    <p>Cet email a été envoyé à {email}</p>
                </div>
            </div>
        </body>
        </html>
        """.format(reset_url=reset_url, email=user_email)

        # Contenu texte alternatif
        text_content = """
        Réinitialisation de mot de passe - SACRA

        Bonjour,

        Tu as demandé à réinitialiser ton mot de passe SACRA.

        Clique sur ce lien pour créer un nouveau mot de passe :
        {reset_url}

        ⚠️ Important :
        - Ce lien est valide pendant 30 minutes
        - Si tu n'as pas demandé cette réinitialisation, ignore cet email
        - Ne partage jamais ce lien avec personne

        SACRA - Ton guide spirituel personnel
        """.format(reset_url=reset_url, email=user_email)

        # Attacher les deux versions
        part1 = MIMEText(text_content, 'plain', 'utf-8')
        part2 = MIMEText(html_content, 'html', 'utf-8')
        message.attach(part1)
        message.attach(part2)

        # Envoyer l'email
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_user, smtp_password)
            server.send_message(message)

        print('Email de réinitialisation envoyé à {}'.format(user_email))
        return True

    except Exception as e:
        print('Erreur lors de l\'envoi de l\'email de réinitialisation : {}'.format(str(e)))
        return False

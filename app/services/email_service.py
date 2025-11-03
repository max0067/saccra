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

def _send_email(message, smtp_server, smtp_port, smtp_user, smtp_password):
    """
    Fonction helper pour envoyer un email avec le bon mode (SSL ou TLS)

    Args:
        message: MIMEMultipart - Le message à envoyer
        smtp_server: str - Serveur SMTP
        smtp_port: int - Port SMTP
        smtp_user: str - Utilisateur SMTP
        smtp_password: str - Mot de passe SMTP
    """
    # Cas spécial: localhost:25 (relay SMTP local o2switch) - pas d'authentification
    if smtp_server in ['localhost', '127.0.0.1'] and smtp_port == 25:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            # Pas de starttls() ni de login() pour localhost
            server.send_message(message)
    # Port 465 = SSL direct
    elif smtp_port == 465:
        with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
            if smtp_user and smtp_password:
                server.login(smtp_user, smtp_password)
            server.send_message(message)
    # Port 587 ou autre = TLS avec STARTTLS
    else:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            if smtp_user and smtp_password:
                server.login(smtp_user, smtp_password)
            server.send_message(message)

def generate_email_footer(email_address):
    """
    Génère un footer HTML pour les emails marketing avec lien de désinscription
    Conforme RGPD

    Args:
        email_address: str - Email du destinataire

    Returns:
        str: HTML du footer
    """
    import hashlib

    # Générer un hash de l'email pour le lien de désinscription
    email_hash = hashlib.sha256(email_address.encode()).hexdigest()[:16]
    unsubscribe_url = f"https://saccra.fr/admin/emails/unsubscribe/{email_hash}"

    footer_html = f"""
    <div style="margin-top: 40px; padding-top: 20px; border-top: 2px solid #e5e7eb; font-size: 12px; color: #6b7280;">
        <table width="100%" cellpadding="0" cellspacing="0" style="font-family: Arial, sans-serif;">
            <tr>
                <td style="padding: 10px 0;">
                    <p style="margin: 0 0 10px 0;"><strong style="color: #7c3aed;">SACRA - Guidance Spirituelle</strong></p>
                    <p style="margin: 0 0 5px 0;">📍 Adresse: France</p>
                    <p style="margin: 0 0 15px 0;">📧 Contact: <a href="mailto:contact@saccra.fr" style="color: #7c3aed;">contact@saccra.fr</a></p>
                </td>
            </tr>
            <tr>
                <td style="padding: 10px 0;">
                    <p style="margin: 0 0 10px 0; color: #9ca3af;">
                        Tu reçois cet email car tu es inscrit à notre liste de diffusion.
                    </p>
                    <p style="margin: 0;">
                        <a href="{unsubscribe_url}" style="color: #7c3aed; text-decoration: underline;">
                            Se désinscrire de cette liste
                        </a>
                    </p>
                </td>
            </tr>
            <tr>
                <td style="padding: 15px 0 0 0; text-align: center;">
                    <p style="margin: 0; color: #9ca3af;">
                        © {import_datetime_year()} SACRA - Tous droits réservés
                    </p>
                </td>
            </tr>
        </table>
    </div>
    """

    return footer_html.replace('{import_datetime_year()}', str(__import__('datetime').datetime.now().year))

def add_footer_to_html(html_content, email_address):
    """
    Ajoute automatiquement le footer à un contenu HTML

    Args:
        html_content: str - Contenu HTML de l'email
        email_address: str - Email du destinataire

    Returns:
        str: HTML avec footer ajouté
    """
    footer = generate_email_footer(email_address)

    # Insérer le footer avant </body> si existe, sinon à la fin
    if '</body>' in html_content:
        html_content = html_content.replace('</body>', footer + '</body>')
    else:
        html_content += footer

    return html_content

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
        _send_email(message, smtp_server, smtp_port, smtp_user, smtp_password)

        print('Email de bienvenue envoyé à {}'.format(user_email))
        return True

    except Exception as e:
        print('Erreur lors de l\'envoi de l\'email : {}'.format(str(e)))
        return False


def send_admin_new_user_notification(user_email, user_name):
    """
    Envoie une notification à l'admin quand un nouveau compte est créé

    Args:
        user_email: str - Email du nouvel utilisateur
        user_name: str - Prénom du nouvel utilisateur

    Returns:
        bool: True si envoyé, False sinon
    """
    # Configuration SMTP depuis les variables d'environnement
    smtp_server = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
    smtp_port = int(os.environ.get('MAIL_PORT', '587'))
    smtp_user = os.environ.get('MAIL_USERNAME', '')
    smtp_password = os.environ.get('MAIL_PASSWORD', '')
    sender_email = os.environ.get('MAIL_DEFAULT_SENDER', 'noreply@saccra.fr')
    admin_email = os.environ.get('ADMIN_EMAIL', '')

    # Si pas de configuration SMTP ou pas d'email admin, ne pas envoyer
    if not smtp_user or not smtp_password or not admin_email:
        print('SMTP ou ADMIN_EMAIL non configuré - Notification admin non envoyée')
        return False

    try:
        # Créer le message
        message = MIMEMultipart('alternative')
        message['Subject'] = '🎉 Nouveau compte créé sur SACRA'
        message['From'] = sender_email
        message['To'] = admin_email

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
                .info-box {{ background: white; border-left: 4px solid #667eea; padding: 15px; margin: 20px 0; }}
                .footer {{ text-align: center; margin-top: 30px; color: #999; font-size: 12px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🎉 Nouveau compte créé !</h1>
                </div>
                <div class="content">
                    <p>Bonjour,</p>

                    <p>Un nouveau compte vient d'être créé sur <strong>SACRA</strong>.</p>

                    <div class="info-box">
                        <p style="margin: 5px 0;"><strong>👤 Prénom :</strong> {name}</p>
                        <p style="margin: 5px 0;"><strong>📧 Email :</strong> {email}</p>
                        <p style="margin: 5px 0;"><strong>📅 Date :</strong> {date}</p>
                    </div>

                    <p>L'utilisateur a reçu son email de bienvenue et peut maintenant accéder à toutes les fonctionnalités de SACRA.</p>

                    <p style="text-align: center; margin-top: 30px;">
                        <a href="https://saccra.fr/admin/users" style="display: inline-block; padding: 12px 30px; background: #667eea; color: white; text-decoration: none; border-radius: 5px;">Voir tous les utilisateurs</a>
                    </p>
                </div>
                <div class="footer">
                    <p>SACRA - Notification automatique</p>
                </div>
            </div>
        </body>
        </html>
        """.format(
            name=user_name or 'Non renseigné',
            email=user_email,
            date=__import__('datetime').datetime.now().strftime('%d/%m/%Y à %H:%M')
        )

        # Contenu texte alternatif
        text_content = """
        Nouveau compte créé sur SACRA !

        Un nouveau compte vient d'être créé.

        Informations :
        - Prénom : {name}
        - Email : {email}
        - Date : {date}

        L'utilisateur a reçu son email de bienvenue et peut maintenant accéder à toutes les fonctionnalités.

        SACRA - Notification automatique
        """.format(
            name=user_name or 'Non renseigné',
            email=user_email,
            date=__import__('datetime').datetime.now().strftime('%d/%m/%Y à %H:%M')
        )

        # Attacher les deux versions
        part1 = MIMEText(text_content, 'plain', 'utf-8')
        part2 = MIMEText(html_content, 'html', 'utf-8')
        message.attach(part1)
        message.attach(part2)

        # Envoyer l'email
        _send_email(message, smtp_server, smtp_port, smtp_user, smtp_password)

        print('Notification admin envoyée pour le nouveau compte : {}'.format(user_email))
        return True

    except Exception as e:
        print('Erreur lors de l\'envoi de la notification admin : {}'.format(str(e)))
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
        _send_email(message, smtp_server, smtp_port, smtp_user, smtp_password)

        print('Email de réinitialisation envoyé à {}'.format(user_email))
        return True

    except Exception as e:
        print('Erreur lors de l\'envoi de l\'email de réinitialisation : {}'.format(str(e)))
        return False

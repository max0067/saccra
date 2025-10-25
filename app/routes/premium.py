"""
Routes Premium : abonnements Stripe et codes promo
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from app.models import db, PromoCode
from datetime import datetime, timedelta
import stripe
import os

bp = Blueprint('premium', __name__)

# Configurer Stripe
stripe.api_key = os.environ.get('STRIPE_SECRET_KEY', '')

@bp.route('/subscribe')
@login_required
def subscribe():
    """Page d'abonnement Premium"""
    return render_template('premium/subscribe.html')

@bp.route('/create-checkout-session', methods=['POST'])
@login_required
def create_checkout_session():
    """Créer une session Stripe Checkout"""
    data = request.get_json()
    plan = data.get('plan', 'monthly')  # monthly ou yearly

    # Récupérer le bon price_id
    if plan == 'yearly':
        price_id = os.environ.get('STRIPE_YEARLY_PRICE_ID', '')
    else:
        price_id = os.environ.get('STRIPE_MONTHLY_PRICE_ID', '')

    if not price_id:
        return jsonify({'error': 'Configuration Stripe incomplète'}), 500

    try:
        # Créer la session Checkout
        checkout_session = stripe.checkout.Session.create(
            customer_email=current_user.email,
            payment_method_types=['card'],
            line_items=[{
                'price': price_id,
                'quantity': 1,
            }],
            mode='subscription',
            success_url=url_for('premium.success', _external=True) + '?session_id={CHECKOUT_SESSION_ID}',
            cancel_url=url_for('premium.subscribe', _external=True),
            metadata={
                'user_id': current_user.id
            }
        )

        return jsonify({'sessionId': checkout_session.id})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/success')
@login_required
def success():
    """Page de confirmation après paiement"""
    session_id = request.args.get('session_id')

    if session_id:
        try:
            # Récupérer la session Stripe
            session = stripe.checkout.Session.retrieve(session_id)

            # Activer le premium
            current_user.is_premium = True
            current_user.premium_until = datetime.utcnow() + timedelta(days=365)  # 1 an par défaut
            current_user.stripe_customer_id = session.customer
            current_user.stripe_subscription_id = session.subscription

            db.session.commit()

            flash('Bienvenue dans SACRA Premium ✨ Ton âme te remercie 🌙', 'success')

        except Exception as e:
            flash(f'Erreur lors de l\'activation : {str(e)}', 'error')

    return redirect(url_for('main.dashboard'))

@bp.route('/cancel-subscription', methods=['POST'])
@login_required
def cancel_subscription():
    """Annuler l'abonnement"""
    if not current_user.is_premium or not current_user.stripe_subscription_id:
        return jsonify({'error': 'Aucun abonnement actif'}), 400

    try:
        # Annuler dans Stripe
        stripe.Subscription.delete(current_user.stripe_subscription_id)

        # Mettre à jour la BDD
        current_user.is_premium = False
        current_user.stripe_subscription_id = None
        db.session.commit()

        return jsonify({'success': True, 'message': 'Abonnement annulé'})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@bp.route('/webhook', methods=['POST'])
def webhook():
    """Webhook Stripe pour les événements de paiement"""
    payload = request.data
    sig_header = request.headers.get('Stripe-Signature')
    webhook_secret = os.environ.get('STRIPE_WEBHOOK_SECRET', '')

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, webhook_secret
        )
    except ValueError:
        return 'Invalid payload', 400
    except stripe.error.SignatureVerificationError:
        return 'Invalid signature', 400

    # Gérer les événements
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        # L'activation est déjà gérée dans success()

    elif event['type'] == 'invoice.payment_succeeded':
        # Renouvellement réussi
        invoice = event['data']['object']
        # Prolonger le premium

    elif event['type'] == 'customer.subscription.deleted':
        # Abonnement annulé
        subscription = event['data']['object']
        # Désactiver le premium

    return jsonify({'status': 'success'})


@bp.route('/apply-promo-code', methods=['POST'])
@login_required
def apply_promo_code():
    """Appliquer un code promo"""
    data = request.get_json()
    code_str = data.get('code', '').strip().upper()

    if not code_str:
        return jsonify({'success': False, 'error': 'Code promo vide'}), 400

    # Trouver le code
    promo = PromoCode.query.filter_by(code=code_str).first()

    if not promo:
        return jsonify({'success': False, 'error': 'Code promo invalide'}), 404

    if not promo.is_valid():
        return jsonify({'success': False, 'error': 'Ce code a expiré ou n\'est plus valide'}), 400

    # Appliquer le code
    success = promo.use_code(current_user)

    if success:
        message = ''
        if promo.reward_type == 'credits':
            message = '{} crédits ajoutés à ton compte ! 🎁'.format(promo.reward_value)
        elif promo.reward_type == 'premium_days':
            message = '{} jours de Premium offerts ! ✨'.format(promo.reward_value)

        return jsonify({
            'success': True,
            'message': message,
            'new_credits': current_user.credits,
            'is_premium': current_user.is_premium
        })
    else:
        return jsonify({'success': False, 'error': 'Impossible d\'appliquer ce code'}), 400

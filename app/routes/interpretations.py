"""
Routes d'interprétations : rêves, signes, tirages, profil spirituel
"""
from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models import db, Interpretation
from app.services.ai_service import interpret_dream, interpret_sign, interpret_tarot, calculate_spiritual_profile
from datetime import datetime
import json

bp = Blueprint('interpretations', __name__)

@bp.route('/dream', methods=['GET', 'POST'])
@login_required
def dream():
    """Page d'interprétation de rêves"""
    if request.method == 'POST':
        # Vérifier les limites freemium
        if not current_user.can_interpret():
            return jsonify({
                'error': 'Tu as atteint ta limite mensuelle. Passe en Premium pour des interprétations illimitées ✨'
            }), 403

        data = request.get_json()
        dream_text = data.get('dream', '').strip()

        if not dream_text:
            return jsonify({'error': 'Décris ton rêve pour recevoir une interprétation'}), 400

        # Interpréter avec l'IA
        try:
            interpretation_result = interpret_dream(dream_text)

            # Sauvegarder dans la base
            interpretation = Interpretation(
                user_id=current_user.id,
                type='dream',
                user_input=dream_text,
                ai_response=json.dumps(interpretation_result, ensure_ascii=False)
            )
            db.session.add(interpretation)
            db.session.commit()

            return jsonify({
                'success': True,
                'interpretation': interpretation_result,
                'remaining': current_user.get_remaining_free_interpretations()
            })

        except Exception as e:
            return jsonify({'error': f'Erreur lors de l\'interprétation : {str(e)}'}), 500

    return render_template('interpretations/dream.html')

@bp.route('/sign', methods=['GET', 'POST'])
@login_required
def sign():
    """Page d'interprétation de signes & synchronicités"""
    if request.method == 'POST':
        if not current_user.can_interpret():
            return jsonify({
                'error': 'Tu as atteint ta limite mensuelle. Passe en Premium pour des interprétations illimitées ✨'
            }), 403

        data = request.get_json()
        sign_text = data.get('sign', '').strip()

        if not sign_text:
            return jsonify({'error': 'Décris le signe que tu as remarqué'}), 400

        try:
            interpretation_result = interpret_sign(sign_text)

            interpretation = Interpretation(
                user_id=current_user.id,
                type='sign',
                user_input=sign_text,
                ai_response=json.dumps(interpretation_result, ensure_ascii=False)
            )
            db.session.add(interpretation)
            db.session.commit()

            return jsonify({
                'success': True,
                'interpretation': interpretation_result,
                'remaining': current_user.get_remaining_free_interpretations()
            })

        except Exception as e:
            return jsonify({'error': f'Erreur lors de l\'interprétation : {str(e)}'}), 500

    return render_template('interpretations/sign.html')

@bp.route('/tarot', methods=['GET', 'POST'])
@login_required
def tarot():
    """Page de tirage intuitif"""
    if request.method == 'POST':
        if not current_user.can_interpret():
            return jsonify({
                'error': 'Tu as atteint ta limite mensuelle. Passe en Premium pour des interprétations illimitées ✨'
            }), 403

        data = request.get_json()
        selected_cards = data.get('cards', [])  # IDs des cartes sélectionnées

        if len(selected_cards) != 3:
            return jsonify({'error': 'Sélectionne exactement 3 cartes'}), 400

        try:
            # interpret_tarot attend directement les IDs des cartes
            interpretation_result = interpret_tarot(selected_cards)

            interpretation = Interpretation(
                user_id=current_user.id,
                type='tarot',
                user_input=json.dumps(selected_cards),
                ai_response=json.dumps(interpretation_result, ensure_ascii=False)
            )
            db.session.add(interpretation)
            db.session.commit()

            return jsonify({
                'success': True,
                'interpretation': interpretation_result,
                'remaining': current_user.get_remaining_free_interpretations()
            })

        except Exception as e:
            return jsonify({'error': f'Erreur lors de l\'interprétation : {str(e)}'}), 500

    return render_template('interpretations/tarot.html')

@bp.route('/spiritual-profile', methods=['GET', 'POST'])
@login_required
def spiritual_profile():
    """Questionnaire de profil spirituel"""
    if request.method == 'POST':
        # Récupérer les données du formulaire
        first_name = request.form.get('first_name', '').strip()
        birth_date_str = request.form.get('birth_date', '')
        favorite_color = request.form.get('favorite_color', '')
        element = request.form.get('element', '')

        # Parser la date
        try:
            birth_date = datetime.strptime(birth_date_str, '%Y-%m-%d').date() if birth_date_str else None
        except:
            birth_date = None

        # Mettre à jour le profil
        current_user.first_name = first_name
        current_user.birth_date = birth_date
        current_user.favorite_color = favorite_color
        current_user.element = element

        # Calculer le profil spirituel avec l'IA
        try:
            profile = calculate_spiritual_profile(
                first_name=first_name,
                birth_date=birth_date,
                favorite_color=favorite_color,
                element=element
            )

            current_user.soul_type = profile.get('soul_type', '')
            current_user.dominant_element = profile.get('dominant_element', '')
            current_user.vibratory_color = profile.get('vibratory_color', '')

        except Exception as e:
            # En cas d'erreur, valeurs par défaut
            current_user.soul_type = 'Âme en éveil'
            current_user.dominant_element = element
            current_user.vibratory_color = favorite_color

        db.session.commit()

        flash('Ton profil spirituel a été créé ✨', 'success')
        return redirect(url_for('main.dashboard'))

    return render_template('interpretations/spiritual_profile.html')

@bp.route('/history')
@login_required
def history():
    """Historique des interprétations (premium)"""
    if not current_user.is_premium:
        flash('Cette fonctionnalité est réservée aux membres Premium', 'warning')
        return redirect(url_for('premium.subscribe'))

    interpretations = current_user.interpretations.order_by(
        Interpretation.created_at.desc()
    ).all()

    return render_template('interpretations/history.html', interpretations=interpretations)

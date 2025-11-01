"""
Routes d'interprétations : rêves, signes, tirages, profil spirituel
"""
from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash, send_file
from flask_login import login_required, current_user
from app.models import db, Interpretation
from app.services.ai_service import interpret_dream, interpret_sign, interpret_tarot, calculate_spiritual_profile, generate_audio_guidance
from datetime import datetime
import json
import io

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
        first_name = data.get('first_name', '').strip()
        age = data.get('age', '').strip()
        city = data.get('city', '').strip()
        question = data.get('question', '').strip()

        if not first_name or not question:
            return jsonify({'error': 'Merci de remplir au moins ton prénom et ta question'}), 400

        try:
            # L'IA tire 3 cartes aléatoires et interprète
            interpretation_result = interpret_tarot(
                first_name=first_name,
                age=age,
                city=city,
                question=question
            )

            # Sauvegarder l'input utilisateur
            user_input = {
                'first_name': first_name,
                'age': age,
                'city': city,
                'question': question
            }

            interpretation = Interpretation(
                user_id=current_user.id,
                type='tarot',
                user_input=json.dumps(user_input, ensure_ascii=False),
                ai_response=json.dumps(interpretation_result, ensure_ascii=False)
            )
            db.session.add(interpretation)
            db.session.commit()

            return jsonify({
                'success': True,
                'interpretation': interpretation_result,
                'interpretation_id': interpretation.id,
                'remaining': current_user.get_remaining_free_interpretations()
            })

        except Exception as e:
            return jsonify({'error': 'Erreur lors de l\'interprétation : {}'.format(str(e))}), 500

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
    """Historique des interprétations (3 dernières pour gratuit, illimité pour premium)"""
    if current_user.is_premium:
        # Premium : toutes les interprétations
        interpretations = current_user.interpretations.order_by(
            Interpretation.created_at.desc()
        ).all()
    else:
        # Gratuit : 3 dernières seulement
        interpretations = current_user.interpretations.order_by(
            Interpretation.created_at.desc()
        ).limit(3).all()

    return render_template('interpretations/history.html', interpretations=interpretations)

@bp.route('/audio/<int:interpretation_id>')
@login_required
def generate_audio(interpretation_id):
    """Génère et renvoie l'audio d'une interprétation"""

    # Récupérer l'interprétation
    interpretation = Interpretation.query.get_or_404(interpretation_id)

    # Vérifier que l'utilisateur est propriétaire de l'interprétation
    if interpretation.user_id != current_user.id:
        return jsonify({'error': 'Accès non autorisé'}), 403

    try:
        # Récupérer le contenu de l'interprétation
        response = interpretation.get_response_dict()

        # Construire le texte de la guidance audio
        audio_text = ""

        if interpretation.type == 'tarot':
            user_data = interpretation.get_user_input_dict()
            first_name = user_data.get('first_name', '') if user_data else ''

            audio_text = "Bonjour {}. ".format(first_name) if first_name else "Bonjour. "
            audio_text += "Voici ta guidance spirituelle. "

            if response.get('interpretation'):
                audio_text += response['interpretation'] + " "

            if response.get('spiritual_message'):
                audio_text += response['spiritual_message'] + " "

            if response.get('personal_advice'):
                audio_text += "Mon conseil pour toi : " + response['personal_advice']

        elif interpretation.type == 'dream':
            audio_text = "Voici l'interprétation de ton rêve. "

            if response.get('symbolism'):
                audio_text += response['symbolism'] + " "

            if response.get('spiritual_message'):
                audio_text += response['spiritual_message'] + " "

            if response.get('personal_advice'):
                audio_text += "Mon conseil : " + response['personal_advice']

        elif interpretation.type == 'sign':
            audio_text = "Voici l'interprétation du signe que tu as reçu. "

            if response.get('symbolism'):
                audio_text += response['symbolism'] + " "

            if response.get('spiritual_message'):
                audio_text += response['spiritual_message'] + " "

            if response.get('personal_advice'):
                audio_text += "Mon conseil : " + response['personal_advice']

        # Générer l'audio avec OpenAI TTS
        audio_content = generate_audio_guidance(audio_text, voice='nova')

        # Créer un buffer pour renvoyer l'audio
        audio_buffer = io.BytesIO(audio_content)
        audio_buffer.seek(0)

        return send_file(
            audio_buffer,
            mimetype='audio/mpeg',
            as_attachment=False,
            download_name='guidance_{}.mp3'.format(interpretation_id)
        )

    except Exception as e:
        return jsonify({'error': 'Erreur lors de la génération audio : {}'.format(str(e))}), 500

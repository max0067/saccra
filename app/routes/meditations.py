"""
Routes pour les méditations guidées audio
"""
from flask import Blueprint, render_template, redirect, url_for, flash, request, send_file, jsonify
from flask_login import login_required, current_user
from app.models import db, Meditation, MeditationListen
from app.services.ai_service import generate_meditation_audio
from datetime import datetime
import io

bp = Blueprint('meditations', __name__, url_prefix='/meditations')


@bp.route('/')
@login_required
def library():
    """Bibliothèque de méditations"""
    # Filtrer par thème si demandé
    theme_filter = request.args.get('theme', '')

    query = Meditation.query.filter_by(is_active=True)

    if theme_filter:
        query = query.filter_by(theme=theme_filter)

    meditations = query.order_by(Meditation.theme, Meditation.duration_minutes).all()

    # Statistiques utilisateur
    remaining_meditations = current_user.get_remaining_meditations()
    monthly_count = current_user.get_monthly_meditations_count()

    return render_template(
        'meditations/library.html',
        meditations=meditations,
        remaining_meditations=remaining_meditations,
        monthly_count=monthly_count,
        theme_filter=theme_filter
    )


@bp.route('/<int:meditation_id>')
@login_required
def player(meditation_id):
    """Player de méditation"""
    meditation = Meditation.query.get_or_404(meditation_id)

    # Vérifier si l'utilisateur peut écouter
    if not current_user.can_listen_meditation():
        flash('Tu as atteint ta limite de méditations gratuites ce mois. Passe en Premium pour un accès illimité ! 🌟', 'warning')
        return redirect(url_for('premium.subscribe'))

    # Compter les statistiques
    total_listens = meditation.listens.count()
    user_has_listened = meditation.listens.filter_by(user_id=current_user.id).first() is not None

    return render_template(
        'meditations/player.html',
        meditation=meditation,
        total_listens=total_listens,
        user_has_listened=user_has_listened
    )


@bp.route('/<int:meditation_id>/audio')
@login_required
def audio(meditation_id):
    """Génère et stream l'audio de la méditation"""
    meditation = Meditation.query.get_or_404(meditation_id)

    # Vérifier si l'utilisateur peut écouter
    if not current_user.can_listen_meditation():
        return jsonify({'error': 'Limite atteinte'}), 403

    # Enregistrer l'écoute
    listen = MeditationListen(
        user_id=current_user.id,
        meditation_id=meditation.id
    )
    db.session.add(listen)
    db.session.commit()

    # Générer l'audio avec OpenAI TTS
    try:
        audio_content = generate_meditation_audio(meditation.script, voice='nova')
        audio_buffer = io.BytesIO(audio_content)
        audio_buffer.seek(0)

        return send_file(
            audio_buffer,
            mimetype='audio/mpeg',
            as_attachment=False,
            download_name='meditation_{}.mp3'.format(meditation.id)
        )
    except Exception as e:
        print('Erreur génération audio méditation: {}'.format(str(e)))
        return jsonify({'error': 'Erreur de génération audio'}), 500


@bp.route('/<int:meditation_id>/complete', methods=['POST'])
@login_required
def mark_complete(meditation_id):
    """Marque une méditation comme terminée"""
    # Trouver la dernière écoute de cet utilisateur pour cette méditation
    listen = MeditationListen.query.filter_by(
        user_id=current_user.id,
        meditation_id=meditation_id
    ).order_by(MeditationListen.listened_at.desc()).first()

    if listen:
        listen.completed = True
        db.session.commit()
        return jsonify({'success': True})

    return jsonify({'error': 'Écoute non trouvée'}), 404

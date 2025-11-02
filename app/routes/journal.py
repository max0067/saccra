"""
Routes pour le Journal Spirituel Quotidien
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from app.models import db, JournalEntry
from datetime import datetime, date, timedelta
from sqlalchemy import func

bp = Blueprint('journal', __name__, url_prefix='/journal')


@bp.route('/')
@login_required
def index():
    """Liste des entrées de journal de l'utilisateur"""

    # Récupérer toutes les entrées de l'utilisateur, triées par date décroissante
    entries = current_user.journal_entries.order_by(JournalEntry.date.desc()).all()

    # Vérifier si une entrée existe pour aujourd'hui
    today = date.today()
    today_entry = current_user.journal_entries.filter_by(date=today).first()

    # Statistiques
    total_entries = len(entries)
    current_streak = calculate_streak(current_user.id)

    # Moyennes des métriques (30 derniers jours)
    thirty_days_ago = date.today() - timedelta(days=30)
    recent_entries = current_user.journal_entries.filter(
        JournalEntry.date >= thirty_days_ago
    ).all()

    avg_mood = 0
    avg_energy = 0
    avg_clarity = 0

    if recent_entries:
        moods = [e.mood for e in recent_entries if e.mood]
        energies = [e.energy_level for e in recent_entries if e.energy_level]
        clarities = [e.mental_clarity for e in recent_entries if e.mental_clarity]

        avg_mood = round(sum(moods) / len(moods), 1) if moods else 0
        avg_energy = round(sum(energies) / len(energies), 1) if energies else 0
        avg_clarity = round(sum(clarities) / len(clarities), 1) if clarities else 0

    stats = {
        'total_entries': total_entries,
        'current_streak': current_streak,
        'avg_mood': avg_mood,
        'avg_energy': avg_energy,
        'avg_clarity': avg_clarity
    }

    return render_template('journal/index.html',
                         entries=entries,
                         today_entry=today_entry,
                         stats=stats)


@bp.route('/new', methods=['GET', 'POST'])
@login_required
def new():
    """Créer une nouvelle entrée de journal"""

    if request.method == 'POST':
        content = request.form.get('content', '').strip()
        entry_date = request.form.get('date')
        mood = request.form.get('mood', type=int)
        energy_level = request.form.get('energy_level', type=int)
        mental_clarity = request.form.get('mental_clarity', type=int)

        # Validation
        if not content:
            flash('Le contenu du journal est requis', 'error')
            return redirect(url_for('journal.new'))

        # Parser la date
        if entry_date:
            try:
                entry_date = datetime.strptime(entry_date, '%Y-%m-%d').date()
            except:
                entry_date = date.today()
        else:
            entry_date = date.today()

        # Vérifier si une entrée existe déjà pour cette date
        existing_entry = current_user.journal_entries.filter_by(date=entry_date).first()
        if existing_entry:
            flash('Une entrée existe déjà pour cette date. Modifie-la plutôt !', 'warning')
            return redirect(url_for('journal.edit', entry_id=existing_entry.id))

        # Créer l'entrée
        entry = JournalEntry(
            user_id=current_user.id,
            date=entry_date,
            content=content,
            mood=mood,
            energy_level=energy_level,
            mental_clarity=mental_clarity
        )

        db.session.add(entry)
        db.session.commit()

        flash('Entrée de journal créée ! ✨', 'success')

        # Générer l'analyse IA pour les premium
        if current_user.is_premium and current_user.premium_until and current_user.premium_until > datetime.utcnow():
            return redirect(url_for('journal.generate_analysis', entry_id=entry.id))

        return redirect(url_for('journal.view', entry_id=entry.id))

    # GET: afficher le formulaire
    # Par défaut, date = aujourd'hui
    default_date = date.today().strftime('%Y-%m-%d')

    return render_template('journal/form.html',
                         entry=None,
                         default_date=default_date)


@bp.route('/<int:entry_id>')
@login_required
def view(entry_id):
    """Voir une entrée de journal"""

    entry = JournalEntry.query.get_or_404(entry_id)

    # Vérifier que l'entrée appartient bien à l'utilisateur
    if entry.user_id != current_user.id:
        flash('Accès refusé', 'error')
        return redirect(url_for('journal.index'))

    return render_template('journal/view.html', entry=entry)


@bp.route('/<int:entry_id>/edit', methods=['GET', 'POST'])
@login_required
def edit(entry_id):
    """Modifier une entrée de journal"""

    entry = JournalEntry.query.get_or_404(entry_id)

    # Vérifier que l'entrée appartient bien à l'utilisateur
    if entry.user_id != current_user.id:
        flash('Accès refusé', 'error')
        return redirect(url_for('journal.index'))

    if request.method == 'POST':
        content = request.form.get('content', '').strip()
        mood = request.form.get('mood', type=int)
        energy_level = request.form.get('energy_level', type=int)
        mental_clarity = request.form.get('mental_clarity', type=int)

        if not content:
            flash('Le contenu du journal est requis', 'error')
            return redirect(url_for('journal.edit', entry_id=entry_id))

        # Mettre à jour l'entrée
        entry.content = content
        entry.mood = mood
        entry.energy_level = energy_level
        entry.mental_clarity = mental_clarity
        entry.updated_at = datetime.utcnow()

        # Réinitialiser l'analyse IA si le contenu a changé
        entry.ai_analysis = None
        entry.ai_analysis_generated_at = None

        db.session.commit()

        flash('Entrée mise à jour ! ✨', 'success')
        return redirect(url_for('journal.view', entry_id=entry.id))

    # GET: afficher le formulaire pré-rempli
    return render_template('journal/form.html',
                         entry=entry,
                         default_date=entry.date.strftime('%Y-%m-%d'))


@bp.route('/<int:entry_id>/delete', methods=['POST'])
@login_required
def delete(entry_id):
    """Supprimer une entrée de journal"""

    entry = JournalEntry.query.get_or_404(entry_id)

    # Vérifier que l'entrée appartient bien à l'utilisateur
    if entry.user_id != current_user.id:
        return jsonify({'success': False, 'error': 'Accès refusé'}), 403

    db.session.delete(entry)
    db.session.commit()

    return jsonify({'success': True, 'message': 'Entrée supprimée'})


@bp.route('/<int:entry_id>/generate-analysis')
@login_required
def generate_analysis(entry_id):
    """Générer l'analyse IA d'une entrée (Premium uniquement)"""

    # Vérifier premium
    if not current_user.is_premium or not current_user.premium_until or current_user.premium_until < datetime.utcnow():
        flash('Fonctionnalité réservée aux membres Premium', 'warning')
        return redirect(url_for('premium.subscribe'))

    entry = JournalEntry.query.get_or_404(entry_id)

    # Vérifier que l'entrée appartient bien à l'utilisateur
    if entry.user_id != current_user.id:
        flash('Accès refusé', 'error')
        return redirect(url_for('journal.index'))

    # Générer l'analyse IA
    from app.services.ai_service import analyze_journal_entry

    try:
        analysis = analyze_journal_entry(entry, current_user)
        entry.ai_analysis = analysis
        entry.ai_analysis_generated_at = datetime.utcnow()
        db.session.commit()

        flash('Analyse IA générée ! 🌟', 'success')
    except Exception as e:
        print(f'Erreur génération analyse IA: {str(e)}')
        flash('Erreur lors de la génération de l\'analyse. Réessaie plus tard.', 'error')

    return redirect(url_for('journal.view', entry_id=entry.id))


@bp.route('/stats')
@login_required
def stats():
    """Page de statistiques et graphiques"""

    # Récupérer toutes les entrées de l'utilisateur
    entries = current_user.journal_entries.order_by(JournalEntry.date).all()

    # Préparer les données pour les graphiques
    dates = []
    moods = []
    energies = []
    clarities = []

    for entry in entries:
        dates.append(entry.date.strftime('%Y-%m-%d'))
        moods.append(entry.mood if entry.mood else None)
        energies.append(entry.energy_level if entry.energy_level else None)
        clarities.append(entry.mental_clarity if entry.mental_clarity else None)

    chart_data = {
        'dates': dates,
        'moods': moods,
        'energies': energies,
        'clarities': clarities
    }

    # Statistiques globales
    total_entries = len(entries)
    current_streak = calculate_streak(current_user.id)

    # Meilleur jour (mood le plus élevé)
    best_day = None
    if entries:
        entries_with_mood = [e for e in entries if e.mood]
        if entries_with_mood:
            best_day = max(entries_with_mood, key=lambda e: e.mood)

    stats = {
        'total_entries': total_entries,
        'current_streak': current_streak,
        'best_day': best_day
    }

    return render_template('journal/stats.html',
                         chart_data=chart_data,
                         stats=stats)


def calculate_streak(user_id):
    """Calcule la série actuelle de jours consécutifs avec une entrée"""

    today = date.today()
    streak = 0
    current_date = today

    while True:
        entry = JournalEntry.query.filter_by(
            user_id=user_id,
            date=current_date
        ).first()

        if entry:
            streak += 1
            current_date -= timedelta(days=1)
        else:
            break

        # Limite de sécurité pour éviter les boucles infinies
        if streak > 365:
            break

    return streak

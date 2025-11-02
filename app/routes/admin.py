"""
Routes administrateur pour SACRA
Gestion des utilisateurs, codes promo, et statistiques
"""
from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash
from flask_login import login_required, current_user
from functools import wraps
from datetime import datetime, timedelta
from sqlalchemy import func
from app.models import db, User, Interpretation, PromoCode, SpiritualProfile, SiteContent, JournalEntry, BlogPost
from werkzeug.utils import secure_filename
import stripe
import os
import uuid

bp = Blueprint('admin', __name__)

# Configuration Stripe
stripe.api_key = os.environ.get('STRIPE_SECRET_KEY', '')

# Configuration upload
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB

def allowed_file(filename):
    """Vérifie si le fichier a une extension autorisée"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def admin_required(f):
    """Décorateur pour restreindre l'accès aux administrateurs"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            flash('Tu dois être connecté pour accéder à cette page', 'error')
            return redirect(url_for('auth.login'))
        if not current_user.is_admin:
            flash('Accès réservé aux administrateurs', 'error')
            return redirect(url_for('main.index'))
        return f(*args, **kwargs)
    return decorated_function


@bp.route('/dashboard')
@login_required
@admin_required
def dashboard():
    """Dashboard administrateur avec statistiques globales"""

    # Statistiques générales
    total_users = User.query.count()
    premium_users = User.query.filter_by(is_premium=True).count()
    total_interpretations = Interpretation.query.count()
    total_journals = JournalEntry.query.count()
    active_promo_codes = PromoCode.query.filter_by(is_active=True).count()

    # Nouveaux utilisateurs cette semaine
    week_ago = datetime.utcnow() - timedelta(days=7)
    new_users_week = User.query.filter(User.created_at >= week_ago).count()

    # Interprétations par type
    dream_count = Interpretation.query.filter_by(type='dream').count()
    sign_count = Interpretation.query.filter_by(type='sign').count()
    tarot_count = Interpretation.query.filter_by(type='tarot').count()

    # Derniers utilisateurs
    recent_users = User.query.order_by(User.created_at.desc()).limit(10).all()

    stats = {
        'total_users': total_users,
        'premium_users': premium_users,
        'free_users': total_users - premium_users,
        'total_interpretations': total_interpretations,
        'total_journals': total_journals,
        'active_promo_codes': active_promo_codes,
        'new_users_week': new_users_week,
        'dream_count': dream_count,
        'sign_count': sign_count,
        'tarot_count': tarot_count,
    }

    return render_template('admin/dashboard.html', stats=stats, recent_users=recent_users)


@bp.route('/users')
@login_required
@admin_required
def users():
    """Liste de tous les utilisateurs avec filtres"""

    page = request.args.get('page', 1, type=int)
    filter_type = request.args.get('filter', 'all')
    search = request.args.get('search', '')

    query = User.query

    # Filtres
    if filter_type == 'premium':
        query = query.filter_by(is_premium=True)
    elif filter_type == 'free':
        query = query.filter_by(is_premium=False)
    elif filter_type == 'admin':
        query = query.filter_by(is_admin=True)

    # Recherche
    if search:
        query = query.filter(
            (User.email.contains(search)) |
            (User.first_name.contains(search))
        )

    # Pagination
    users_paginated = query.order_by(User.created_at.desc()).paginate(
        page=page, per_page=20, error_out=False
    )

    return render_template('admin/users.html', users=users_paginated, filter_type=filter_type, search=search)


@bp.route('/users/<int:user_id>/add-credits', methods=['POST'])
@login_required
@admin_required
def add_credits(user_id):
    """Ajouter des crédits à un utilisateur"""

    user = User.query.get_or_404(user_id)
    data = request.get_json()
    credits = data.get('credits', 0)

    if credits <= 0 or credits > 1000:
        return jsonify({'success': False, 'error': 'Nombre de crédits invalide'}), 400

    user.credits += credits
    db.session.commit()

    return jsonify({
        'success': True,
        'message': '{} crédits ajoutés à {}'.format(credits, user.email),
        'new_credits': user.credits
    })


@bp.route('/users/<int:user_id>/toggle-premium', methods=['POST'])
@login_required
@admin_required
def toggle_premium(user_id):
    """Activer/désactiver le premium manuellement"""

    user = User.query.get_or_404(user_id)
    data = request.get_json()
    days = data.get('days', 30)

    if not user.is_premium or not user.premium_until or user.premium_until < datetime.utcnow():
        # Activer premium
        user.is_premium = True
        user.premium_until = datetime.utcnow() + timedelta(days=days)
        message = 'Premium activé pour {} jours'.format(days)
    else:
        # Désactiver premium
        user.is_premium = False
        user.premium_until = None
        message = 'Premium désactivé'

    db.session.commit()

    return jsonify({
        'success': True,
        'message': message,
        'is_premium': user.is_premium,
        'premium_until': user.premium_until.isoformat() if user.premium_until else None
    })


@bp.route('/users/<int:user_id>/toggle-admin', methods=['POST'])
@login_required
@admin_required
def toggle_admin(user_id):
    """Promouvoir/rétrograder un utilisateur admin"""

    user = User.query.get_or_404(user_id)

    # Ne pas se désadminer soi-même
    if user.id == current_user.id:
        return jsonify({'success': False, 'error': 'Tu ne peux pas modifier ton propre statut admin'}), 400

    user.is_admin = not user.is_admin
    db.session.commit()

    return jsonify({
        'success': True,
        'message': 'Admin {} pour {}'.format('activé' if user.is_admin else 'désactivé', user.email),
        'is_admin': user.is_admin
    })


@bp.route('/users/<int:user_id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_user(user_id):
    """Supprimer un utilisateur"""

    user = User.query.get_or_404(user_id)

    # Ne pas se supprimer soi-même
    if user.id == current_user.id:
        return jsonify({'success': False, 'error': 'Tu ne peux pas supprimer ton propre compte'}), 400

    email = user.email
    db.session.delete(user)
    db.session.commit()

    return jsonify({
        'success': True,
        'message': 'Utilisateur {} supprimé'.format(email)
    })


@bp.route('/promo-codes')
@login_required
@admin_required
def promo_codes():
    """Liste des codes promo"""

    codes = PromoCode.query.order_by(PromoCode.created_at.desc()).all()
    return render_template('admin/promo_codes.html', codes=codes)


@bp.route('/promo-codes/create', methods=['POST'])
@login_required
@admin_required
def create_promo_code():
    """Créer un nouveau code promo"""

    data = request.get_json()

    code = data.get('code', '').strip().upper()
    reward_type = data.get('reward_type')
    reward_value = data.get('reward_value', 0)
    max_uses = data.get('max_uses')
    expires_days = data.get('expires_days')
    description = data.get('description', '')

    # Validation
    if not code or len(code) < 3:
        return jsonify({'success': False, 'error': 'Code trop court (min 3 caractères)'}), 400

    if PromoCode.query.filter_by(code=code).first():
        return jsonify({'success': False, 'error': 'Ce code existe déjà'}), 400

    if reward_type not in ['credits', 'premium_days']:
        return jsonify({'success': False, 'error': 'Type de récompense invalide'}), 400

    if reward_value <= 0:
        return jsonify({'success': False, 'error': 'Valeur de récompense invalide'}), 400

    # Créer le code promo
    promo = PromoCode(
        code=code,
        reward_type=reward_type,
        reward_value=reward_value,
        max_uses=max_uses if max_uses and max_uses > 0 else None,
        expires_at=datetime.utcnow() + timedelta(days=expires_days) if expires_days else None,
        description=description,
        created_by=current_user.id
    )

    db.session.add(promo)
    db.session.commit()

    return jsonify({
        'success': True,
        'message': 'Code promo {} créé'.format(code),
        'code': {
            'id': promo.id,
            'code': promo.code,
            'reward_type': promo.reward_type,
            'reward_value': promo.reward_value
        }
    })


@bp.route('/promo-codes/<int:code_id>/toggle', methods=['POST'])
@login_required
@admin_required
def toggle_promo_code(code_id):
    """Activer/désactiver un code promo"""

    promo = PromoCode.query.get_or_404(code_id)
    promo.is_active = not promo.is_active
    db.session.commit()

    return jsonify({
        'success': True,
        'message': 'Code {} {}'.format(promo.code, 'activé' if promo.is_active else 'désactivé'),
        'is_active': promo.is_active
    })


@bp.route('/promo-codes/<int:code_id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_promo_code(code_id):
    """Supprimer un code promo"""

    promo = PromoCode.query.get_or_404(code_id)
    code = promo.code
    db.session.delete(promo)
    db.session.commit()

    return jsonify({
        'success': True,
        'message': 'Code promo {} supprimé'.format(code)
    })


@bp.route('/site-contents')
@login_required
@admin_required
def site_contents():
    """Gestion des contenus du site"""

    contents = SiteContent.query.order_by(SiteContent.category, SiteContent.key).all()

    # Grouper par catégorie
    contents_by_category = {}
    for content in contents:
        category = content.category or 'Général'
        if category not in contents_by_category:
            contents_by_category[category] = []
        contents_by_category[category].append(content)

    return render_template('admin/site_contents.html', contents_by_category=contents_by_category)


@bp.route('/site-contents/create', methods=['POST'])
@login_required
@admin_required
def create_site_content():
    """Créer un nouveau contenu"""

    data = request.get_json()
    key = data.get('key', '').strip()
    category = data.get('category', 'Général').strip()
    value = data.get('value', '').strip()
    description = data.get('description', '').strip()

    if not key or not value:
        return jsonify({'success': False, 'error': 'Clé et valeur obligatoires'}), 400

    # Vérifier que la clé n'existe pas
    if SiteContent.query.filter_by(key=key).first():
        return jsonify({'success': False, 'error': 'Cette clé existe déjà'}), 400

    content = SiteContent(
        key=key,
        category=category,
        value=value,
        description=description
    )
    db.session.add(content)
    db.session.commit()

    return jsonify({
        'success': True,
        'message': 'Contenu créé',
        'content': {
            'id': content.id,
            'key': content.key,
            'value': content.value
        }
    })


@bp.route('/site-contents/<int:content_id>/update', methods=['POST'])
@login_required
@admin_required
def update_site_content(content_id):
    """Mettre à jour un contenu"""

    content = SiteContent.query.get_or_404(content_id)
    data = request.get_json()
    new_value = data.get('value', '').strip()

    if not new_value:
        return jsonify({'success': False, 'error': 'Valeur obligatoire'}), 400

    content.value = new_value
    content.updated_at = datetime.utcnow()
    db.session.commit()

    return jsonify({
        'success': True,
        'message': 'Contenu mis à jour'
    })


@bp.route('/site-contents/<int:content_id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_site_content(content_id):
    """Supprimer un contenu"""

    content = SiteContent.query.get_or_404(content_id)
    db.session.delete(content)
    db.session.commit()

    return jsonify({
        'success': True,
        'message': 'Contenu supprimé'
    })


@bp.route('/users/<int:user_id>/payments')
@login_required
@admin_required
def user_payments(user_id):
    """Récupérer l'historique des paiements d'un utilisateur depuis Stripe"""

    user = User.query.get_or_404(user_id)

    # Vérifier si l'utilisateur a un customer_id Stripe
    if not user.stripe_customer_id:
        return jsonify({
            'success': True,
            'payments': []
        })

    try:
        # Récupérer les charges (payments) depuis Stripe
        charges = stripe.Charge.list(
            customer=user.stripe_customer_id,
            limit=100
        )

        payments = []
        for charge in charges.data:
            payments.append({
                'id': charge.id,
                'amount': '{:.2f}'.format(charge.amount / 100),
                'currency': charge.currency,
                'status': charge.status,
                'description': charge.description or 'Abonnement SACRA Premium',
                'date': datetime.fromtimestamp(charge.created).strftime('%d/%m/%Y à %H:%M'),
                'receipt_url': charge.receipt_url
            })

        return jsonify({
            'success': True,
            'payments': payments,
            'customer_id': user.stripe_customer_id
        })

    except stripe.error.StripeError as e:
        return jsonify({
            'success': False,
            'error': 'Erreur Stripe: {}'.format(str(e))
        }), 500
    except Exception as e:
        return jsonify({
            'success': False,
            'error': 'Erreur: {}'.format(str(e))
        }), 500


@bp.route('/interpretations')
@login_required
@admin_required
def interpretations():
    """Liste de toutes les interprétations avec filtres"""

    page = request.args.get('page', 1, type=int)
    filter_type = request.args.get('filter', 'all')
    search = request.args.get('search', '')

    query = Interpretation.query

    # Filtres par type
    if filter_type in ['dream', 'sign', 'tarot']:
        query = query.filter_by(type=filter_type)

    # Recherche par email ou prénom d'utilisateur
    if search:
        query = query.join(User).filter(
            (User.email.contains(search)) |
            (User.first_name.contains(search))
        )

    # Pagination
    interpretations_paginated = query.order_by(Interpretation.created_at.desc()).paginate(
        page=page, per_page=20, error_out=False
    )

    return render_template('admin/interpretations.html',
                          interpretations=interpretations_paginated,
                          filter_type=filter_type,
                          search=search)


@bp.route('/journals')
@login_required
@admin_required
def journals():
    """Liste de toutes les entrées de journal avec filtres"""

    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '')

    query = JournalEntry.query

    # Recherche par email ou prénom d'utilisateur
    if search:
        query = query.join(User).filter(
            (User.email.contains(search)) |
            (User.first_name.contains(search)) |
            (JournalEntry.content.contains(search))
        )

    # Pagination
    journals_paginated = query.order_by(JournalEntry.date.desc()).paginate(
        page=page, per_page=20, error_out=False
    )

    return render_template('admin/journals.html',
                          journals=journals_paginated,
                          search=search)


@bp.route('/blog')
@login_required
@admin_required
def blog():
    """Liste de tous les articles de blog"""

    page = request.args.get('page', 1, type=int)
    filter_status = request.args.get('filter', 'all')
    search = request.args.get('search', '')

    query = BlogPost.query

    # Filtres par statut
    if filter_status == 'published':
        query = query.filter_by(is_published=True)
    elif filter_status == 'draft':
        query = query.filter_by(is_published=False)

    # Recherche par titre ou contenu
    if search:
        query = query.filter(
            (BlogPost.title.contains(search)) |
            (BlogPost.content.contains(search))
        )

    # Pagination
    posts_paginated = query.order_by(BlogPost.created_at.desc()).paginate(
        page=page, per_page=20, error_out=False
    )

    return render_template('admin/blog.html',
                          posts=posts_paginated,
                          filter_status=filter_status,
                          search=search)


@bp.route('/blog/new', methods=['GET', 'POST'])
@login_required
@admin_required
def blog_new():
    """Créer un nouvel article de blog"""

    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        excerpt = request.form.get('excerpt', '').strip()
        content = request.form.get('content', '').strip()
        image_url = request.form.get('image_url', '').strip()
        meta_title = request.form.get('meta_title', '').strip()
        meta_description = request.form.get('meta_description', '').strip()
        is_published = request.form.get('is_published') == 'on'

        # Validation
        if not title or not content:
            flash('Le titre et le contenu sont obligatoires', 'error')
            return render_template('admin/blog_form.html', post=None)

        # Générer le slug à partir du titre
        slug = BlogPost.generate_slug(title)

        # Vérifier que le slug est unique
        existing_post = BlogPost.query.filter_by(slug=slug).first()
        if existing_post:
            # Ajouter un suffixe numérique si le slug existe déjà
            counter = 1
            while BlogPost.query.filter_by(slug=f'{slug}-{counter}').first():
                counter += 1
            slug = f'{slug}-{counter}'

        # Créer l'article
        post = BlogPost(
            author_id=current_user.id,
            title=title,
            slug=slug,
            excerpt=excerpt if excerpt else None,
            content=content,
            image_url=image_url if image_url else None,
            meta_title=meta_title if meta_title else title,
            meta_description=meta_description if meta_description else excerpt,
            is_published=is_published,
            published_at=datetime.utcnow() if is_published else None
        )

        db.session.add(post)
        db.session.commit()

        flash('Article créé avec succès !', 'success')
        return redirect(url_for('admin.blog'))

    return render_template('admin/blog_form.html', post=None)


@bp.route('/blog/<int:post_id>/edit', methods=['GET', 'POST'])
@login_required
@admin_required
def blog_edit(post_id):
    """Éditer un article de blog"""

    post = BlogPost.query.get_or_404(post_id)

    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        excerpt = request.form.get('excerpt', '').strip()
        content = request.form.get('content', '').strip()
        image_url = request.form.get('image_url', '').strip()
        meta_title = request.form.get('meta_title', '').strip()
        meta_description = request.form.get('meta_description', '').strip()
        is_published = request.form.get('is_published') == 'on'

        # Validation
        if not title or not content:
            flash('Le titre et le contenu sont obligatoires', 'error')
            return render_template('admin/blog_form.html', post=post)

        # Mettre à jour le slug si le titre a changé
        if title != post.title:
            new_slug = BlogPost.generate_slug(title)
            # Vérifier que le nouveau slug est unique
            existing_post = BlogPost.query.filter(
                BlogPost.slug == new_slug,
                BlogPost.id != post.id
            ).first()
            if existing_post:
                counter = 1
                while BlogPost.query.filter(
                    BlogPost.slug == f'{new_slug}-{counter}',
                    BlogPost.id != post.id
                ).first():
                    counter += 1
                new_slug = f'{new_slug}-{counter}'
            post.slug = new_slug

        # Mettre à jour l'article
        post.title = title
        post.excerpt = excerpt if excerpt else None
        post.content = content
        post.image_url = image_url if image_url else None
        post.meta_title = meta_title if meta_title else title
        post.meta_description = meta_description if meta_description else excerpt

        # Si on publie pour la première fois, définir la date de publication
        if is_published and not post.is_published:
            post.published_at = datetime.utcnow()

        post.is_published = is_published
        post.updated_at = datetime.utcnow()

        db.session.commit()

        flash('Article mis à jour avec succès !', 'success')
        return redirect(url_for('admin.blog'))

    return render_template('admin/blog_form.html', post=post)


@bp.route('/blog/<int:post_id>/delete', methods=['POST'])
@login_required
@admin_required
def blog_delete(post_id):
    """Supprimer un article de blog"""

    post = BlogPost.query.get_or_404(post_id)
    title = post.title

    db.session.delete(post)
    db.session.commit()

    return jsonify({
        'success': True,
        'message': 'Article "{}" supprimé'.format(title)
    })


@bp.route('/blog/<int:post_id>/toggle-publish', methods=['POST'])
@login_required
@admin_required
def blog_toggle_publish(post_id):
    """Publier/dépublier un article"""

    post = BlogPost.query.get_or_404(post_id)

    # Inverser le statut de publication
    post.is_published = not post.is_published

    # Si on publie pour la première fois, définir la date de publication
    if post.is_published and not post.published_at:
        post.published_at = datetime.utcnow()

    db.session.commit()

    return jsonify({
        'success': True,
        'message': 'Article {} {}'.format(post.title, 'publié' if post.is_published else 'dépublié'),
        'is_published': post.is_published
    })


@bp.route('/blog/upload-image', methods=['POST'])
@login_required
@admin_required
def blog_upload_image():
    """Upload une image pour un article de blog"""

    # Vérifier qu'un fichier a été envoyé
    if 'image' not in request.files:
        return jsonify({'success': False, 'error': 'Aucun fichier envoyé'}), 400

    file = request.files['image']

    # Vérifier que le fichier a un nom
    if file.filename == '':
        return jsonify({'success': False, 'error': 'Aucun fichier sélectionné'}), 400

    # Vérifier l'extension
    if not allowed_file(file.filename):
        return jsonify({
            'success': False,
            'error': 'Type de fichier non autorisé. Utilisez: ' + ', '.join(ALLOWED_EXTENSIONS)
        }), 400

    # Vérifier la taille du fichier
    file.seek(0, os.SEEK_END)
    file_size = file.tell()
    file.seek(0)  # Retour au début du fichier

    if file_size > MAX_FILE_SIZE:
        return jsonify({
            'success': False,
            'error': 'Fichier trop volumineux (max 5MB)'
        }), 400

    try:
        # Générer un nom de fichier unique
        ext = file.filename.rsplit('.', 1)[1].lower()
        filename = '{}.{}'.format(uuid.uuid4().hex, ext)

        # Chemin de sauvegarde
        upload_dir = os.path.join(os.getcwd(), 'app', 'static', 'uploads', 'blog')
        os.makedirs(upload_dir, exist_ok=True)
        filepath = os.path.join(upload_dir, filename)

        # Sauvegarder le fichier
        file.save(filepath)

        # Générer l'URL publique
        image_url = '/static/uploads/blog/{}'.format(filename)

        return jsonify({
            'success': True,
            'url': image_url,
            'filename': filename
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': 'Erreur lors de l\'upload: {}'.format(str(e))
        }), 500

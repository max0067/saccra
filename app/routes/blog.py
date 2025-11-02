"""
Routes pour le blog SACRA
"""
from flask import Blueprint, render_template, abort
from app.models import db, BlogPost
from sqlalchemy import desc

bp = Blueprint('blog', __name__, url_prefix='/blog')


@bp.route('/')
def index():
    """Liste des articles de blog publiés"""
    # Récupérer tous les articles publiés, triés par date de publication (plus récent en premier)
    posts = BlogPost.query.filter_by(is_published=True).order_by(desc(BlogPost.published_at)).all()

    return render_template('blog/index.html', posts=posts)


@bp.route('/<slug>')
def article(slug):
    """Affichage d'un article de blog"""
    # Récupérer l'article par son slug
    post = BlogPost.query.filter_by(slug=slug, is_published=True).first_or_404()

    # Incrémenter le compteur de vues
    post.views += 1
    db.session.commit()

    # Récupérer les 3 articles les plus récents (hors article actuel) pour les suggestions
    related_posts = BlogPost.query.filter(
        BlogPost.is_published == True,
        BlogPost.id != post.id
    ).order_by(desc(BlogPost.published_at)).limit(3).all()

    return render_template('blog/article.html', post=post, related_posts=related_posts)

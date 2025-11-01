"""
Routes pour le Coach Spirituel IA (Chatbot)
"""
from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user
from app.models import db, Conversation, ChatMessage
from app.services.ai_service import generate_chat_response
from datetime import datetime
import json

bp = Blueprint('chat', __name__)


@bp.route('/coach')
@login_required
def coach():
    """Page principale du coach spirituel IA"""
    # Récupérer les conversations récentes
    conversations = current_user.conversations.order_by(
        Conversation.updated_at.desc()
    ).limit(10).all()

    # Compter les messages restants
    remaining_messages = current_user.get_remaining_chat_messages()

    return render_template('chat/coach.html',
                          conversations=conversations,
                          remaining_messages=remaining_messages)


@bp.route('/coach/conversation/<int:conversation_id>')
@login_required
def view_conversation(conversation_id):
    """Voir une conversation spécifique"""
    conversation = Conversation.query.get_or_404(conversation_id)

    # Vérifier que l'utilisateur est propriétaire
    if conversation.user_id != current_user.id:
        return jsonify({'error': 'Accès non autorisé'}), 403

    # Récupérer tous les messages
    messages = conversation.messages.all()

    return render_template('chat/conversation.html',
                          conversation=conversation,
                          messages=messages,
                          remaining_messages=current_user.get_remaining_chat_messages())


@bp.route('/coach/send', methods=['POST'])
@login_required
def send_message():
    """Envoyer un message au coach spirituel"""

    # Vérifier les limites
    if not current_user.can_send_chat_message():
        return jsonify({
            'error': 'Tu as atteint ta limite de 5 messages gratuits pour aujourd\'hui. Passe en Premium pour des conversations illimitées ! ✨',
            'limit_reached': True
        }), 403

    data = request.get_json()
    message_content = data.get('message', '').strip()
    conversation_id = data.get('conversation_id')

    if not message_content:
        return jsonify({'error': 'Message vide'}), 400

    try:
        # Récupérer ou créer une conversation
        if conversation_id:
            conversation = Conversation.query.get(conversation_id)
            if not conversation or conversation.user_id != current_user.id:
                return jsonify({'error': 'Conversation non trouvée'}), 404
        else:
            # Nouvelle conversation
            conversation = Conversation(user_id=current_user.id)
            db.session.add(conversation)
            db.session.flush()  # Pour obtenir l'ID

        # Sauvegarder le message de l'utilisateur
        user_message = ChatMessage(
            conversation_id=conversation.id,
            is_user=True,
            content=message_content
        )
        db.session.add(user_message)

        # Construire le profil utilisateur pour personnalisation
        user_profile = {
            'first_name': current_user.first_name,
            'soul_type': current_user.soul_type,
            'dominant_element': current_user.dominant_element
        }

        # Récupérer l'historique de la conversation
        previous_messages = conversation.messages.order_by(ChatMessage.created_at).all()
        conversation_history = []
        for msg in previous_messages:
            conversation_history.append({
                'role': 'user' if msg.is_user else 'assistant',
                'content': msg.content
            })

        # Générer la réponse de l'IA
        ai_response = generate_chat_response(
            user_message=message_content,
            user_profile=user_profile,
            conversation_history=conversation_history
        )

        # Sauvegarder la réponse de l'IA
        ai_message = ChatMessage(
            conversation_id=conversation.id,
            is_user=False,
            content=ai_response
        )
        db.session.add(ai_message)

        # Générer un titre pour la conversation si c'est le premier message
        if not conversation.title:
            # Titre = premiers mots de la question (max 50 caractères)
            title = message_content[:50]
            if len(message_content) > 50:
                title += '...'
            conversation.title = title

        # Mettre à jour updated_at
        conversation.updated_at = datetime.utcnow()

        db.session.commit()

        return jsonify({
            'success': True,
            'conversation_id': conversation.id,
            'user_message': {
                'id': user_message.id,
                'content': user_message.content,
                'created_at': user_message.created_at.isoformat(),
                'is_user': True
            },
            'ai_message': {
                'id': ai_message.id,
                'content': ai_message.content,
                'created_at': ai_message.created_at.isoformat(),
                'is_user': False
            },
            'remaining_messages': current_user.get_remaining_chat_messages()
        })

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Erreur lors de la génération de la réponse : {}'.format(str(e))}), 500


@bp.route('/coach/history')
@login_required
def history():
    """Historique des conversations"""

    # Si gratuit : 7 derniers jours seulement
    if not current_user.is_premium:
        from datetime import timedelta
        seven_days_ago = datetime.utcnow() - timedelta(days=7)
        conversations = current_user.conversations.filter(
            Conversation.created_at >= seven_days_ago
        ).order_by(Conversation.updated_at.desc()).all()
    else:
        # Premium : toutes les conversations
        conversations = current_user.conversations.order_by(
            Conversation.updated_at.desc()
        ).all()

    return render_template('chat/history.html',
                          conversations=conversations)


@bp.route('/coach/delete/<int:conversation_id>', methods=['POST'])
@login_required
def delete_conversation(conversation_id):
    """Supprimer une conversation"""

    conversation = Conversation.query.get_or_404(conversation_id)

    # Vérifier que l'utilisateur est propriétaire
    if conversation.user_id != current_user.id:
        return jsonify({'error': 'Accès non autorisé'}), 403

    db.session.delete(conversation)
    db.session.commit()

    return jsonify({
        'success': True,
        'message': 'Conversation supprimée'
    })

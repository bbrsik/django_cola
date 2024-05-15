from django.db.models import QuerySet
from message.models import Chat, Message


def serialize_chats(qs: QuerySet):
    chats = []
    for chat in qs:
        chats.append({
            'created_at': chat.created_at.strftime("%D %H:%M:%S"),
            'id': chat.id,
            'name': chat.name,
        })
    return chats


def serialize_messages(qs: QuerySet):
    messages = []
    for message in qs:
        messages.append({
            'created_at': message.created_at.strftime("%D %H:%M:%S"),
            'user': message.user,
            'text': message.text,
            'id': message.id,
            'replies_history': serialize_messages(message.get_replies_history())
        })
    return messages

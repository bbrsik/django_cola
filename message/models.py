from django.db import models
from django.contrib.auth.models import User
from user.models import Profile


class Chat(models.Model):
    name = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return (
            f"NAME: {self.name}, "
            f"ID: {self.id}"
        )


class Message(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    reply_on = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)

    def get_replies_history(self):
        current = self.reply_on
        replies = []
        while current is not None:
            replies.append(current)
            current = current.reply_on
        return replies

    def __str__(self):
        return (
            f"CHAT {self.chat}; "
            f"DATE: ({self.created_at:%Y-%m-%d %H:%M}): "
            f"USER: {self.user}; "
            f"MESSAGE: {self.text}"
        )


class Badword(models.Model):
    word = models.TextField()

    def __str__(self):
        return (
            f"WORD: {self.word} "
        )

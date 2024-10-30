from django.contrib.auth.models import User
from django.db import models


def get_roles():
    return {"user": "user", "system": "system", "assistant": "assistant"}


class ChatSession(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.DO_NOTHING, default=None
    )
    topic = models.CharField(max_length=255)
    creation_date_time = models.DateTimeField(auto_now_add=True)


class Message(models.Model):
    session = models.ForeignKey(
        ChatSession,
        on_delete=models.CASCADE,
        default=[],
    )
    role = models.CharField(max_length=16, choices=get_roles())
    content = models.CharField(max_length=1024)
    temperature = models.DecimalField(max_digits=2, decimal_places=1)
    creation_date_time = models.DateTimeField(auto_now_add=True)

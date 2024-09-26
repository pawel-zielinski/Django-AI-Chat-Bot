from django.contrib.auth.models import User
from django.db import models


class ChatSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    topic = models.CharField(max_length=255)
    creation_date_time = models.DateTimeField(auto_now_add=True)
    qa = models.ForeignKey('QuestionAnswer', on_delete=models.CASCADE)


class QuestionAnswer(models.Model):
    question = models.CharField(max_length=255)
    answer = models.CharField(max_length=255)

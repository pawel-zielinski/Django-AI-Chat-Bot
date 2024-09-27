from django.contrib import admin

from bot.models import Message, QuestionAnswer, ChatSession

admin.site.register(Message)
admin.site.register(QuestionAnswer)
admin.site.register(ChatSession)

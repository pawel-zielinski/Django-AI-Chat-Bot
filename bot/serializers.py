from rest_framework.serializers import BaseSerializer

from .models import ChatSession


class BotSerializer(BaseSerializer):
    class Meta:
        model = ChatSession
        fields = ('user', 'topic', 'creation_date_time', 'qa')
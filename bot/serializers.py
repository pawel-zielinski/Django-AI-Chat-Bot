from rest_framework.exceptions import ValidationError
from rest_framework.serializers import BaseSerializer
from rest_framework import serializers

from .models import ChatSession, Message


class BotSerializer(BaseSerializer):
    class Meta:
        model = ChatSession
        fields = ("user", "topic", "creation_date_time", "qa")


class MessageSerializer(serializers.Serializer):
    class Meta:
        model = Message
        fields = ("role", "content", "temperature")

    def validate_role(self, value):
        if value not in ["user", "system", "assistant"]:
            raise ValidationError(
                f"Invalid role {value}. Choose one of the following: user, system, assistant."
            )

    def validate_temperature(self, value):
        if 0.1 > value > 0.9:
            raise ValidationError(
                f"Invalid temperature {value}. Temperature can be chosen from range <0.1; 0.9>."
            )

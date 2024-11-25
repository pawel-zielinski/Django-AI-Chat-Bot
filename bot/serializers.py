from django.contrib.auth.models import User
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import BaseSerializer
from rest_framework import serializers

from .models import ChatSession, Message


class RoomSerializer(BaseSerializer):
    class Meta:
        model = ChatSession
        fields = ("user", "topic", "creation_date_time")

    def to_representation(self, instance):
        return {
            "topic": instance.topic,
            "creation_date_time": instance.creation_date_time,
            "qa": self.qa_to_json(instance.message_set.all()),
        }

    @staticmethod
    def qa_to_json(qa):
        response = {}
        for creation_date_time, content, role in qa.values_list(
            "creation_date_time", "content", "role"
        ):
            response[creation_date_time.strftime("%d %b %Y %H:%M:%S")] = {
                role: content,
            }
        return response


class SessionsSerializer(serializers.Serializer):
    class Meta:
        model = ChatSession
        fields = ("pk", "topic")

    def to_representation(self, instance):
        return {
            "pk": instance.pk,
            "topic": instance.topic,
            "creation_date_time": instance.creation_date_time,
        }

    def to_internal_value(self, data):
        return {
            "user": self.context.get("request").user,
        }

    def create(self, validated_data):
        return ChatSession.objects.create(**validated_data)


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ("id", "session", "role", "content", "temperature")

    @staticmethod
    def validate_role(value):
        if value not in ["user", "system", "assistant"]:
            raise ValidationError(
                f"Invalid role {value}. Choose one of the following: user, system, assistant."
            )
        return value

    @staticmethod
    def validate_temperature(value):
        if 0.1 > value > 0.9:
            raise ValidationError(
                f"Invalid temperature {value}. Temperature can be chosen from range <0.1; 0.9>."
            )
        return value

    def create(self, validated_data):
        return Message.objects.create(**validated_data)

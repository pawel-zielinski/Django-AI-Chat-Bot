from rest_framework.exceptions import ValidationError
from rest_framework.serializers import BaseSerializer
from rest_framework import serializers

from .models import ChatSession, Message


class RoomSerializer(BaseSerializer):
    class Meta:
        model = ChatSession
        fields = ("user", "topic", "creation_date_time", "qa")

    def to_representation(self, instance):
        return {
            "topic": instance.topic,
            "creation_date_time": instance.creation_date_time,
            "qa": self.qa_to_json(instance.questionanswer_set.all()),
        }

    @staticmethod
    def qa_to_json(qa):
        response = {}
        for pk, question, answer in qa.values_list("pk", "question", "answer"):
            response[pk] = {question: answer}
        return response


class SessionsSerializer(serializers.Serializer):
    class Meta:
        model = ChatSession
        fields = ("pk", "topic", "creation_date_time")

    def to_representation(self, instance):
        return {
            "pk": instance.pk,
            "topic": instance.topic,
            "creation_date_time": instance.creation_date_time,
        }


class MessageSerializer(serializers.Serializer):
    class Meta:
        model = Message
        fields = ("session", "role", "content", "temperature")

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

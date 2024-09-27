from rest_framework import viewsets, status
from rest_framework.mixins import RetrieveModelMixin, ListModelMixin, CreateModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from .models import ChatSession, QuestionAnswer
from .permissions import HasPermissionToSession
from .serializers import RoomSerializer, MessageSerializer, SessionsSerializer

from openai import OpenAI


class SessionsViewSet(
    GenericViewSet, RetrieveModelMixin, ListModelMixin, CreateModelMixin
):
    queryset = ChatSession.objects.all()
    serializer_class = RoomSerializer
    permission_classes = (
        IsAuthenticated,
        # HasPermissionToSession
    )

    def get_serializer_class(self):
        if self.action == "list_all_sessions":
            return SessionsSerializer
        return RoomSerializer

    @action(detail=False, methods=["get"], serializer_class=(SessionsSerializer,))
    def list_all_sessions(self, request, *args, **kwargs):
        queryset = ChatSession.objects.filter(user=request.user)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["get"])
    def retrieve_session(self, request, *args, **kwargs):
        # odczyt odpowiedzi z modelu
        return super().retrieve(request, *args, **kwargs)


class PromptViewset(GenericViewSet, RetrieveModelMixin, CreateModelMixin):
    queryset = ChatSession.objects.all()
    serializer_class = RoomSerializer
    permission_classes = (IsAuthenticated, HasPermissionToSession)
    CLIENT = OpenAI(api_key="your-api-key")

    @action(detail=False, methods=["post"], serializer_class=MessageSerializer)
    def create_question(self, request, *args, **kwargs):
        serializer = self.action["kwargs"].get("serializer_class")(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        self.chat_prompt(serializer)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

    def chat_prompt(self, serializer):
        temperature = serializer.data.popitem("temperature")
        response = self.CLIENT.chat.completions.create(
            model="gpt-3.5-turbo", messages=[serializer.data], **temperature
        )
        self.save_qa(
            serializer.data.get("session"),
            serializer.data.get("content"),
            response.choices[0].message.content,
        )

    @staticmethod
    def save_qa(session, question, answer):
        QuestionAnswer.objects.create(session=session, question=question, answer=answer)

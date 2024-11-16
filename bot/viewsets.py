import os

from rest_framework import viewsets, status
from rest_framework.mixins import (
    RetrieveModelMixin,
    ListModelMixin,
    CreateModelMixin,
    DestroyModelMixin,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet
from rest_framework_simplejwt.tokens import RefreshToken

from .models import ChatSession, Message
from .permissions import HasPermissionToSession
from .serializers import RoomSerializer, MessageSerializer, SessionsSerializer

import google.generativeai as genai

genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))


class PromptViewSet(
    GenericViewSet,
    RetrieveModelMixin,
    ListModelMixin,
    CreateModelMixin,
    DestroyModelMixin,
):
    queryset = ChatSession.objects.all()
    serializer_class = RoomSerializer
    permission_classes = (IsAuthenticated,)
    serializer_action_classes = {
        "list_all_sessions": SessionsSerializer,
        "create": SessionsSerializer,
        "retrieve_session": RoomSerializer,
        "create_question": MessageSerializer,
    }

    def get_serializer_class(self):
        return self.serializer_action_classes.get(self.action, RoomSerializer)

    @action(
        methods=["get"],
        detail=False,
    )
    def list_all_sessions(self, request, *args, **kwargs):
        queryset = self.filter_queryset(ChatSession.objects.filter(user=request.user))
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(
        detail=True,
        methods=["get"],
        permission_classes=(
            IsAuthenticated,
            HasPermissionToSession,
        ),
        queryset=ChatSession.objects.all(),
    )
    def retrieve_session(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

    @action(detail=False, methods=["post"])
    def create_question(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid(raise_exception=True):
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        response_text, response_date = self.chat_prompt(serializer)
        return Response(
            {'response_text': response_text, 'response_date': response_date}, status=status.HTTP_201_CREATED, headers=headers
        )

    def chat_prompt(self, serializer):
        model = self.get_ai_model()
        history = self.create_history(serializer)
        chat = self.start_ai_chat(history, model)
        temperature = float(serializer.data.get("temperature"))
        response = chat.send_message(serializer.data.get("content"), stream=False).text
        return response, self.save_qa(serializer.data.get("session"), response, temperature).creation_date_time

    @staticmethod
    def start_ai_chat(history, model):
        return model.start_chat(
            history=history,
        )

    @staticmethod
    def get_ai_model():
        return genai.GenerativeModel("gemini-1.5-flash")

    @staticmethod
    def create_history(serializer):
        history = []
        for role, content in Message.objects.filter(
            session_id=serializer.data.get("session")
        ).values_list("role", "content"):
            history.append({"role": role, "parts": content})
        return history

    @staticmethod
    def save_qa(session, answer, temperature):
        return Message.objects.create(
            session_id=session, role="model", content=answer, temperature=temperature
        )


class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    @staticmethod
    def post(request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)

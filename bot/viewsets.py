import os

from rest_framework import viewsets, status
from rest_framework.mixins import RetrieveModelMixin, ListModelMixin, CreateModelMixin
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


class SessionsViewSet(
    GenericViewSet, RetrieveModelMixin, ListModelMixin, CreateModelMixin
):
    queryset = ChatSession.objects.all()
    serializer_class = RoomSerializer
    permission_classes = (IsAuthenticated,)

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

    @action(
        detail=True,
        methods=["get"],
        permission_classes=(
            IsAuthenticated,
            HasPermissionToSession,
        ),
    )
    def retrieve_session(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)


class PromptViewSet(GenericViewSet, RetrieveModelMixin, CreateModelMixin):
    queryset = ChatSession.objects.all()
    serializer_class = RoomSerializer
    permission_classes = (IsAuthenticated,)

    def get_serializer_class(self):
        if self.action == "create_question":
            return MessageSerializer
        return RoomSerializer

    @action(detail=False, methods=["post"])
    def create_question(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        self.chat_prompt(serializer)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

    def chat_prompt(self, serializer):
        model = genai.GenerativeModel("gemini-1.5-flash")
        history = self.create_history(serializer)
        chat = model.start_chat(
            history=history,
        )
        temperature = float(serializer.data.get("temperature"))
        response = chat.send_message(serializer.data.get("content"), stream=False)
        self.save_qa(serializer.data.get("session"), response.text, temperature)

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
        Message.objects.create(
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

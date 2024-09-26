from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import ChatSession
from .permissions import HasPermissionToSession
from .serializers import BotSerializer


class SessionsViewSet(viewsets.GenericViewSet, viewsets.mixins.RetrieveModelMixin, viewsets.mixins.ListModelMixin):
    queryset = ChatSession.objects.all()
    serializer_class = BotSerializer
    permission_classes = (IsAuthenticated, HasPermissionToSession)

    @action(detail=False, methods=['get'])
    def list_all_sessions(self, request, *args, **kwargs):
        self.queryset = ChatSession.objects.filter(user=request.user)
        return super().list(request, *args, **kwargs)

    @action(detail=True, methods=['get'])
    def retrieve_session(self, request, *args, **kwargs):
        # odczyt odpowiedzi z modelu
        return super().retrieve(request, *args, **kwargs)

    @action(detail=False, methods=['post'])
    def create_question(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        # prompt chata i zapis odpowiedzi do modelu
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

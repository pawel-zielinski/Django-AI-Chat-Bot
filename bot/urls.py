from django.urls import path

from .viewsets import PromptViewSet
from rest_framework_simplejwt import views as jwt_views

urlpatterns = [
    path(
        "home/",
        PromptViewSet.as_view({"get": "list_all_sessions"}),
        name="sessions-list",
    ),
    path(
        "home/<int:pk>",
        PromptViewSet.as_view({"get": "retrieve_session"}),
        name="sessions-detail",
    ),
    path(
        "create_session",
        PromptViewSet.as_view({"post": "create"}),
        name="sessions-create",
    ),
    path(
        "home/<int:pk>/delete",
        PromptViewSet.as_view({"delete": "destroy"}),
        name="sessions-delete",
    ),
    path("token/", jwt_views.TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", jwt_views.TokenRefreshView.as_view(), name="token_refresh"),
    path(
        "create_question",
        PromptViewSet.as_view({"post": "create_question"}),
        name="message-create",
    ),
    path(
        "create_topic",
        PromptViewSet.as_view({"post": "create_topic"}),
        name="topic_create",
    ),
]

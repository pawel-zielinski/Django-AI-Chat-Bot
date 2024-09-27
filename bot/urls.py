from django.urls import path
from rest_framework import routers

from .viewsets import SessionsViewSet, PromptViewset

router = routers.SimpleRouter()
router.register(r"session", PromptViewset, basename="sessions")
urlpatterns = [
    path(
        "home/",
        SessionsViewSet.as_view({"get": "list_all_sessions"}),
        name="sessions-list",
    ),
    path(
        "home/<int:pk>",
        SessionsViewSet.as_view({"get": "retrieve_session"}),
        name="sessions-detail",
    ),
    path(
        "create_session",
        SessionsViewSet.as_view({"post": "create"}),
        name="sessions-create",
    ),
]
urlpatterns += router.urls

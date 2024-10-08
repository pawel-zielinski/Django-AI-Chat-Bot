from django.urls import path
from rest_framework import routers

from .viewsets import SessionsViewSet, PromptViewSet
from rest_framework_simplejwt import views as jwt_views

router = routers.SimpleRouter()
router.register(r"session", PromptViewSet, basename="sessions")
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
    path("token/", jwt_views.TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", jwt_views.TokenRefreshView.as_view(), name="token_refresh"),
]
urlpatterns += router.urls

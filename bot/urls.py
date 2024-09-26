from rest_framework import routers

from .viewsets import SessionsViewSet

router = routers.SimpleRouter()
router.register(r'sessions', SessionsViewSet, basename='sessions')
urlpatterns = router.urls

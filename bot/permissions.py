from rest_framework import permissions

from .models import ChatSession


class HasPermissionToSession(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            getattr(
                ChatSession.objects.filter(
                    pk=request.parser_context["kwargs"]["pk"]
                ).first(),
                "user",
                "",
            )
            == request.user
        )

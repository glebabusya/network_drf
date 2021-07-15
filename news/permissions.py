from rest_framework import permissions
from .models import Comment, Note


class IsAuthorOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        if isinstance(obj, Note):
            return obj.content_object.id == request.user.id

        return obj.author.id == request.user.id

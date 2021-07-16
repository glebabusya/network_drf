from rest_framework import permissions

from users.models import NetworkUser


class IsOwnerOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.id == request.user.id


class IsNotAuthenticated(permissions.BasePermission):
    def has_permission(self, request, view):
        return not request.user.is_authenticated


class IsOpenOrFriend(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if not obj.closed:
            return True

        return obj.friends.filter(id=request.user.id).exists()

    def has_permission(self, request, view):
        id = int(request.get_full_path().split('/')[2])
        user = NetworkUser.objects.get(id=id)
        if not user.closed:
            return True

        return user.friends.filter(id=request.user.id).exists()

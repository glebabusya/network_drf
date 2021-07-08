from rest_framework import permissions


class IsStaffOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        print(obj.staff.filter(id=request.user.id))
        print(obj.staff.filter(id=request.user.id).exists())
        print()
        return obj.staff.filter(id=request.user.id).exists()
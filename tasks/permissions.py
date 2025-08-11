from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission: write actions allowed only to owner (or staff).
    Read-only allowed to anyone (or at least authenticated for creation).
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        # write permissions only for owner or staff
        return obj.owner == request.user or request.user.is_staff

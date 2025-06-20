from rest_framework import permissions

class IsOwnerViaMaison(permissions.BasePermission):
    """Permission pour n'autoriser que le propriétaire de la maison à gérer ses chambres."""
    def has_object_permission(self, request, view, obj):
        return obj.proprietaire_id == request.user.id 
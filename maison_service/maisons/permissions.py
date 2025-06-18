from rest_framework import permissions

class IsOwner(permissions.BasePermission):
    """Permission pour n'autoriser que le propriétaire à accéder/modifier sa maison."""
    def has_object_permission(self, request, view, obj):
        return obj.proprietaire_id == request.user.id 
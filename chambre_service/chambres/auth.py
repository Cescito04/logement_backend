from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import permissions

class JWTOnlyAuthentication(JWTAuthentication):
    def get_user(self, validated_token):
        class SimpleUser:
            def __init__(self, user_id):
                self.id = user_id
                self.is_authenticated = True
        user_id = validated_token.get('user_id')
        return SimpleUser(user_id)

class IsJWTAuthenticated(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and hasattr(request.user, 'id')) 
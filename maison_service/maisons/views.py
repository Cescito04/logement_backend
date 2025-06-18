from django.shortcuts import render
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from .models import Maison
from .serializers import MaisonSerializer
from .permissions import IsOwner

# Create your views here.

class MaisonViewSet(viewsets.ModelViewSet):
    serializer_class = MaisonSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get_queryset(self):
        # Retourne uniquement les maisons du propriétaire connecté
        return Maison.objects.filter(proprietaire_id=self.request.user.id)

    def perform_create(self, serializer):
        # proprietaire_id vient du token JWT
        serializer.save(proprietaire_id=self.request.user.id)

    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def create_test_user(self, request):
        """Créer un utilisateur de test et retourner un token JWT"""
        try:
            # Créer un utilisateur de test
            user, created = User.objects.get_or_create(
                username='test_user',
                defaults={
                    'email': 'test@example.com',
                    'first_name': 'Test',
                    'last_name': 'User'
                }
            )
            
            # Générer le token JWT
            refresh = RefreshToken.for_user(user)
            access_token = refresh.access_token
            
            return Response({
                'message': 'Utilisateur de test créé avec succès',
                'access_token': str(access_token),
                'refresh_token': str(refresh),
                'user_id': user.id,
                'username': user.username
            })
        except Exception as e:
            return Response({
                'error': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def get_test_token(self, request):
        """Obtenir un token JWT pour l'utilisateur de test existant"""
        try:
            user = User.objects.get(username='test_user')
            refresh = RefreshToken.for_user(user)
            access_token = refresh.access_token
            
            return Response({
                'access_token': str(access_token),
                'refresh_token': str(refresh),
                'user_id': user.id,
                'username': user.username
            })
        except User.DoesNotExist:
            return Response({
                'error': 'Utilisateur de test non trouvé. Utilisez d\'abord /create-test-user/'
            }, status=status.HTTP_404_NOT_FOUND)

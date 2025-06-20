from django.shortcuts import render
from rest_framework import viewsets, permissions, status, filters
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Chambre
from .serializers import ChambreSerializer
from .permissions import IsOwnerViaMaison

class ChambreViewSet(viewsets.ModelViewSet):
    serializer_class = ChambreSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerViaMaison]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['type', 'taille', 'prix', 'titre']
    ordering_fields = ['prix', 'taille', 'cree_le']

    def get_queryset(self):
        user = self.request.user
        if self.action == 'search':
            return Chambre.objects.filter(disponible=True)
        if not user or not hasattr(user, 'id'):
            return Chambre.objects.none()
        if getattr(user, 'is_staff', False):
            return Chambre.objects.all()
        return Chambre.objects.filter(proprietaire_id=user.id)

    def perform_create(self, serializer):
        user = self.request.user
        if not user or not hasattr(user, 'id'):
            raise permissions.PermissionDenied("Authentication credentials were not provided or invalid.")
        serializer.save(proprietaire_id=user.id)

    def get_permissions(self):
        if self.action in ['search', 'list', 'retrieve']:
            return [permissions.AllowAny()]
        return super().get_permissions()

    @action(detail=False, methods=['get'], permission_classes=[permissions.AllowAny])
    def search(self, request):
        queryset = self.get_queryset()
        type_ = request.query_params.get('type')
        if type_:
            queryset = queryset.filter(type=type_)
        prix_min = request.query_params.get('prix_min')
        if prix_min:
            queryset = queryset.filter(prix__gte=prix_min)
        prix_max = request.query_params.get('prix_max')
        if prix_max:
            queryset = queryset.filter(prix__lte=prix_max)
        taille = request.query_params.get('taille')
        if taille:
            queryset = queryset.filter(taille=taille)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

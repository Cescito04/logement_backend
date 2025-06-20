from rest_framework.routers import DefaultRouter
from .views import ChambreViewSet
from django.urls import path, include

router = DefaultRouter()
router.register(r'', ChambreViewSet, basename='chambre')

urlpatterns = [
    path('', include(router.urls)),
] 
from rest_framework.routers import DefaultRouter
from .views import MaisonViewSet
from django.urls import path, include

router = DefaultRouter()
router.register(r'', MaisonViewSet, basename='maison')

urlpatterns = [
    path('', include(router.urls)),
] 
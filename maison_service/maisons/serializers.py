from rest_framework import serializers
from .models import Maison

class MaisonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Maison
        fields = ['id', 'proprietaire_id', 'adresse', 'latitude', 'longitude', 'description', 'cree_le']
        read_only_fields = ['id', 'proprietaire_id', 'cree_le']

    def validate_latitude(self, value):
        if not (-90 <= value <= 90):
            raise serializers.ValidationError("La latitude doit être comprise entre -90 et 90.")
        return value

    def validate_longitude(self, value):
        if not (-180 <= value <= 180):
            raise serializers.ValidationError("La longitude doit être comprise entre -180 et 180.")
        return value 
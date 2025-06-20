from rest_framework import serializers
from .models import Chambre

class ChambreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chambre
        fields = ['id', 'maison_id', 'proprietaire_id', 'titre', 'description', 'taille', 'type', 'meublee', 'salle_de_bain', 'prix', 'disponible', 'cree_le']
        read_only_fields = ['id', 'proprietaire_id', 'cree_le']

    def validate_type(self, value):
        if value not in dict(Chambre.TYPE_CHOICES):
            raise serializers.ValidationError("Type de chambre invalide.")
        return value

    def validate_prix(self, value):
        if value < 0:
            raise serializers.ValidationError("Le prix doit être positif.")
        return value

    def validate_taille(self, value):
        if not value.endswith('m²'):
            raise serializers.ValidationError("La taille doit être au format '12m²'.")
        return value 
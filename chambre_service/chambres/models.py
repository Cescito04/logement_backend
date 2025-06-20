from django.db import models

# Create your models here.

class Chambre(models.Model):
    TYPE_CHOICES = [
        ("simple", "Simple"),
        ("appartement", "Appartement"),
        ("maison", "Maison"),
    ]
    maison_id = models.IntegerField()
    proprietaire_id = models.IntegerField()
    titre = models.CharField(max_length=255)
    description = models.TextField()
    taille = models.CharField(max_length=20)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    meublee = models.BooleanField()
    salle_de_bain = models.BooleanField()
    prix = models.DecimalField(max_digits=10, decimal_places=2)
    disponible = models.BooleanField(default=True)
    cree_le = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Chambre {self.id} - {self.titre}"

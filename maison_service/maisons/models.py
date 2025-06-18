from django.db import models

# Create your models here.

class Maison(models.Model):
    proprietaire_id = models.IntegerField()
    adresse = models.CharField(max_length=255)
    latitude = models.FloatField()
    longitude = models.FloatField()
    description = models.TextField()
    cree_le = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Maison {self.id} - {self.adresse}"

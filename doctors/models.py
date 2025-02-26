from django.db import models
from django.contrib.auth.models import User


class Doctor(models.Model):

    class SpecializationChoices(models.TextChoices):
        
        GENERAL_PRACTICE = "GP", "General Practice"
        CARDIOLOGY = "CA", "Cardiology"
        DERMATOLOGY = "DE", "Dermatology"
        NEUROLOGY = "NE", "Neurology"
        PEDIATRICS = "PE", "Pediatrics"
        ORTHOPEDICS = "OR", "Orthopedics"

    full_name = models.CharField(max_length=100)
    specialization = models.CharField(
        max_length=2,
        choices=SpecializationChoices.choices,
        default=SpecializationChoices.GENERAL_PRACTICE,
    )

    bio = models.TextField()
    photo = models.ImageField(upload_to="images/doctors", default="images/doctors/default.jpg")



    def __str__(self):
        return f"{self.full_name}"
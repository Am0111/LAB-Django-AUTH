from django.db import models
from django.contrib.auth.models import User
from doctors.models import Doctor

class Clinic(models.Model):

    class WorkingHoursChoices(models.TextChoices):
        
        MORNING = "08:00-12:00", "08:00-12:00"
        AFTERNOON = "12:00-16:00", "12:00-16:00"
        EVENING = "16:00-20:00", "16:00-20:00"

    name = models.CharField(max_length=100)
    working_hours = models.CharField(
        max_length=11,
        choices=WorkingHoursChoices.choices,
        default=WorkingHoursChoices.MORNING,
    )

    description = models.TextField()
    photo = models.ImageField(upload_to="images/clinics", default="images/doctors/default.jpg")
    doctors = models.ManyToManyField(Doctor)


    def __str__(self):
        return f"{self.name}"
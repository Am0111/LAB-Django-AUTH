from django.db import models
from django.contrib.auth.models import User
from doctors.models import Doctor
from clinics.models import Clinic

class Reservation(models.Model):

    user = models.ForeignKey(User, on_delete=models.PROTECT, null=True)
    clinic = models.ForeignKey(Clinic, on_delete=models.PROTECT, null=True)
    doctor = models.ForeignKey(Doctor, on_delete=models.PROTECT, null=True)
    date = models.DateField()
    time_slot = models.TimeField()
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"{self.user.first_name}"
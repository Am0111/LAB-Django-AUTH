from django import forms
from .models import Reservation

# Create the form class.
class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = "__all__"

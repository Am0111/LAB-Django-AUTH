from django import forms
from .models import Doctor

# Create the form class.
class DoctorForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = "__all__"
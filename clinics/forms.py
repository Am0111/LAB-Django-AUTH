from django import forms
from .models import Clinic

# Create the form class.
class ClinicForm(forms.ModelForm):
    class Meta:
        model = Clinic
        fields = "__all__"
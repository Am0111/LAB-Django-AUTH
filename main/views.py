from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from doctors.models import Doctor
from clinics.models import Clinic
from django.contrib import messages



def home_view(request:HttpRequest):

    doctors = Doctor.objects.all()[0:3]
    clinics = Clinic.objects.all()[0:3]



    return render(request, 'main/index.html',{"doctors":doctors,'specialization_choices': Doctor.SpecializationChoices.choices, 'clinics':clinics})

def dashboard(request:HttpRequest):

    if not request.user.is_staff:
        messages.success(request, "only staff can add clinic", "warning")
        return redirect("main:home_view")
    else:
        return redirect("doctors:all_doctors")
        # return render(request, 'main/dashboard.html')





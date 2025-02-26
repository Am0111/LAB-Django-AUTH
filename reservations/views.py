from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse, Http404
from django.core.paginator import Paginator
from django.contrib import messages
from .forms import ReservationForm
from doctors.models import Doctor
from clinics.models import Clinic
from django.contrib.auth.models import User
from .models import Reservation


def create_reservation(request:HttpRequest):

    if not request.user.is_authenticated:
        messages.success(request, "only registerd user", "warning")
        return redirect("accounts:signin")


    form = ReservationForm()
    
    doctors = Doctor.objects.all()
    clinics = Clinic.objects.all()

    if request.method == "POST":
        clinic_object = Clinic.objects.get(pk=request.POST['clinic'])
        doctor_object = Doctor.objects.get(pk=request.POST['doctor'])
        reservation = Reservation(user= request.user, clinic=clinic_object , doctor=doctor_object,date=request.POST['date'] ,time_slot=request.POST['time_slot'] )
        reservation.save()
        messages.success(request, "Added reservation Successfuly", "success")
        return redirect('reservations:all_reservations')
        # else:
        #     print("not valid form", form.errors)
        #     messages.error(request, "Couldn't add reservation", "danger")
        #     return redirect('clinics:all_clinics')
            
    return render(request, "reservations/reservation_form.html",{'doctors':doctors,'clinics':clinics})
    
def all_reservations(request:HttpRequest):

    if not request.user.is_authenticated:
        messages.success(request, "only user can view their reservations", "warning")
        return redirect("main:home_view")

    reservation = Reservation.objects.all()

    
    return render(request, "reservations/reservations_list.html",{'reservation':reservation})


def cancel_reservation(request:HttpRequest, reservation_id:int):

    if not request.user.is_authenticated:
        messages.warning(request, "only user can cancel their reservations", "warning")
        return redirect("main:home_view")
    
    try:
        reservation = Reservation.objects.get(pk=reservation_id)
        reservation.delete()
        messages.success(request, "canceld reservation successfully", "success")
        return redirect("reservations:all_reservations")
    except Exception as e:
        print(e)
        messages.error(request, "Couldn't cancel reservation", "danger")


    return redirect("main:home_view")
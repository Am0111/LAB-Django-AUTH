from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse, Http404
from django.core.paginator import Paginator
from django.contrib import messages
from .forms import ClinicForm
from .models import Clinic
from doctors.models import Doctor
from django.db import IntegrityError


def add_clinic(request:HttpRequest):

    if not request.user.is_staff:
        messages.success(request, "only staff can add clinic", "warning")
        return redirect("main:home_view")

    form = ClinicForm()

    if request.method == "POST":
        
        form = ClinicForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Added Clinic Successfuly", "success")
            return redirect('clinics:all_clinics')
        else:
            print("not valid form", form.errors)
            messages.error(request, "Couldn't add Clinic", "danger")
            return redirect('clinics:all_clinics')
            
    return redirect("main:home_view")


    
def all_clinics(request:HttpRequest):

    if not request.user.is_staff:
        messages.success(request, "only staff can add Clinic", "warning")
        return redirect("main:home_view")

    clinics = Clinic.objects.all()
    doctors = Doctor.objects.all()

    if "category" in request.GET and request.GET["category"]:
        clinics = clinics.filter(working_hours=request.GET.get('category'))
    if "q" in request.GET and request.GET["q"]:
        clinics = clinics.filter(name__icontains=request.GET.get('q'))

    page_number = request.GET.get("page",1)
    paginator = Paginator(clinics,1)
    clinics_page = paginator.get_page(page_number)

    
    return render(request, "clinics/clinics_list.html",{'clinics':clinics, 'doctors' :doctors ,'working_hours': Clinic.WorkingHoursChoices.choices})


def delete_clinic(request:HttpRequest,clinic_id):

    if not request.user.is_staff:
        messages.success(request, "only staff can delete Clinic", "danger")
        return redirect("main:home_view")

    try:
        clinic = Clinic.objects.get(pk=clinic_id)
        clinic.delete()
        messages.success(request, "Deleted clinic Successfully", "success")
        return redirect('clinics:all_clinics')

    except IntegrityError as e:
        print(e)
        messages.error(request, "Couldn't Delete clinic that has at least one doctor or one reservation", "danger")
        return redirect('clinics:all_clinics')
    
    except Exception as e:
        print(e)
        messages.error(request, "Unkown error: Couldn't Delete clinic", "danger")
        return redirect('clinics:all_clinics')
    

def update_clinic(request:HttpRequest,clinic_id):

    if not request.user.is_staff:
        messages.success(request, "only staff can delete clinic", "danger")
        return redirect("main:home_view")
    
    if request.method == "POST":

        try:
            clinic = Clinic.objects.get(pk=clinic_id)
            form = ClinicForm(instance=clinic, data=request.POST, files=request.FILES)
            if form.is_valid():
                form.save()
                messages.success(request, "Updated Successfully", "success")
            else:
                print(form.errors)
                messages.error(request, "Couldn't Update clinic ", "danger")
            return redirect('clinics:all_clinics')

        except Exception as e:
            print(e)
            messages.error(request,e, "danger")
            return redirect('clinics:all_clinics')
    return redirect('main:home_view')


def clinic_detail(request,clinic_id):
     clinic = Clinic.objects.get(pk=clinic_id)
     doctors=clinic.doctors.all()
     return render(request, "clinics/clinic_detail.html",{"clinic":clinic , "doctors":doctors})


def clinic_display(request):
     clinic = Clinic.objects.all()
     return render(request, "clinics/all_clinics.html",{"clinics":clinic})


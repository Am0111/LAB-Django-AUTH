from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse, Http404
from django.core.paginator import Paginator
from django.contrib import messages
from .forms import DoctorForm
from .models import Doctor
from django.db import IntegrityError



def add_doctor(request:HttpRequest):

    if not request.user.is_staff:
        messages.success(request, "only staff can add doctor", "warning")
        return redirect("main:home_view")

    form = DoctorForm()

    if request.method == "POST":
        
        form = DoctorForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Added Doctor Successfuly", "success")
            return redirect('doctors:all_doctors')
        else:
            print("not valid form", form.errors)
            messages.error(request, "Couldn't add Doctor", "danger")
            return redirect('doctors:all_doctors')
            
    return redirect("main:home_view")


    
def all_doctors(request:HttpRequest):

    if not request.user.is_staff:
        messages.success(request, "only staff can add doctor", "warning")
        return redirect("main:home_view")

    doctors = Doctor.objects.all()

    if "category" in request.GET and request.GET["category"]:
        doctors = doctors.filter(specialization=request.GET.get('category'))
    if "q" in request.GET and request.GET["q"]:
        doctors = doctors.filter(full_name__icontains=request.GET.get('q'))

    page_number = request.GET.get("page",1)
    paginator = Paginator(doctors,1)
    doctors_page = paginator.get_page(page_number)

    
    return render(request, "doctors/doctors_list.html",{'doctors':doctors,'specialization_choices': Doctor.SpecializationChoices.choices})


def delete_doctor(request:HttpRequest,doctor_id):

    if not request.user.is_staff:
        messages.success(request, "only staff can delete doctor", "danger")
        return redirect("main:home_view")

    try:
        doctor = Doctor.objects.get(pk=doctor_id)
        doctor.delete()
        messages.success(request, "Deleted Doctor Successfully", "success")

    
    except IntegrityError as e:
        print(e)
        messages.error(request, "Couldn't Delete doctor which has at least one reservation", "danger")

    
    except Exception as e:
        print(e)
        messages.error(request, "Couldn't Delete Doctor", "danger")
    return redirect('doctors:all_doctors')


def update_doctor(request:HttpRequest,doctor_id):

    if not request.user.is_staff:
        messages.success(request, "only staff can delete doctor", "danger")
        return redirect("main:home_view")
    
    if request.method == "POST":

        try:
            doctor = Doctor.objects.get(pk=doctor_id)
            form = DoctorForm(instance=doctor, data=request.POST, files=request.FILES)
            if form.is_valid():
                form.save()
                messages.success(request, "Updated Doctor Successfully", "success")
            else:
                print(form.errors)
                messages.error(request, "Couldn't Update Doctor ", "danger")
            return redirect('doctors:all_doctors')

        except Exception as e:
            print(e)
            messages.error(request,e, "danger")
            return redirect('doctors:all_doctors')
    return redirect('main:home_view')


def doctor_detail(request:HttpRequest,doctor_id:int):
    doctor = Doctor.objects.get(pk=doctor_id)
    return render(request, "doctors/doctor_detail.html",{"doctor": doctor})

def doctor_display(request):
     doctors = Doctor.objects.all()
     return render(request, "doctors/all_doctors.html",{"doctors":doctors})


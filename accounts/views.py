from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError, transaction
from django.contrib import messages
from .models import Profile
from django.db.models import Count
from reservations.models import Reservation

def signup(request:HttpRequest):

    if request.method == "POST":

        try:
            with transaction.atomic():
                new_user = User.objects.create_user(username=request.POST["username"],password=request.POST["password"],email=request.POST["email"], first_name=request.POST["first_name"], last_name=request.POST["last_name"])
                new_user.save()

                #create profile for user
                profile = Profile(user=new_user, address=request.POST["address"],phone_number=request.POST["phone_number"])
                profile.save()

            messages.success(request, "Registered User Successfuly", "success")
            return redirect("accounts:signin")
        
        except IntegrityError as e:
            messages.error(request, "Please choose another username", "danger")
            print(e)
        except Exception as e:
            messages.error(request, "Couldn't register user. Try again", "danger")
            print(e)
    

    return render(request, "accounts/signup.html", {})




def signin(request:HttpRequest):

    if request.method == "POST":

        #checking user credentials
        user = authenticate(request, username=request.POST["username"], password=request.POST["password"])
        print(user)
        if user:
            #login the user
            login(request, user)
            messages.success(request, "Logged in successfully", "success")
            return redirect(request.GET.get("next", "/"))
        else:
            messages.error(request, "Please try again. You credentials are wrong", "danger")



    return render(request, "accounts/signin.html")

def user_profile(request:HttpRequest, user_name):

    try:
        user = User.objects.get(username=user_name)
        if not Profile.objects.filter(user=user).first():
            new_profile = Profile(user=user)
            new_profile.save()

    except Exception as e:
        print(e)
        return render(request,'404.html')
    

    return render(request, 'accounts/profile.html', {"user" : user})

def update_profile(request):

    if not request.user.is_authenticated:
        messages.warning(request, "Only registered users can update their profile", "warning")
        return redirect("accounts:sign_in")
    

    if request.method == "POST":

        try:
            with transaction.atomic():
                user:User = request.user

                user.first_name = request.POST["first_name"]
                user.last_name = request.POST["last_name"]
                user.email = request.POST["email"]
                user.save()

                profile:Profile = user.profile
                profile.address = request.POST["address"]
                profile.phone_number = request.POST["phone_number"]
                profile.save()

            messages.success(request, "updated profile successfuly", "success")
        except Exception as e:
            messages.error(request, "Couldn't update profile", "danger")
            print(e)

    return render(request, 'accounts/update_profile.html')


def log_out(request: HttpRequest):

    logout(request)
    messages.success(request, "logged out successfully", "warning")

    return redirect(request.GET.get("next", "/"))


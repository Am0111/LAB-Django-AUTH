from django.urls import path
from . import views

app_name = "doctors"

urlpatterns = [
    path('', views.all_doctors, name="all_doctors"),
    path('add/', views.add_doctor, name="add_doctor"),
    path('delete/<int:doctor_id>', views.delete_doctor, name="delete_doctor"),
    path('update/<int:doctor_id>', views.update_doctor, name="update_doctor"),
    path("detail/<int:doctor_id>/",views.doctor_detail,name="doctor_detail"),
    path("all/",views.doctor_display,name="doctor_display"),


]
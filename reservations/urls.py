from django.urls import path
from . import views

app_name = "reservations"

urlpatterns = [

    path('', views.all_reservations, name="all_reservations"),
    path('create/', views.create_reservation, name="create_reservation"),
    path('cancel/<int:reservation_id>',views.cancel_reservation, name="cancel_reservation"),
]
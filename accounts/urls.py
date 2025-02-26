from django.urls import path
from . import views

app_name = "accounts"

urlpatterns = [
    path('signin/', views.signin, name="signin"),
    path('signup/', views.signup, name="signup"),
    path('logout/', views.log_out, name="log_out"),
    path('<user_name>/', views.user_profile, name="user_profile"),
    path('update/', views.update_profile, name="update_profile"),

]
from django.urls import path
from django.contrib import admin
from .views import HomePage,SignupPatient
from django.contrib.auth import views 
from .reset_password import ResetPatientPassword,resetConfirm
urlpatterns = [
    path('',HomePage.as_view(),name='home'),
    path('healthpanel/', admin.site.urls),
    path('create-account/',SignupPatient.as_view(),name='signup'),
    path('reset-account/',ResetPatientPassword.as_view(),name='reset'),
    path('sign-in',views.LoginView.as_view(template_name='login.html'),name='signin'),
    path('signout',views.LogoutView.as_view(next_page='home'),name='signout'),
    path('reset-password/',resetConfirm)
]

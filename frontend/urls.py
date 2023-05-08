from django.urls import path
from django.contrib import admin
from .views import HomePage
urlpatterns = [
    path('',HomePage.as_view(),name='home'),
    path('healthpanel/', admin.site.urls),
]

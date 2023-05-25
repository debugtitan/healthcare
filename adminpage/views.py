from django.shortcuts import render
from django.views.generic import ListView
from django.contrib.auth.models import User

class UsersList(ListView):
    model = User
    template_name = 'customs/view_users.html'
    
    
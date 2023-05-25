from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User

class CustomForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'first_name', 'last_name']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form_all_inputs'}),
            'email': forms.EmailInput(attrs={'class': 'form_all_inputs'}),
            'first_name': forms.TextInput(attrs={'class': 'form_all_inputs'}),
            'last_name': forms.TextInput(attrs={'class': 'form_all_inputs'}),
        }



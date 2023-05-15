
from django.db import models
from django.contrib.auth.models import User
from django.forms import CharField

class ResetPassword(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reset_token = models.CharField(max_length=80,null=True,blank=True)
    token_expire_time = models.DateTimeField(auto_now_add=False,null=True)
 

class Subscribers(models.Model):
    email = models.CharField(max_length=50,null=True,unique=True)
    
    def __str__(self) -> str:
        return self.email
    

class Appointments(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    fullName= models.CharField(max_length=60)
    email = models.CharField(max_length=50)
    contact = models.CharField(max_length=14)
    time = models.DateTimeField()
    reason = models.CharField(max_length=10000)
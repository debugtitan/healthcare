from django.db import models
from django.contrib.auth.models import User
class ResetPassword(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reset_token = models.CharField(max_length=80,null=True,blank=True)
    token_expire_time = models.DateTimeField(auto_now_add=False,null=True)
 
from django.db import models
from django.contrib.auth.models import User
from django.forms import BooleanField


class BanPatient(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name="is_banned")
    is_banned = models.BooleanField(default=False)
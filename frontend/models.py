
from django.db import models
from django.contrib.auth.models import User

class ResetPassword(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='resekey')
    reset_token = models.CharField(max_length=80,null=True,blank=True)
    token_expire_time = models.DateTimeField(auto_now_add=False,null=True)
 

class Subscriber(models.Model):
    email = models.CharField(max_length=50,null=True,unique=True)
    
    def __str__(self) -> str:
        return self.email
    

class DoctorDepartment(models.Model):
    title = models.CharField(max_length=50,unique=True)
    desc  = models.CharField(max_length=300,default='short info for this department')
    icon_name = models.CharField(max_length=50,default='ri-more-line',help_text='get icon name from https://remixicon.com/icon/')
    
    
    def __str__(self) -> str:
        return self.title

class StaffDepartment(models.Model):
    title = models.CharField(max_length=50,unique=True)

    def __str__(self) -> str:
        return self.title


class Doctor(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    doctor_full_name = models.CharField(max_length=50)
    doctor_email = models.EmailField(max_length=90,unique=True)
    doctor_department = models.ForeignKey(DoctorDepartment,on_delete=models.CASCADE,related_name='departments')

    def __str__(self) -> str:
        return self.doctor_full_name
    
class HealthStaff(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='healthstaffs')
    staff_department = models.ForeignKey(StaffDepartment,on_delete=models.CASCADE,related_name='staffdepartment')

    def __str__(self) -> str:
        return self.user,self.staff_department
    

class HealthVacancies(models.Model):
    title = models.CharField(max_length=50)
    job_requirements = models.CharField(max_length=300)
    job_description = models.TextField()

    def __str__(self) -> str:
        return self.title

class Appointment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    patient_name = models.CharField(max_length=70)
    appointment_department = models.ForeignKey(DoctorDepartment,on_delete=models.CASCADE)
    doctor_patient_preferred =  models.ForeignKey(Doctor,on_delete=models.CASCADE)
    patient_email  = models.EmailField(max_length=50)
    patient_contact  = models.CharField(max_length=15)
    patient_message = models.TextField()

    def __str__(self) -> str:
        return f"{self.user} Appointment"


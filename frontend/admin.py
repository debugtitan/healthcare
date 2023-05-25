from django.contrib import admin
from .models import *

admin.site.register(Doctor)
admin.site.register(DoctorDepartment)
admin.site.register(StaffDepartment)
admin.site.register(HealthStaff)
admin.site.register(Appointment)
admin.site.register(Subscriber)
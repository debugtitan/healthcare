from django.contrib.auth.models import User
from django.views.generic import CreateView,ListView
from django.urls import reverse_lazy
from .models import *
from .forms import *
from django.contrib.auth.mixins import LoginRequiredMixin


#logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')\

class HomePage(CreateView):
    template_name = 'home/home.html'
    model= Subscriber
    fields  =  ['email']
    success_url = reverse_lazy('home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['departments'] = DoctorDepartment.objects.all()
        return context
    
    def form_valid(self, form):
        email = form.cleaned_data['email']
        if Subscriber.objects.filter(email=email).exists():
            return self.form_invalid(form)
        return super().form_valid(form) 
    

class SignupPatient(CreateView):
    template_name = "forms/signup.html"
    model = User
    success_url = reverse_lazy('signin')
    form_class = CustomForm

    

class ReceiveSendAppointment(LoginRequiredMixin,CreateView):
    template_name = "appointments/appointments.html"
    model = Appointment
    success_url = reverse_lazy('home')
    fields =  ['patient_name','appointment_department',"doctor_patient_preferred",'patient_email',"patient_contact",'patient_message']

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['patient_name'].widget.attrs['class'] = 'form-control'
        form.fields['patient_email'].widget.attrs['class'] = 'form-control'
        form.fields['patient_message'].widget.attrs['class'] = 'form-control'
        form.fields['patient_contact'].widget.attrs['class'] = 'form-control'
        return form
    
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        print(form.cleaned_data)
        return super().form_valid(form)



class AboutPage(ListView):
    template_name = 'home/about.html'
    model = DoctorDepartment
    context_object_name = 'departments'
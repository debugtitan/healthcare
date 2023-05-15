
from django.contrib.auth.models import User
from django.shortcuts import render
from django.views.generic import TemplateView
from .forms import SignUp
from django.shortcuts import HttpResponseRedirect,HttpResponse
from django.urls import reverse_lazy
from django.http  import HttpResponse
from .models import Appointments
import json,logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
from .models import Subscribers
class HomePage(TemplateView):
    template_name = 'home.html'

    def post(self,request):
        try:
           email = json.loads(request.body)['email']
           user = Subscribers()
           logging.info(f"Üser: {email}")
           user.email= email
           user.user = User.objects.get(email=email)
           user.save()
           return HttpResponse(status=201)
        except Exception as error:
            logging.warning(f"Subscriber not registered {error}")
            return HttpResponse()

    

    


class SignupPatient(TemplateView):
    template_name = "signup.html"


    def post(self,request):
        inData = request.POST
        allData = SignUp(username=inData['username'],email=inData['email'],password=inData['psw'],firstname=inData['firstname'],lastname=inData['lastname'])
        if allData.valid()['valid']:
            allData.save()
            return HttpResponseRedirect(reverse_lazy('signin'))
            
        else:
            data = {
                "username_err": allData.valid()['username_err'],
                "email_err": allData.valid()['email_error']
            }

            return render(request,self.template_name,data)


class ReceiveSendAppointment(TemplateView):
    template_name = "appointments.html"

    def post(self,request):
        try:
            inData= json.loads(request.body)
            print(inData)
            user_appointments = Appointments(
                user = request.user,
                email = inData['email'],
                fullName = inData['name'],
                contact = inData['contact'],
                time = inData['time'],
                reason =inData['reason']
            )

            user_appointments.save()
        except Exception as error:
            logging.warning(f"Send appointments: {error}")
        return HttpResponse()

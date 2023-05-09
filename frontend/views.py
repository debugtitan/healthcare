from django.shortcuts import render
from django.views.generic import TemplateView
from .forms import SignUp
from django.shortcuts import HttpResponseRedirect
from django.urls import reverse_lazy

class HomePage(TemplateView):
    template_name = 'index.html'

    def get(self,request):
        context = {
            "loggedin" : request.user.is_authenticated,
            "admin": request.user.is_staff
        }
        return render (request,self.template_name,context)
    

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

        
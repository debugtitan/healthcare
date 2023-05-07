from django.shortcuts import render
from django.views.generic import TemplateView


class HomePage(TemplateView):
    template_name = 'index.html'

    def get(self,request):
        context = {
            "loggedin" : request.user.is_authenticated,
            "admin": request.user.is_staff
        }

        print(context)

        return render (request,self.template_name,context)
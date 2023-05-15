from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes,force_str
from django.template.loader import render_to_string
from django.views.generic import TemplateView
import logging
from .models import ResetPassword

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

class ProcessPasswordReset():

    def __init__(self,token,user_id):
        self.token = token
        self.user_id = user_id
        self.user = self.get_member_username()
       

    def get_member_username(self):
        uid = force_str(urlsafe_base64_decode(self.user_id))
        
        try:
            #User.objects.values().get(id=uid)
            return User.objects.get(id=uid)
        except Exception:
            return None

    def check_token_valid(self):
        if self.user is not  None:
            try:
                query_user_token = ResetPassword.objects.get(user=self.user)
                logging.info("hi", query_user_token.token_expire_time)
                if PasswordResetTokenGenerator().check_token(self.user, self.token) and query_user_token.token_expire_time> timezone.now():
                    #logging.info(f'{self.token} for {self.get_member_username()} is valid')
                    return True
            except Exception as err:
                #logging.info(f'{self.token} for {self.get_member_username()} is not  valid or expired\nerr: {err}')
                return False 

    def update_member_password(self,newPassword: str):
        try:
            if self.user is not None:
                self.user.set_password(newPassword)
                updates = ResetPassword.objects.get(user=self.user)
                updates.reset_token = None
                updates.token_expire_time = None
                updates.save()
                return True
        except Exception as e:
            #logging.WARNING(f'function update_member_password : {e}')
            return False



class ResetPatientPassword(TemplateView):
    template_name = 'reset.html'

    def post(self,request):
        try:
            user_id = User.objects.get(email=request.POST['email'])
            user = ResetPassword()
            token = PasswordResetTokenGenerator().make_token(user_id) #generating a random token for unique user
            uid = urlsafe_base64_encode(force_bytes(user_id.pk)), 
            #print(token,uid)
            user.user = user_id
            user.reset_token = token
            user.token_expire_time = timezone.now() + timezone.timedelta(hours=1) #setting up the token expiry time to one hour
            user.save()
            reset_link = request.build_absolute_uri('/reset-password/') + '?user=' + uid[0] + '&token=' + token
            subject = 'Password Reset Request'
            message = render_to_string('emails/reset_password.html', {
                'reset_link': reset_link
            })
            html_message = render_to_string('emails/reset_password.html', {
                'reset_link': reset_link
            })
            from_email, recipient_list = 'support@healthcare.com', [request.POST['email']]
            
            send_mail(subject, message, from_email, recipient_list, html_message=html_message)
            return render(request,self.template_name,{"msg":'We\'ve sent you an email with instructions on how to reset your password.'})
            
        except Exception as err:
            print(err)
            return render(request,self.template_name)



def resetConfirm(request):
    user_id = request.GET['user']
    token = request.GET['token']
    if ProcessPasswordReset(token=token,user_id=user_id).check_token_valid():
        if request.POST:
            
            password = request.POST['password']
            #print(password)
            if ProcessPasswordReset(token=token,user_id=user_id).update_member_password(newPassword=str(password)):
                return redirect('signin')
            else:
                return render(request, '404.html')
        else:
            return render(request, 'reset_confirm.html')

    #SINCE WE CAN'T VERIFY THEIR ID AND TOKEN RATHER SEND 404 ERROR
    else:
        return render(request, '404.html')




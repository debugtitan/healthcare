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


class ProcessPasswordReset():

    def __init__(self,token,user_id):
        self.token = token
        self.user_id = user_id
        self.user = self.get_member_username()

    def get_member_username(self):
        uid = force_str(urlsafe_base64_decode(self.user_id))
        logging.INFO(uid)
        try:
            return User.objects.get(id=uid)
        except Exception:
            return None

    def check_token_valid(self):
        if self.user is not None:
            try:
                if PasswordResetTokenGenerator().check_token(self.user, self.token) and self.user.password_reset_expiration > timezone.now():
                    return True
            except Exception:
                return False

    def update_member_password(self,newPassword: str):
        try:
            if self.user is not None:
                self.user.set_password(newPassword)
                self.user.password_reset_token = None
                self.user.password_reset_expiration = None
                self.user.save()
                return True
        except Exception as e:
            logging.WARNING(f'function update_member_password : {e}')
            return False



class ResetPatientPassword(TemplateView):
    template_name = 'reset.html'

    def post(self,request):
        try:
            user = User.objects.get(email=request.POST['email'])
            token = PasswordResetTokenGenerator().make_token(user) #generating a random token for unique user
            uid = urlsafe_base64_encode(force_bytes(user.pk)),
            print(token,uid)
            
            user.password_reset_token = token
            user.password_reset_expiration = timezone.now() + timezone.timedelta(hours=1) #setting up the token expiry time to one hour
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






"""
def reset_confirm(request):
    user_id = request.GET.get('user')
    token = request.GET.get('token')
    if verify(token=token,user_id=user_id).check_token_valid:
        print('true')
        if request.method == 'POST':
            password = request.POST.get('password')
            print(password)
            if verify(token=token,user_id=user_id).update_member_password(newPassword=str(password)):
                return redirect('login')
            else:
                return render(request, 'forms/reset_confirm.html')
        else:
            return render(request, 'forms/reset_confirm.html')

    #TAKE THE USER BACK TO LOGIN SINCE WE CAN'T VERIFY THEIR ID AND TOKEN RATHER SEND 404 ERROR
    else:
        return render(request, '404.html')
"""
    
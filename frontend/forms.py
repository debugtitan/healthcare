
from django.contrib.auth.models import User

class SignUp:
    
    def __init__(self,username,email,password,firstname,lastname) -> None:
        self.username = username
        self.email = email
        self.password = password
        self.firstname,self.lastname = firstname,lastname
        
    def clean_username(self):
        username = self.username
        if User.objects.filter(username=username).exists():
            return False
        else:
            return True

    def clean_email(self):
        email = self.email
        if User.objects.filter(email=email).exists():
            return False
        else:
            return True

    def valid(self):
        data = {
            "valid": False,
            "username_err" : "",
            "email_error": ""  
        }
        if self.clean_email() and self.clean_username():
            data['valid']= True

        if not self.clean_email():
            data["email_error"] = "This email is already taken."

        if not self.clean_username():
            data["username_err"] = "This username is already taken."

        print(data)

        return data

    def save(self):
        User.objects.create_user(username=self.username, email = self.email, password = self.password,last_name=self.lastname,first_name=self.firstname)
            
    






    







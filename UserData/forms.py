from django import forms
from .models import UserProfile
from django.contrib.auth.models import User


class RegistrationForms(forms.ModelForm):

    class Meta:

        model =User

        fields =["username","first_name",'last_name','email','password']




class LoginForm(forms.Form):

    username =forms.CharField(max_length=50)

    password=forms.CharField(max_length=50)





class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['profile_picture', 'phone', 'address', 'city', 'state', 'country', 'pincode',]
        



class ForgotForm(forms.Form):

    username =forms.CharField(max_length=50)



class Otp_VerifyForm(forms.Form):

    otp =forms.CharField(max_length=4)    


class Restform(forms.Form):

    newpassword=forms.CharField(max_length=10)

    conformpassword=forms.CharField(max_length=10)
    
      










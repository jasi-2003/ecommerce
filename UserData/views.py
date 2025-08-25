from django.shortcuts import render ,redirect
from django.contrib.auth.models import User 
from django.views.generic import View
from django.contrib.auth import authenticate ,login ,logout
from django.views.generic import View ,CreateView  ,DeleteView ,DetailView ,UpdateView ,ListView
from product.models import Cart,Ordermodel,CategoryModel,ProductModel
from django.urls import reverse_lazy
from UserData.forms import RegistrationForms ,LoginForm ,ProfileUpdateForm,ForgotForm,Otp_VerifyForm,Restform
from django.core.mail import send_mail
import random




from .forms import ProfileUpdateForm
from .models import UserProfile

# Create your views here.

from django.contrib.auth.decorators import login_required

@login_required
def profile_view(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    return render(request, "profile.html", {"profile": profile})


class Homepage(View):

    def get(self,request):
         
        data1=ProductModel

        data = CategoryModel.objects.all()

        return render(request,"Homepage.html",{"data":data})


class Registration(View):

    def get (self,request):

        form = RegistrationForms
        
        return render(request,"Registration.html",{'form':form})
    

    def post (self,request):

        form = RegistrationForms(request.POST)

        if form.is_valid():

           user = User.objects.create_user(**form.cleaned_data)    

           Cart.objects.create(user = user) #model cart user = user

           Ordermodel.objects.create(user=user) #order

           


           subject ="Welcome to Auramart! 🌟"

           message ="Your one-stop destination for quality products at unbeatable prices! 🛍️✨ \
             Enjoy a seamless shopping experience with exclusive deals, fast delivery, and top-notch customer service.\
                 Start exploring now and find everything you need in just a few clicks! \
                 \
                 Happy Shopping! 🛒💖"

           from_email ='akhilkarunan0@gmail.com'

           recipient_list =[form.cleaned_data.get('email')]

           send_mail(subject,message,from_email,recipient_list,fail_silently=False)

           form = RegistrationForms


            # return render(request,"Registration.html",{'form':form})
        return redirect("login")




class Login(View):

    def get (self,request):

        form = LoginForm

        return render(request,"Login.html",{'form':form})
    

    def post (self,request):

        form =LoginForm(request.POST)

        if form.is_valid():

            uname = form.cleaned_data.get('username')

            pword=form.cleaned_data.get('password')

            user=authenticate(request,username=uname,password=pword)

            if user:

                login(request,user)

                print(request.user)

                return redirect ("product_list")
            
            else:
                return redirect('registration')




class LogoutView(View):

    def get(self,request):

        logout(request)

        return redirect("login")    



#profile info   , update ,

def profile_view(request):
    
    # Get or create the profile for the logged-in user
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    if request.method == "POST":
        form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')  # Redirect after updating profile

    else:
        form = ProfileUpdateForm(instance=profile)

    return render(request, 'profile.html', {'form': form, 'profile': profile})


class ProfileUpdate(UpdateView):

    model=UserProfile

    template_name ="profileupdate.html"

    fields =['profile_picture', 'phone', 'address', 'city', 'state', 'country', 'pincode',]

    success_url = reverse_lazy("login")



class ProfileDetailView(DetailView):

    model = UserProfile

    template_name ="profiledetails.html"

    context_object_name="data"

    success_url = reverse_lazy("login")  



#Forgot Password

class ForgotpasswordView(View):

    def get (self,request):

        form =ForgotForm

        return render (request,"forgot.html",{"form":form})
    
    def post(self,request):

        username= request.POST.get("username")    

        user = User.objects.get(username=username)

        if user:

            otp =random.randint(1000,9999)

            request.session["username"] =username

            request.session["otp"] =otp

            send_mail(subject="Reset Your Password - OTP Verification" ,message=str(otp) ,from_email='akhilkarunan0@gmail.com',recipient_list=[user.email])

            return redirect("otpverify")

    
class Otp_verify(View):

    def get(self,request):

        form =Otp_VerifyForm

        return render (request,"Otp_verify.html",{'form':form})
    
    def post(self,request):

        new_otp = request.POST.get("otp")

        old_otp =request.session.get("otp")

        if str(new_otp)==str(old_otp):

            print("match")

        return redirect("restpassword")    
    

class ConformPassword(View):

    def get(self,request):

        form = Restform

        return render(request,"conformpass.html",{"form":form})

    def post(self,request):

        o_password =request.POST.get("newpassword")

        c_password= request.POST.get("conformpassword")

        if o_password == c_password :

            u_name =request.session.get("username")

            user =User.objects.get(username=u_name)

            user.set_password(c_password)

            user.save()

            return redirect("login")





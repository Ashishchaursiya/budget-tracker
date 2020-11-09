from django.shortcuts import render,redirect
from django.views import View
import json
from django.http import JsonResponse
from validate_email import validate_email
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.mail import EmailMessage
from django.utils.encoding import force_bytes,force_text,DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from .utils import token_generator
from django.contrib import auth
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.auth.models import User
import threading
# Create your views here.


#send fast email
class EmailThread(threading.Thread):
    def __init__(self,email):
        self.email=email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send(fail_silently=False)    
#username validation
class usernameValidation(View):
    def post(self,request):
        data=json.loads(request.body)
        username=data['username']
        
        if not username.isalnum():
            return JsonResponse({"username_error":"username should contain only alfanumeric character"})
        if User.objects.filter(username=username).exists():
            return JsonResponse({"username_error":"username already taken"})
        return JsonResponse({"user_valid":True})

#email validation
class emailValidation(View):
    def post(self,request):
        data=json.loads(request.body)
        email=data['email']
        
        if not validate_email(email):
            return JsonResponse({"email_error":"email is wrong"})
        if User.objects.filter(email=email).exists():
            return JsonResponse({"email_error":"email already taken"})    
        return JsonResponse({"email_valid":True})

#password validation
class passwordValidation(View):
    def post(self,request):
        data=json.loads(request.body)
        password=data['password']
        
        if len(password)<6:
            return JsonResponse({"password_error":"password too short"})
        if  password.isalnum():
            return JsonResponse({"password_error":"password should contain special(@,$,#) character"})
        return JsonResponse({"password_valid":True})

#send regiter form
class Register(View):
    def get(self,request):
        return render(request,'authentication/register.html')
    def post(self,request):
        username=request.POST['username']
        email=request.POST['email']
        password=request.POST['password']
        if not User.objects.filter(username=username) and not User.objects.filter(email=email):
            user=User.objects.create_user(username=username,email=email,password=password)
            user.is_active=False
            user.save()
            #code for activate account
            uidb64= urlsafe_base64_encode(force_bytes(user.pk))
            domain = get_current_site(request).domain
            link= reverse('activate-account',kwargs={
                'uidb64':uidb64,'token':token_generator.make_token(user)
            })
            activate_url = 'http://'+domain+link
            email_body= 'hi '+user.username + ' please use this link to verify your account\n'+activate_url
            email_subject= "Activate your account"
            email_obj = EmailMessage(
            email_subject,
            email_body,
            'noreply@example.com',
            [email],
            
     
              )
             
            EmailThread(email).start()
            messages.success(request,"Account successful created, check your email")
            return render(request,'authentication/register.html')

        return render(request,'authentication/register.html')    
#email verification view
class verificationView(View):
    def get(self,request,uidb64,token):
    
        id=force_text(urlsafe_base64_decode(uidb64))
        user=User.objects.get(pk=id)

        

        if user.is_active:
            return redirect('login')
        user.is_active=True
        user.save()
        messages.success(request,'Account activated successfully')
        return redirect('login')
       

class LoginView(View):
    def get(self,request):
        return render(request,'authentication/login.html')  

    def post(self,request):
        username=request.POST['username'] 
        password=request.POST['password'] 
        user = auth.authenticate(username=username,password=password)
        if user:
            if user.is_active:
                auth.login(request,user)
                messages.success(request,'Welcome '+user.username+' You are now logged in')
                return redirect('/')
            messages.error(request,'Account is not active,Check your email') 
            return render(request,'authentication/login.html')
        messages.error(request,'Invalid Credential,Try again') 
        return render(request,'authentication/login.html')    

#logout View
class logoutView(View):
    def post(self,request):
        auth.logout(request)
        messages.success(request,'You have been logeed out')
        return redirect('login')
                       
#reset Password View
class ResetPasswordView(View):
    def get(self,request):
            return render(request,'authentication/reset_password.html')
    def post(self,request):
        email=request.POST['email']
        context={'values':request.POST}
        if not validate_email(email):
            messages.error(request,'Please enter valid email')
            return render(request,'authentication/reset_password.html',context)
        current_site=  get_current_site(request) 
         
        #user=request.objects.filter(email=email)
        try:
            user=User.objects.get(email=email)
            if user:
                uidb64= urlsafe_base64_encode(force_bytes(user.pk))
        
                email_content={
                'user':user,
                'domain':current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':token_generator.make_token(user)
                    }
                link= reverse('reset-user-password',kwargs={
                'uidb64':uidb64,'token':PasswordResetTokenGenerator().make_token(user)
                      })
                reset_url = 'http://'+current_site.domain+link
                email_body= 'hi there, please use this link to reset password \n'+reset_url
                email_subject= "Password reset Instructions"
                email_obj = EmailMessage(
                email_subject,
                email_body,
                'noreply@example.com',
                [email],
            
     
              )
                EmailThread(email).start() 
                messages.success(request,'We have sent to  you  email to reset password')
                return render(request,'authentication/reset_password.html') 
        except:
            messages.error(request,'Email is not exist in Database')
            return render(request,'authentication/reset_password.html') 

            

            
      
          
#complete password
class CompletePassword(View):
    def get(self,request,uidb64,token):
        context={
            'uidb64':uidb64,
            'token':token
        }
        return render(request,'authentication/set-newpassword.html',context)

    def post(self,request,uidb64,token):
        context={
            'uidb64':uidb64,
            'token':token
        }
        password1=request.POST['password1']
        password2=request.POST['password2']
        if password1 != password2:
            messages.error(request,'Password do not match')
            return render(request,'authentication/set-newpassword.html',context) 
        try:
            user_id=force_text(urlsafe_base64_decode(uidb64)) 
            user=User.objects.get(pk=user_id) 
            user.set_password(password1 ) 
            user.save()
            messages.success(request,'Password   reset successfully')
            return redirect('login') 
        except:
            messages.info(request,'something went wrong')
            return render(request,'authentication/set-newpassword.html',context) 

                  
         
        

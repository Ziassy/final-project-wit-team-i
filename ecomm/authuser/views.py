from django.shortcuts import render

# Create your views here.
from django.shortcuts import render,redirect, HttpResponse
from django.contrib.auth.models import User
from django.views.generic import View
from django.contrib import messages
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from .utils import TokenGenerator,generate_token
from django.utils.encoding import force_bytes,force_str,DjangoUnicodeDecodeError
from django.core.mail import EmailMessage
from django.conf import settings

# Create your views here.
def signin(request):
    return render(request, 'authentication/signin.html')

def signup(request):
    if request.method=="POST":
        userName=request.POST['userName']
        email=request.POST['email']
        password=request.POST['pass1']
        confirm_password=request.POST['pass2']
        if password!=confirm_password:
            messages.warning(request,"Password is Not Matching")
            return render(request,'signup.html')                   
        try:
            if User.objects.get(username=email):
                # return HttpResponse("email already exist")
                messages.info(request,"Email is Taken")
                return render(request,'signup.html')
        except Exception as identifier:
            pass
        user = User.objects.create_user(userName,email,password)
        user.is_active=True #yang baru signi[, isactive = false
        user.save()
        # email_subject="Activate Your Account"
        # message=render_to_string('activate.html',{
        #     'user':user,
        #     'domain':'127.0.0.1:8000',
        #     'uid':urlsafe_base64_encode(force_bytes(user.pk)), #urlsafe_base64_encode generate token
        #     'token':generate_token.make_token(user)

        # })
        #https://www.youtube.com/watch?v=7VEveJz7hdM 4:01:42
        # email_message = EmailMessage(email_subject,message,settings.EMAIL_HOST_USER,[email])
        # email_message.send()
        # messages.success(request,f"Activate Your Account by clicking the link in your email {message}")
        return redirect('/auth/login/')
    return render(request,"account/signup.html")

# class ActivateAccountView(View):
#     def get(self,request,uidb64,token):
#         try:
#             uid=force_str(urlsafe_base64_decode(uidb64))
#             user=User.objects.get(pk=uid)
#         except Exception as identifier:
#             user=None
#         if user is not None and generate_token.check_token(user,token):
#             user.is_active=True
#             user.save()
#             message.info(request,"Account Activated Successfully")
#             return redirect('/auth/login/')
#         return render(request,'activatefail.html') #jika gagal redirect ke activate fail

def logout(request):
    return redirect('/auth/signin')
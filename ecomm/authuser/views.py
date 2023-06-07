# Create your views here.
from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth.models import User
from django.views.generic import View
from django.contrib import messages
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from .utils import TokenGenerator,generate_token
from django.utils.encoding import force_bytes,force_str,DjangoUnicodeDecodeError
from django.core.mail import EmailMessage
from django.conf import settings

from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.auth import authenticate,login,logout
from django.views.decorators.csrf import csrf_protect
from django.http import HttpResponseRedirect

# Create your views here.
def signup(request):
    if request.method=="POST": 
        username=request.POST['username']
        email=request.POST['email']
        password=request.POST['pass1']
        confirm_password=request.POST['pass2']
        if password!=confirm_password:
            messages.warning(request,"Passwords do not match. Please try again.")
            return render(request,'account/signup.html')                   
        try:
            if User.objects.get(email=email) and User.objects.get(username=username):
                # return HttpResponse("email already exist")
                messages.info(request,"Email or Username already exists. Please choose a different email or username")
                return render(request,'account/signup.html')
        except Exception as identifier:
            pass
        user = User.objects.create_user(username,email,password)
        user.is_active=True #yang baru signi[, isactive = false
        user.save()
        # email_subject="Activate Your Account"
        # message=render_to_string('account/activate.html',{
        #      'user':user,
        #      'domain':'127.0.0.1:8000',
        #      'uid':urlsafe_base64_encode(force_bytes(user.pk)), #urlsafe_base64_encode generate token
        #      'token':generate_token.make_token(user)

        #  })
        # user = user
        # domain = '127.0.0.1:8000'
        # uid = urlsafe_base64_encode(force_bytes(user.pk))
        # token = generate_token.make_token(user)
        #https://www.youtube.com/watch?v=7VEveJz7hdM 4:01:42
        # email_message = EmailMessage(email_subject,message,settings.EMAIL_HOST_USER,[email])
        # email_message.send()
        # messages.success(request,f"Activate Your Account by clicking this link http://{domain}/'activate'/{uid}/{token}")
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
#             messages.info(request,"Account Activated Successfully")
#             return redirect('/auth/login')
#         return render(request,'account/activatefail.html') #jika gagal redirect ke activate fail

@csrf_protect
def handlelogin(request):
    if request.method=="POST":

        username=request.POST['username']
        password=request.POST['password']
        myuser = authenticate(request, username=username, password=password)

        if myuser is not None and myuser.is_active:
            login(request,myuser)
            return redirect('/')

        else:
            messages.error(request,"Invalid Credentials")
            return redirect('/auth/login')

    return render(request,'account/login.html')   

@csrf_protect #Prevention CSRF (Cross-Site Request Forgery)
def handle_logout(request):
    logout(request)
    # Untuk redirect ke page home ( / ) setelah logout
    return redirect('/')
from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import messages
from .models import *
import uuid
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth import authenticate,login,logout
# Create your views here.
def home(request):
    return render(request,'home.html')
def login_attempt(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user_obj = User.objects.filter(username = username).first()
        if user_obj is None:
            messages.success(request,'Username  not found.')
            return redirect('/login')
        profile_obj = Profile.objects.filter(user = user_obj).first()
        if not profile_obj.is_verified:
            messages.success(request,'Please first verify your by clicking on link sent to you on Your gmail.')
            return redirect('/login')
        userr = authenticate(username=username, password=password)
        if userr is None:
            messages.success(request,'Please Enter your username and password correctly.')
            return redirect('/login')
        login(request,userr)
        return redirect('/success')
    return render(request,'login.html')
def logout_attempt(request):
    logout(request)
    messages.success(request, "Successfully logged out")
    return redirect('/')
def register_attempt(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            if User.objects.filter(username=username).first():
                messages.success(request,'Username  is taken.')
                return redirect('/register')
            if User.objects.filter(email = email).first():
                messages.success(request,'Email  is taken.')
                return redirect('/register')
            user_obj = User.objects.create(username=username,email=email)
            user_obj.set_password(password)
            user_obj.save()
            auth_token = str(uuid.uuid4())
            profile_obj = Profile.objects.create(user = user_obj, auth_token = auth_token)
            profile_obj.save()
            send_mail_after_registration(email,auth_token)
            return redirect('/token')
        except Exception  as e:
            print(e)      
    return render(request,'register.html')

def verify(request, auth_token):
    try:
        profile_obj = Profile.objects.filter(auth_token=auth_token).first()
        print(profile_obj)
        if profile_obj:
            profile_obj.is_verified = True
            profile_obj.save()
            messages.success(request,'Your Email  is Verified.')
            return redirect('/login')
        else:
            return redirect('/error')
    except Exception as e:
        print(e)
def error_page(request):
    return render(request, 'error.html')
def success(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

    return render(request,'success.html')
def token_send(request):
    return render(request,'token_send.html')

def send_mail_after_registration(email,token):
    subject = 'your account  need to be verified'
    message = f'Hi click the link to verify your account http://127.0.0.1:8000/verify/{token}'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, email_from, recipient_list)

def forget_password(request):
    try:
        if request.method == 'POST':
            username = request.POST.get('username')
            user_obj = User.objects.filter(username = username).first()
            if user_obj is None:
                messages.success(request,'Username  not found.')
                return redirect('/forget_password')
            token = str(uuid.uuid4())
            profile_obj = Profile.objects.filter(user=user_obj).first()
            profile_obj.auth_token = token
            profile_obj.save()
            email = user_obj.email
            send_email(email, token)
            messages.success(request,'Check your Email.')
            return redirect('/forget_password/')
    except Exception as e:
        print(e)
    return render(request,"forget_password.html")
        

def change_password(request,token):
    # profile_obj = Profile.objects.get(auth_token = token)
    try:
        profile_obj = Profile.objects.filter(auth_token = token)[0]
        context = {"user_id": profile_obj.user.id}
        if request.method == 'POST':
            password = request.POST.get('password')
            confirmpassword = request.POST.get('confirmpassword')
            user_id = request.POST.get('user_id')
            if password != confirmpassword:
                messages.success(request,'passwords do not match.')
                return redirect("/change_password/{{token}}")
            if user_id is None:
                return redirect('/change_password/{{token}}')
            user_obj = User.objects.get(id = user_id)
            user_obj.set_password(password)
            user_obj.save()
            messages.success(request,'your password is changed.')
            return redirect("/login")
    except Exception as e:
        print(e)
    return render(request,"change_password.html",context)

def send_email(email,token):
    subject = 'Link to reset your password'
    message = f'Hi, click on the link to reset password http://127.0.0.1:8000/change_password/{token}'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, email_from, recipient_list)
    return True
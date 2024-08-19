from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import random
import datetime
from django.utils import timezone
from django.core.mail import send_mail 
from django.utils.crypto import get_random_string
from django.conf import settings

# file imports 
from orders.models import Order
from .models import CustomUser, BuyerProfile
from .models import BuyerProfile, ShippingAddress
from .forms import  BuyerProfileForm, OTPForm, EmailLoginForm


# --------------------------------------------------- buyer ----------------------------------------------------------

# ثبت نام خریدار
def buyer_signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        date_of_birth = request.POST.get('date_of_birth')

        if not username or not password1 or not password2 or not email:
            return render(request, 'accounts/buyer_signup.html', {'error': 'تمامی فیلدها الزامی هستند.'})

        if password1 != password2:
            return render(request, 'accounts/buyer_signup.html', {'error': 'رمز عبورها مطابقت ندارند.'})

        try:
            if CustomUser.objects.filter(username=username).exists():
                return render(request, 'accounts/buyer_signup.html', {'error': 'این نام کاربری قبلا ثبت شده است.'})

            user = CustomUser.objects.create_user(
                username=username,
                email=email,
                password=password1,
                phone_number=phone_number
            )
            user.is_buyer = True
            user.save()

            BuyerProfile.objects.create(
                user=user,
                date_of_birth=date_of_birth
            )

            login(request, user)
            return redirect('main_page')

        except IntegrityError:
            return render(request, 'accounts/buyer_signup.html', {'error': 'مشکلی در ثبت نام پیش آمده است. لطفا دوباره تلاش کنید.'})

    return render(request, 'accounts/buyer_signup.html')


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Authenticate user
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_superuser:
                messages.error(request, 'شما اجازه ورود به عنوان ادمین را ندارید.')
                return redirect('login')

            login(request, user)
            return redirect('main_page')
        else:
            messages.error(request, 'نام کاربری یا رمز عبور اشتباه است.')

    return render(request, 'accounts/login.html')

# Logout View
def user_logout(request):
    if request.method == "POST":
        logout(request)
        return redirect('main_page')
    return redirect('main_page')

# ------------------------------------------------------------- MOBILE OTP --------------------------------------------------

def generate_otp():
    return str(random.randint(100000, 999999))

def send_otp_via_sms(phone_number, otp):
    # Replace this with your SMS sending logic, e.g., using Twilio
    pass

def request_otp(request):
    if request.method == 'POST':
        phone_number = request.POST.get('phone_number')
        user = CustomUser.objects.filter(phone_number=phone_number).first()
        if user:
            otp = generate_otp()
            user.otp = otp
            user.otp_expiry = timezone.now() + datetime.timedelta(minutes=10)  # OTP valid for 10 minutes
            user.save()
            send_otp_via_sms(phone_number, otp)
            return redirect('verify_otp_mobile')
        else:
            return render(request, 'accounts/request_otp.html', {'error': 'Phone number not found.'})
    return render(request, 'accounts/request_otp.html')

def verify_otp_mobile(request):
    if request.method == 'POST':
        phone_number = request.POST.get('phone_number')
        otp = request.POST.get('otp')
        user = CustomUser.objects.filter(phone_number=phone_number, otp=otp).first()
        if user and user.otp_expiry > timezone.now():
            user.otp = None
            user.otp_expiry = None
            user.save()
            # Automatically log in the user
            login(request, user)
            return redirect('main_page')  # Redirect to a success page or dashboard
        else:
            return render(request, 'accounts/verify_otp.html', {'error': 'Invalid or expired OTP.'})
    return render(request, 'accounts/verify_otp.html')

# --------------------------------------------------------- EMAIL OTP ------------------------------------------------------

def generate_otp():
    return get_random_string(length=6, allowed_chars='0123456789')

def send_otp_email(user):
    otp = generate_otp()
    user.otp = otp
    user.otp_expiry = timezone.now() + timezone.timedelta(minutes=5)
    user.save()
    
    subject = 'Your OTP Code'
    message = f'Your OTP code is {otp}'
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [user.email]
    
    send_mail(subject, message, from_email, recipient_list)

def email_login(request):
    if request.method == 'POST':
        form = EmailLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            user = CustomUser.objects.filter(email=email).first()

            if user:
                send_otp_email(user)
                return redirect('verify_otp_email')
            else:
                # User does not exist, create a new user
                new_user = CustomUser.objects.create(email=email, username=email, password=CustomUser.objects.make_random_password())
                send_otp_email(new_user)
                return redirect('verify_otp_email')
    else:
        form = EmailLoginForm()

    return render(request, 'accounts/email_login.html', {'form': form})

def verify_otp_email(request):
    if request.method == 'POST':
        form = OTPForm(request.POST)
        if form.is_valid():
            otp = form.cleaned_data['otp']
            user = request.user
            if user.otp == otp and user.otp_expiry > timezone.now():
                user.otp = None
                user.otp_expiry = None
                user.save()
                login(request, user)
                return redirect('main_page')
            else:
                messages.error(request, 'Invalid OTP or OTP expired')
    else:
        form = OTPForm()
    return render(request, 'accounts/email_verify_otp.html', {'form': form})


def send_otp(request):
    user = request.user
    send_otp_email(user)
    return render(request, 'accounts/email_send_otp.html', {'message': 'OTP has been sent to your email'})
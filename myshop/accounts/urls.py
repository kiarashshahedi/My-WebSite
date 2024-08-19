# accounts/urls.py
from django.urls import path
from . import views


urlpatterns = [
   
    path('signup/', views.buyer_signup, name='buyer_signup'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('request-otp/', views.request_otp, name='request_otp'),
    path('verify-otp-mobile/', views.verify_otp_mobile, name='verify_otp_mobile'),
    path('send-otp/', views.send_otp, name='send_otp'),
    path('verify-otp-email/', views.verify_otp_email, name='verify_otp_email'),
    path('email-login/', views.email_login, name='email_login'),
]

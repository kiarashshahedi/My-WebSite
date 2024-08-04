# accounts/urls.py
from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('signup/seller/', views.seller_signup, name='seller_signup'),
    path('signup/buyer/', views.buyer_signup, name='buyer_signup'),
    path('logout/', LogoutView.as_view(), name='logout'),
    
    path('seller_dashboard/', views.seller_dashboard, name='seller_dashboard'),
    

]

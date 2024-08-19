from django.urls import path
from . import views


urlpatterns = [
    # SELLER 
    path('seller/signup/', views.seller_signup, name='seller_signup'),
    path('seller/dashboard/', views.seller_dashboard, name='seller_dashboard'),

]

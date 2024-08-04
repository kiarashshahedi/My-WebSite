from django.urls import path
from . import views

urlpatterns = [
    path('manage_order/<int:order_id>/', views.manage_order, name='manage_order'),

]

from django.urls import path
from . import views
from dashboard.views import update_bank_details

urlpatterns = [
    path('create/', views.create_order, name='create_order'),
    path('payment/<int:order_id>/', views.payment_view, name='payment'),
    path('status/<int:order_id>/', views.order_status_view, name='order_status'),
    path('seller/orders/', views.seller_orders_view, name='seller_orders'),
    path('seller/update-bank-details/', update_bank_details, name='update_bank_details'),

]

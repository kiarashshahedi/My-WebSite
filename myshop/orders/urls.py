from django.urls import path
from . import views 

urlpatterns = [
    path('checkout/', views.checkout, name='checkout'),
    path('payment/<int:order_id>/', views.payment_view, name='payment_view'),
    path('payment/callback/<int:order_id>/', views.payment_callback, name='payment_callback'),
    path('order/history/', views.order_history, name='order_history'),
    path('order/<int:order_id>/', views.order_detail, name='order_detail'),
]










# from django.urls import path
# from . import views
# from dashboard.views import update_bank_details

# urlpatterns = [
#     path('create/', views.create_order, name='create_order'),
#     path('payment/<int:order_id>/', views.payment_view, name='payment'),
#     path('status/<int:order_id>/', views.order_status_view, name='order_status'),
#     path('seller/orders/', views.seller_orders_view, name='seller_orders'),
#     path('seller/update-bank-details/', update_bank_details, name='update_bank_details'),

# ]

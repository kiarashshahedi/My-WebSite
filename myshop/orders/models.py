# orders/models.py
from django.db import models
from django.contrib.auth import get_user_model
from products.models import Product
from accounts.models import SellerProfile

User = get_user_model()

class Order(models.Model):
    
    # فروشنده
    seller = models.ForeignKey(SellerProfile, on_delete=models.CASCADE, related_name='orders')
    # خریدار
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders') 
    
    # نام مشتری 
    customer_name = models.CharField(max_length=255)
    
    # تاریخ سفارش
    order_date = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # وضعیت 
    status = models.CharField(max_length=50, choices=[('Pending', 'Pending'), ('Completed', 'Completed')])
        
    # محصول
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    
    # تعداد
    quantity = models.PositiveIntegerField()
    
    # قیمت
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    # قیمت کل
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return f"Order #{self.id} by {self.buyer.username}"

class OrderItem(models.Model):
   

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"

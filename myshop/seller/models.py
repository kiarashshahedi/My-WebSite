from django.db import models
from accounts.models import CustomUser

# Seller Profile
class SellerProfile(models.Model):
    
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='seller_profile')
    store_name = models.CharField(max_length=255)
    description = models.TextField()
    logo = models.ImageField(upload_to='seller_logos/', null=True, blank=True)
    
    # شناسه منحصر به فرد برای یک کسب و کار
    business_registration_number = models.CharField(max_length=50, unique=True, null=True, blank=True)
    # زمانی که فروشگاه فروشنده تاسیس شد
    established_date = models.DateField(null=True, blank=True)
    # موقعیت فیزیکی کسب و کار فروشنده
    location = models.CharField(max_length=255, null=True, blank=True)
    # ب سایت تجاری فروشنده
    website = models.URLField(max_length=200, null=True, blank=True)
    # JSON پیوندها به نمایه های رسانه های اجتماعی فروشنده به 
    social_media_links = models.JSONField(null=True, blank=True)
    # میانگین امتیاز فروشنده
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.0)
    # تعداد کل فروش های تکمیل شده
    number_of_sales = models.PositiveIntegerField(default=0)
    # روش ترجیحی فروشنده برای ارسال محصولات
    preferred_shipping_method = models.CharField(max_length=255, null=True, blank=True)
    # ایمیل اختصاصی برای پشتیبانی مشتری
    customer_support_email = models.EmailField(null=True, blank=True)
    # شماره تلفن برای پشتیبانی مشتری
    customer_support_phone = models.CharField(max_length=15, null=True, blank=True)
    # شماره حساب بانکی
    bank_account_number = models.CharField(max_length=20, null=True, blank=True)  
    # شماره_مسیر_بانک
    bank_routing_number = models.CharField(max_length=9, null=True, blank=True)
    
    
    
    def __str__(self):
        return self.store_name
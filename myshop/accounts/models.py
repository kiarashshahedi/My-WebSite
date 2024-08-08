from django.contrib.auth.models import AbstractUser
from django.db import models

# Custom User model
class CustomUser(AbstractUser):
    
    is_seller = models.BooleanField(default=False)
    is_buyer = models.BooleanField(default=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    
    # برای اینکه کاربران بتوانند عکس پروفایل را آپلود کنند
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
    # برای پیگیری زمان عضویت کاربر به پلتفرم 
    date_joined = models.DateTimeField(auto_now_add=True)
    # برای ذخیره آخرین زمان ورود
    last_login = models.DateTimeField(null=True, blank=True)

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

# Buyer Profile
class BuyerProfile(models.Model):
    
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='buyer_profile')
    date_of_birth = models.DateField(null=True, blank=True)
    favorite_categories = models.ManyToManyField('products.Category', blank=True)
    
    # لیست علاقه مندی ها: رابطه خیلی به چند با محصولات برای ردیابی آیتم های لیست خواسته های خریدار
    wishlist = models.ManyToManyField('products.Product', related_name='wishlisted_by', blank=True)
    # رابطه خیلی به چند با سفارشات برای ردیابی خریدهای گذشته خریدار
    buy_history = models.ManyToManyField('orders.Order', related_name='purchased_by', blank=True)
    # ذخیره روش پرداخت ترجیحی خریدار
    preferred_payment_method = models.CharField(max_length=50, null=True, blank=True)
    # آدرس پیش فرضی که خریدار برای ارسال ترجیح می دهد.
    preferred_shipping_address = models.TextField(null=True, blank=True)
    # برای ارتباط
    communication_preferences = models.JSONField(null=True, blank=True)
    # امتیازهای وفاداری کسب شده توسط خریدار را پیگیری کنید
    loyalty_points = models.PositiveIntegerField(default=0)
    # اینکه آیا خریدار مشترک خبرنامه است
    newsletter_subscription = models.BooleanField(default=False)

    
    def __str__(self):
        return self.user.username

from django.contrib.auth.models import AbstractUser
from django.db import models

# Custom User model
class CustomUser(AbstractUser):
    
    is_seller = models.BooleanField(default=False)
    is_buyer = models.BooleanField(default=True)
    
    phone_number = models.CharField(max_length=11, unique=True, null=True, blank=True)
    otp = models.CharField(max_length=6, null=True, blank=True)  
    otp_expiry = models.DateTimeField(null=True, blank=True)  
    email = models.CharField(max_length=50, unique=True, null=True, blank=True)

    # برای اینکه کاربران بتوانند عکس پروفایل را آپلود کنند
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
    # برای پیگیری زمان عضویت کاربر به پلتفرم 
    date_joined = models.DateTimeField(auto_now_add=True)
    # برای ذخیره آخرین زمان ورود
    last_login = models.DateTimeField(null=True, blank=True)


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
    # address fields
    shipping_addresses = models.ManyToManyField('ShippingAddress', blank=True)
    billing_address = models.ForeignKey('ShippingAddress', related_name='billing_address_for', null=True, blank=True, on_delete=models.SET_NULL)
    
    def __str__(self):
        return self.user.username

    def get_last_orders(self):
        return self.buy_history.order_by('-created_at')[:5]
    
    def get_total_spent(self):
        return sum(order.total_price for order in self.buy_history.all())
    
    def add_to_wishlist(self, product):
        self.wishlist.add(product)
    
    def remove_from_wishlist(self, product):
        self.wishlist.remove(product)

# address model 
class ShippingAddress(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name=("user"))
    address_line1 = models.CharField(max_length=255, verbose_name=("address line 1"))
    address_line2 = models.CharField(max_length=255, blank=True, verbose_name=("address line 2"))
    city = models.CharField(max_length=100, verbose_name=("city"))
    state = models.CharField(max_length=100, verbose_name=("state"))
    postal_code = models.CharField(max_length=20, verbose_name=("postal code"))
    country = models.CharField(max_length=100, verbose_name=("country"))
    is_default = models.BooleanField(default=False, verbose_name=("is default"))

    def __str__(self):
        return f"{self.address_line1}, {self.city}, {self.country}"
    




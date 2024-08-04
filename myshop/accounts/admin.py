from django.contrib import admin
from .models import CustomUser, SellerProfile, BuyerProfile

admin.site.register(CustomUser)
admin.site.register(SellerProfile)
admin.site.register(BuyerProfile)

from django.contrib import admin
from .models import CustomUser, BuyerProfile, ShippingAddress

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_seller', 'is_buyer')
    search_fields = ('username', 'email')


@admin.register(BuyerProfile)
class BuyerProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'loyalty_points')
    search_fields = ('user__username',)

@admin.register(ShippingAddress)
class ShippingAddressAdmin(admin.ModelAdmin):
    list_display = ('user', 'address_line1', 'city')
    search_fields = ('user__username', 'address_line1')

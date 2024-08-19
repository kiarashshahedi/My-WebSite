from django.contrib import admin
from .models import SellerProfile


@admin.register(SellerProfile)
class SellerProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'store_name', 'rating')
    search_fields = ('store_name',)
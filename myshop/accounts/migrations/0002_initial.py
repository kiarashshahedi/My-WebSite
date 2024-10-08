# Generated by Django 5.0.7 on 2024-08-20 15:18

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
        ('orders', '0001_initial'),
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='buyerprofile',
            name='buy_history',
            field=models.ManyToManyField(blank=True, related_name='purchased_by', to='orders.order'),
        ),
        migrations.AddField(
            model_name='buyerprofile',
            name='favorite_categories',
            field=models.ManyToManyField(blank=True, to='products.category'),
        ),
        migrations.AddField(
            model_name='buyerprofile',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='buyer_profile', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='buyerprofile',
            name='wishlist',
            field=models.ManyToManyField(blank=True, related_name='wishlisted_by', to='products.product'),
        ),
        migrations.AddField(
            model_name='shippingaddress',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='user'),
        ),
        migrations.AddField(
            model_name='buyerprofile',
            name='billing_address',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='billing_address_for', to='accounts.shippingaddress'),
        ),
        migrations.AddField(
            model_name='buyerprofile',
            name='shipping_addresses',
            field=models.ManyToManyField(blank=True, to='accounts.shippingaddress'),
        ),
    ]

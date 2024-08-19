from django import forms
from .models import BuyerProfile, ShippingAddress

# show the bank status and payments to seller



class BuyerProfileForm(forms.ModelForm):
    class Meta:
        model = BuyerProfile
        fields = ['date_of_birth', 'favorite_categories', 'preferred_payment_method', 'preferred_shipping_address', 'communication_preferences', 'newsletter_subscription']
        widgets = {
            'communication_preferences': forms.Textarea(attrs={'class': 'form-control'}),
        }

class ShippingAddressForm(forms.ModelForm):
    class Meta:
        model = ShippingAddress
        fields = ['address_line1', 'address_line2', 'city', 'state', 'postal_code', 'country', 'is_default']
        widgets = {
            'address_line1': forms.TextInput(attrs={'class': 'form-control'}),
            'address_line2': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'state': forms.TextInput(attrs={'class': 'form-control'}),
            'postal_code': forms.TextInput(attrs={'class': 'form-control'}),
            'country': forms.TextInput(attrs={'class': 'form-control'}),
            'is_default': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

# email OTP sending form     
class EmailLoginForm(forms.Form):
    email = forms.EmailField()

class OTPForm(forms.Form):
    otp = forms.CharField(max_length=6)
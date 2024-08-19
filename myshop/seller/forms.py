from django import forms
from .models import SellerProfile



class SellerBankDetailsForm(forms.ModelForm):
    class Meta:
        model = SellerProfile
        fields = ['bank_account_number', 'bank_routing_number']
        labels = {
            'bank_account_number': 'Bank Account Number',
            'bank_routing_number': 'Bank Routing Number',
        }
        widgets = {
            'bank_account_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your bank account number'}),
            'bank_routing_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your bank routing number'}),
        }
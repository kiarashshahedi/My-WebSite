from django import forms
from .models import ProductReview
from accounts.models import BuyerProfile

class ProductReviewForm(forms.ModelForm):
    class Meta:
        model = ProductReview
        fields = ['rating', 'title', 'body']
        widgets = {
            'rating': forms.Select(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'body': forms.Textarea(attrs={'class': 'form-control'}),
        }

# for show interest products to each user 
class FavoriteCategoriesForm(forms.ModelForm):
    class Meta:
        model = BuyerProfile
        fields = ['favorite_categories']
        widgets = {
            'favorite_categories': forms.CheckboxSelectMultiple(),
        }

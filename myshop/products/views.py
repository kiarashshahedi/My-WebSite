from django.shortcuts import render, redirect
from .models import Product
from django.contrib.auth.decorators import login_required
from .forms import ProductForm
def product_list(request):
    products = Product.objects.all()
    return render(request, 'products/product_list.html', {'products': products})

def home(request):
    return render(request, 'products/home.html')

@login_required
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.seller = request.user.seller_profile
            product.save()
            return redirect('seller_dashboard')
    else:
        form = ProductForm()
    return render(request, 'add_product.html', {'form': form})
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from products.models import Product
from orders.models import Order
from seller.forms import SellerBankDetailsForm
from products.forms import ProductForm
from accounts.models import BuyerProfile, ShippingAddress
from accounts.forms import BuyerProfileForm
from django.utils import translation
from django.contrib import messages

@login_required
def seller_dashboard(request):
    seller_profile = request.user.seller_profile
    products = Product.objects.filter(seller=seller_profile)
    orders = Order.objects.filter(items__product__seller=seller_profile).distinct()
    
    # Summarize data for overview
    total_sales = orders.filter(status='completed').count()
    total_revenue = sum(order.total_price for order in orders.filter(status='completed'))
    
    context = {
        'seller_profile': seller_profile,
        'products': products,
        'orders': orders,
        'total_sales': total_sales,
        'total_revenue': total_revenue,
    }
    
    return render(request, 'dashboard/dashboard.html', context)

@login_required
def manage_products(request):
    products = Product.objects.filter(seller=request.user.seller_profile)
    return render(request, 'dashboard/manage_products.html', {'products': products})

@login_required
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.seller = request.user.seller_profile
            product.save()
            return redirect('manage_products')
    else:
        form = ProductForm()
    return render(request, 'dashboard/add_product.html', {'form': form})

@login_required
def edit_product(request, product_id):
    # Get the product to edit, ensuring it belongs to the current seller
    product = get_object_or_404(Product, id=product_id, seller=request.user.seller_profile)
    
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()  # Save the updated product
            return redirect('manage_products')  # Redirect to the product management page
    else:
        form = ProductForm(instance=product)  # Populate the form with the product's existing data

    return render(request, 'dashboard/edit_product.html', {'form': form, 'product': product})

@login_required
def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id, seller=request.user.seller_profile)
    if request.method == 'POST':
        product.delete()
        return redirect('manage_products')
    return render(request, 'dashboard/delete_product.html', {'product': product})

@login_required
def view_orders(request):
    orders = Order.objects.filter(items__product__seller=request.user.seller_profile).distinct()
    return render(request, 'dashboard/view_orders.html', {'orders': orders})

@login_required
def update_bank_details(request):
    seller_profile = request.user.seller_profile
    if request.method == 'POST':
        form = SellerBankDetailsForm(request.POST, instance=seller_profile)
        if form.is_valid():
            form.save()
            return redirect('seller_dashboard')
    else:
        form = SellerBankDetailsForm(instance=seller_profile)
    return render(request, 'dashboard/update_bank_details.html', {'form': form})


# DASHBOARD
@login_required
def buyer_dashboard(request):
    if hasattr(request.user, 'seller_profile'):
        return redirect('seller_dashboard')  # Redirect sellers

    buyer_profile = get_object_or_404(BuyerProfile, user=request.user)
    orders = buyer_profile.get_last_orders()

    context = {
        'buyer_profile': buyer_profile,
        'orders': orders,
    }

    return render(request, 'dashboard/buyer_dashboard.html', context)

# UPDATE BUYER PROFILE
@login_required
def update_buyer_profile(request):
    buyer_profile = get_object_or_404(BuyerProfile, user=request.user)
    
    if request.method == 'POST':
        form = BuyerProfileForm(request.POST, instance=buyer_profile)
        if form.is_valid():
            form.save()
            return redirect('buyer_dashboard')
    else:
        form = BuyerProfileForm(instance=buyer_profile)
    
    return render(request, 'dashboard/update_buyer_profile.html', {'form': form})


@login_required
def manage_shipping_addresses(request):
    buyer_profile = get_object_or_404(BuyerProfile, user=request.user)
    addresses = ShippingAddress.objects.filter(user=request.user)

    if request.method == 'POST':
        address_line1 = request.POST.get('address_line1')
        address_line2 = request.POST.get('address_line2')
        city = request.POST.get('city')
        state = request.POST.get('state')
        postal_code = request.POST.get('postal_code')
        country = request.POST.get('country')
        is_default = request.POST.get('is_default') == 'on'

        new_address = ShippingAddress(
            user=request.user,
            address_line1=address_line1,
            address_line2=address_line2,
            city=city,
            state=state,
            postal_code=postal_code,
            country=country,
            is_default=is_default
        )
        new_address.save()

        return redirect('manage_shipping_addresses')

    return render(request, 'dashboard/manage_shipping_addresses.html', {'addresses': addresses})

@login_required
def update_shipping_address(request, id):
    
    translation.activate('fa')

    address = get_object_or_404(ShippingAddress, id=id, user=request.user)
    
    if request.method == 'POST':
        address.address_line1 = request.POST.get('address_line1')
        address.address_line2 = request.POST.get('address_line2')
        address.city = request.POST.get('city')
        address.state = request.POST.get('state')
        address.postal_code = request.POST.get('postal_code')
        address.country = request.POST.get('country')
        address.is_default = request.POST.get('is_default') == 'on'
        
        address.save()
        messages.success(request, ('Shipping address updated successfully.'))
        return redirect('manage_shipping_addresses')

    context = {
        'form': {
            'address_line1': address.address_line1,
            'address_line2': address.address_line2,
            'city': address.city,
            'state': address.state,
            'postal_code': address.postal_code,
            'country': address.country,
            'is_default': address.is_default,
        }
    }
    
    return render(request, 'dashboard/update_shipping_address.html', context)
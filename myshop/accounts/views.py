from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from .forms import SellerBankDetailsForm, BuyerProfileForm, ShippingAddressForm
from .models import SellerProfile, BuyerProfile, ShippingAddress
# models 
from products.models import Product
from orders.models import Order
from .models import CustomUser, SellerProfile, BuyerProfile





# ------------------------------------------------------------ seller -------------------------------------------------------

# ثبت نام فروشنده
def seller_signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        store_name = request.POST.get('store_name')
        description = request.POST.get('description')
        
        # Simple validation
        if not username or not password1 or not password2 or not email:
            return render(request, 'accounts/seller_signup.html', {'error': 'تمامی فیلدها الزامی هستند.'})
        
        if password1 != password2:
            return render(request, 'accounts/seller_signup.html', {'error': 'رمز عبورها مطابقت ندارند.'})

        try:
            # Check if username already exists
            if CustomUser.objects.filter(username=username).exists():
                return render(request, 'accounts/seller_signup.html', {'error': 'این نام کاربری قبلا ثبت شده است.'})

            # Create the user
            user = CustomUser.objects.create_user(
                username=username,
                email=email,
                password=password1,
                phone_number=phone_number
            )
            user.is_seller = True
            user.save()

            # Create the seller profile
            SellerProfile.objects.create(
                user=user,
                store_name=store_name,
                description=description
            )

            # Log in the user and redirect
            login(request, user)
            return redirect('main_page')

        except IntegrityError:
            # Handle cases where there is an unexpected database error
            return render(request, 'accounts/seller_signup.html', {'error': 'مشکلی در ثبت نام پیش آمده است. لطفا دوباره تلاش کنید.'})
    
    return render(request, 'accounts/seller_signup.html')

# نمایش لیست محصولات و سفارشات فروشنده
@login_required
def seller_dashboard(request):
    products = request.user.seller_profile.products.all()
    orders = Order.objects.filter(product__seller=request.user.seller_profile)
    return render(request, 'accounts/seller_dashboard.html', {'products': products, 'orders': orders})

# show bank and payments to seller
@login_required
def update_bank_details(request):
    seller_profile = request.user.seller_profile

    if request.method == 'POST':
        form = SellerBankDetailsForm(request.POST, instance=seller_profile)
        if form.is_valid():
            form.save()
            return redirect('seller_dashboard')  # Redirect to seller's dashboard after saving
    else:
        form = SellerBankDetailsForm(instance=seller_profile)

    return render(request, 'seller/update_bank_details.html', {'form': form})

# --------------------------------------------------- buyer ----------------------------------------------------------

# ثبت نام خریدار
def buyer_signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        date_of_birth = request.POST.get('date_of_birth')

        if not username or not password1 or not password2 or not email:
            return render(request, 'accounts/buyer_signup.html', {'error': 'تمامی فیلدها الزامی هستند.'})

        if password1 != password2:
            return render(request, 'accounts/buyer_signup.html', {'error': 'رمز عبورها مطابقت ندارند.'})

        try:
            if CustomUser.objects.filter(username=username).exists():
                return render(request, 'accounts/buyer_signup.html', {'error': 'این نام کاربری قبلا ثبت شده است.'})

            user = CustomUser.objects.create_user(
                username=username,
                email=email,
                password=password1,
                phone_number=phone_number
            )
            user.is_buyer = True
            user.save()

            BuyerProfile.objects.create(
                user=user,
                date_of_birth=date_of_birth
            )

            login(request, user)
            return redirect('main_page')

        except IntegrityError:
            return render(request, 'accounts/buyer_signup.html', {'error': 'مشکلی در ثبت نام پیش آمده است. لطفا دوباره تلاش کنید.'})

    return render(request, 'accounts/buyer_signup.html')

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


# BUYER SHIPPING ADDRESS 
@login_required
def manage_shipping_addresses(request):
    buyer_profile = get_object_or_404(BuyerProfile, user=request.user)
    addresses = ShippingAddress.objects.filter(user=request.user)

    if request.method == 'POST':
        form = ShippingAddressForm(request.POST)
        if form.is_valid():
            address = form.save(commit=False)
            address.user = request.user
            address.save()
            return redirect('manage_shipping_addresses')
    else:
        form = ShippingAddressForm()

    return render(request, 'dashboard/manage_shipping_addresses.html', {'form': form, 'addresses': addresses})

# BUYER ORDER HISTORY
@login_required
def order_history(request):
    buyer_profile = get_object_or_404(BuyerProfile, user=request.user)
    orders = buyer_profile.buy_history.all()

    return render(request, 'dashboard/order_history.html', {'orders': orders})

# BUYER ORDER STATUS
@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, purchased_by=request.user.buyer_profile)
    return render(request, 'dashboard/order_detail.html', {'order': order})

# ------------------------------------------------------------ end buyer---------------------------------------------------


from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from .forms import SellerBankDetailsForm
from .models import SellerProfile

# models 
from products.models import Product
from orders.models import Order
from .models import CustomUser, SellerProfile, BuyerProfile

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
            return redirect('home')

        except IntegrityError:
            # Handle cases where there is an unexpected database error
            return render(request, 'accounts/seller_signup.html', {'error': 'مشکلی در ثبت نام پیش آمده است. لطفا دوباره تلاش کنید.'})
    
    return render(request, 'accounts/seller_signup.html')

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
            return redirect('home')

        except IntegrityError:
            return render(request, 'accounts/buyer_signup.html', {'error': 'مشکلی در ثبت نام پیش آمده است. لطفا دوباره تلاش کنید.'})

    return render(request, 'accounts/buyer_signup.html')

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
from django.shortcuts import render, redirect, get_object_or_404
from .models import Cart, CartItem, Product
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

@login_required
def cart_detail(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    return render(request, 'cart/cart_detail.html', {'cart': cart})

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    
    if created:
        cart_item.quantity = 1  # Default quantity if newly added
    else:
        # Ensure that the quantity does not exceed the maximum limit
        if cart_item.quantity < 5:
            cart_item.quantity += 1
        cart_item.save()
    
    return redirect('cart_detail')

@login_required
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    cart_item.delete()
    return redirect('cart_detail')

@login_required
def update_cart(request):
    if request.method == 'POST':
        cart, created = Cart.objects.get_or_create(user=request.user)
        
        for item in cart.items.all():
            new_quantity = int(request.POST.get(f'quantity_{item.id}', item.quantity))
            
            # Ensure the new quantity is between 1 and 5
            if 1 <= new_quantity <= 5:
                item.quantity = new_quantity
                item.save()
            elif new_quantity > 5:
                item.quantity = 5  # Set to maximum limit if exceeded
                item.save()
        
        # Return a JSON response to indicate success
        return JsonResponse({'status': 'success'})
    
    # Handle non-POST requests or errors
    return JsonResponse({'status': 'error'}, status=400)


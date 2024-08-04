from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import OrderForm
from .models import Order

@login_required
def manage_order(request, order_id):
    order = Order.objects.get(id=order_id)
    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('seller_dashboard')
    else:
        form = OrderForm(instance=order)
    return render(request, 'manage_order.html', {'form': form, 'order': order})
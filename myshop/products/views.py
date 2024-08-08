from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Category, ProductReview
from django.contrib.auth.decorators import login_required
from .forms import ProductReviewForm


def home(request):
    return render(request, 'products/home.html')

def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(stock__gt=0)

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)

    return render(request, 'products/product_list.html', {
        'category': category,
        'categories': categories,
        'products': products
    })

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    related_products = Product.objects.filter(category=product.category).exclude(id=product.id)[:4]
    reviews = product.reviews.all()

    return render(request, 'products/product_detail.html', {
        'product': product,
        'related_products': related_products,
        'reviews': reviews
    })

@login_required
def add_product_review(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        form = ProductReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.user = request.user
            review.save()
            return redirect('product_detail', product_id=product.id)
    else:
        form = ProductReviewForm()

    return render(request, 'products/add_product_review.html', {'form': form, 'product': product})


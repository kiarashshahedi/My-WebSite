# for showing different products in main page by users interest and like


from .models import Product, Category

def recommend_products(user):
    # Get user's favorite categories
    profile = user.buyer_profile
    favorite_categories = profile.favorite_categories.all()

    # Recommend products from favorite categories
    recommended_products = Product.objects.filter(category__in=favorite_categories).distinct()

    return recommended_products

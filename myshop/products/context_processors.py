from .models import Category

def category_list(request):
    # Fetch all categories with their subcategories
    categories = Category.objects.filter(parent__isnull=True)  # Main categories
    subcategories = Category.objects.exclude(parent__isnull=True)  # Subcategories

    return {
        'categories': categories,
        'subcategories': subcategories
    }
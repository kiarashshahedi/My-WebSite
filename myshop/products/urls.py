from django.urls import path
from . import views

urlpatterns = [
    path('', views.main_page, name='main_page'),
    path('products/<slug:slug>/', views.product_list, name='product_list'),
    path('category/<slug:category_slug>/', views.product_list, name='product_list_by_category'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('product/<int:product_id>/review/', views.add_product_review, name='add_product_review'),
    path('update-preferences/', views.update_preferences, name='update_preferences'),
    path('category/<slug:slug>/', views.category_list, name='category_detail'),


]

    
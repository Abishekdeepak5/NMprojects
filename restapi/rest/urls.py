from django.urls import path
from .views import ProductList, ProductDetail, CategoryList, CategoryDetail

urlpatterns = [
    path('products/', ProductList.as_view(), name='product_list'),
    path('products/<int:pk>/', ProductDetail.as_view(), name='product_detail'),
    path('categories/', CategoryList.as_view(), name='category_list'),
    path('categories/<int:pk>/', CategoryDetail.as_view(), name='category_detail'),
]

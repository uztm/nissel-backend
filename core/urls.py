from django.urls import path
from .views import ProductListAPIView, ProductDetailAPIView, OrderCreateAPIView

urlpatterns = [
    path('products', ProductListAPIView.as_view(), name='product-list'),
    path('product/<uuid:id>', ProductDetailAPIView.as_view(), name='product-detail'),
    path('order', OrderCreateAPIView.as_view(), name='order-create'),
]

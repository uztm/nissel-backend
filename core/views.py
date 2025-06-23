from rest_framework import generics
from .models import Product, Order
from .serializers import ProductSerializer, OrderSerializer

class ProductListAPIView(generics.ListAPIView):
    queryset = Product.objects.prefetch_related('images').all()
    serializer_class = ProductSerializer


class ProductDetailAPIView(generics.RetrieveAPIView):
    queryset = Product.objects.prefetch_related('images').all()
    serializer_class = ProductSerializer
    lookup_field = 'id'


class OrderCreateAPIView(generics.CreateAPIView):
    serializer_class = OrderSerializer

from rest_framework import serializers
from .models import Product, ProductImage, Order

class ProductImageSerializer(serializers.ModelSerializer):
    image = serializers.ImageField()

    class Meta:
        model = ProductImage
        fields = ['image']


class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True)
    category = serializers.StringRelatedField()
    discount = serializers.ReadOnlyField()

    class Meta:
        model = Product
        fields = [
            'id', 'title', 'description', 'images', 'price', 'original_price',
            'category', 'brand', 'rating', 'in_stock', 'stock_count',
            'tags', 'discount', 'features', 'return_policy', 'warranty'
        ]


class OrderSerializer(serializers.ModelSerializer):
    products = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Product.objects.all(),
        required=False  # 👈 This makes the field optional
    )

    class Meta:
        model = Order
        fields = ['id', 'full_name', 'phone_number', 'region', 'products']
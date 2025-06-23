import uuid
from django.db import models
from django.utils.functional import cached_property


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.PositiveIntegerField()
    original_price = models.PositiveIntegerField()
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='products')
    brand = models.CharField(max_length=100)
    rating = models.FloatField(default=0.0)
    in_stock = models.BooleanField(default=True)
    stock_count = models.PositiveIntegerField()
    tags = models.JSONField(default=list)
    features = models.JSONField(default=list)
    return_policy = models.CharField(max_length=255, blank=True)
    warranty = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.title

    @cached_property
    def discount(self):
        if self.original_price and self.original_price > self.price:
            return round((self.original_price - self.price) / self.original_price * 100)
        return 0


class ProductImage(models.Model):
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='product_images/')  # 👈 upload file

class Order(models.Model):
    STATUS_CHOICES = [
        ('new', '🆕 New'),
        ('processing', '🔄 Processing'),
        ('shipped', '📦 Shipped'),
        ('delivered', '✅ Delivered'),
        ('cancelled', '❌ Cancelled'),
    ]


    full_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=30)
    region = models.CharField(max_length=100)
    products = models.ManyToManyField('Product')
    created_at = models.DateTimeField(auto_now_add=True)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    internal_note = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.full_name} – {self.status}"
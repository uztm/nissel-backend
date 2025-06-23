from django.contrib import admin
from django.utils.html import format_html
import json
from django import forms
from .models import Category, Product, ProductImage, Order
from .widgets import RepeaterListWidget
from django.contrib.auth.models import User, Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.safestring import mark_safe



class JSONListField(forms.Field):
    def to_python(self, value):
        if not value:
            return []
        if isinstance(value, list):
            return value
        try:
            return json.loads(value)
        except Exception:
            raise forms.ValidationError("Enter a valid list.")

    def prepare_value(self, value):
        if isinstance(value, list):
            return json.dumps(value, ensure_ascii=False)
        return value


class UserAdmin(BaseUserAdmin):
    def has_add_permission(self, request):
        return request.user.is_superuser  # Only superusers can add users

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        return False  # Staff can’t edit any user

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser  # Only superusers can delete users

    def get_model_perms(self, request):
        if request.user.is_superuser:
            return super().get_model_perms(request)
        return {}  # Hide for staff

admin.site.unregister(User)
admin.site.register(User, UserAdmin)

# ----- Product Admin Form with custom widgets for tags & features -----

class ProductAdminForm(forms.ModelForm):
    tags = JSONListField(required=False, widget=RepeaterListWidget())
    features = JSONListField(required=False, widget=RepeaterListWidget())

    class Meta:
        model = Product
        fields = '__all__'


# ----- Inline images with preview -----
class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    fields = ('image', 'image_preview',)
    readonly_fields = ('image_preview',)

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="100" style="border-radius:8px"/>', obj.image.url)
        return "-"
    image_preview.short_description = "Preview"


# ----- Product Admin -----
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    form = ProductAdminForm
    inlines = [ProductImageInline]
    list_display = ('title', 'price', 'stock_count', 'in_stock', 'thumbnail')
    readonly_fields = ('thumbnail',)

    def get_model_perms(self, request):
        if request.user.is_staff or request.user.is_superuser:
            return super().get_model_perms(request)
        return {}

    def thumbnail(self, obj):
        first_image = obj.images.first()
        if first_image and first_image.image:
            return format_html('<img src="{}" width="80" style="border-radius:6px"/>', first_image.image.url)
        return "-"
    thumbnail.short_description = "Image"


# ----- Category Admin -----
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']

    def get_model_perms(self, request):
        if request.user.is_staff or request.user.is_superuser:
            return super().get_model_perms(request)
        return {}


# ----- Order Admin -----
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = [
        'full_name_display',
        'region',
        'phone_number',
        'created_at',
        'product_images_preview',
        'status',  # status is shown but not clickable
    ]

    # ✅ Only non-editable fields in list_display_links
    list_display_links = [
        'full_name_display',
        'region',
        'phone_number',
        'created_at',
        'product_images_preview',
    ]

    # ✅ status is editable (must NOT be in list_display_links)
    list_editable = ['status']

    readonly_fields = ['created_at', 'product_images_preview']
    list_filter = ['status', 'created_at', 'region']
    search_fields = ['full_name', 'phone_number', 'region']
    ordering = ['-created_at']
    date_hierarchy = 'created_at'

    fieldsets = (
        ("Customer Information", {
            "fields": ("full_name", "phone_number", "region", "products"),
            "description": "Customer contact and product selection.",
        }),
        ("Order Tracking", {
            "fields": ("status", "internal_note", "created_at", "product_images_preview"),
            "description": "Track order state and leave internal notes.",
        }),
    )

    def full_name_display(self, obj):
        return format_html('<span style="font-weight: 600;">{}</span>', obj.full_name)

    full_name_display.short_description = "Customer"

    def product_images_preview(self, obj):
        images = []
        for product in obj.products.all():
            first_image = product.images.first()
            if first_image and first_image.image:
                images.append(
                    f'''
                    <img src="{first_image.image.url}" width="50" height="50"
                         style="margin:3px; border-radius:6px; object-fit:cover; box-shadow:0 1px 4px rgba(0,0,0,0.08);"
                         title="{product.title}" />
                    '''
                )
        return format_html(''.join(images)) if images else "-"

    def get_model_perms(self, request):
        """
        Only show model in admin sidebar if staff or superuser
        """
        if request.user.is_staff or request.user.is_superuser:
            return super().get_model_perms(request)
        return {}  # Hide from others

    product_images_preview.short_description = "Products"

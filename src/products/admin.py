from django.contrib import admin

from products.models import Product, Variation, ProductImage, Category


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 0

class VariationInline(admin.TabularInline):
    model = Variation
    extra = 0

class ProductAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'price', 'id']
    inlines = [
        ProductImageInline,
        VariationInline
    ]
    class Meta:
        model = Product


admin.site.register(Product, ProductAdmin)
admin.site.register(Category)

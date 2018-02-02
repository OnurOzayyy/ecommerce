from django.contrib import admin

from products.models import Product, Variation


class VariationInline(admin.TabularInline):
    model = Variation
    extra = 0

class ProductAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'price', 'id']
    inlines = [
        VariationInline
    ]
    class Meta:
        model = Product


admin.site.register(Product, ProductAdmin)

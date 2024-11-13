from django.contrib import admin

from .models import Category, Product, ProductPrice, ProductPriceHistory


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'category',
        'sku',
        'description',
    )
    search_fields = ('name', 'sku', 'category__name')
    list_filter = ('category',)


@admin.register(ProductPrice)
class ProductPriceAdmin(admin.ModelAdmin):
    list_display = (
        'product',
        'start_date',
        'end_date',
        'price',
    )
    search_fields = ('product__name', 'product__sku')
    list_filter = ('product__category',)
    date_hierarchy = 'start_date'


@admin.register(ProductPriceHistory)
class ProductPriceHistoryAdmin(admin.ModelAdmin):
    list_display = (
        'product_name',
        'product_sku',
        'start_date',
        'end_date',
        'price',
        'action',
        'change_date',
    )
    search_fields = ('product_name', 'product_sku')
    list_filter = ('action', 'change_date')
    date_hierarchy = 'change_date'

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

from rest_framework import serializers

from storage.models import Category, Product, ProductPrice


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'category', 'sku', 'description']


class ProductPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductPrice
        fields = ['id', 'product', 'start_date', 'end_date', 'price']
        read_only_fields = ['id', 'product']

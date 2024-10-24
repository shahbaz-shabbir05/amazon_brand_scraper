from rest_framework import serializers
from .models import Brand, Product

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'asin', 'sku', 'image', 'last_updated']

class BrandSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True, read_only=True)

    class Meta:
        model = Brand
        fields = ['id', 'name', 'amazon_brand_url', 'products']

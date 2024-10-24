from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework import generics

from .models import Brand, Product
from .serializers import BrandSerializer, ProductSerializer


class BrandListAPIView(generics.ListAPIView):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer


class ProductListAPIView(generics.ListAPIView):
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['brand__id']
    search_fields = ['name', 'asin', 'sku']

    def get_queryset(self):
        brand_id = self.kwargs.get('brand_id')
        return Product.objects.filter(brand__id=brand_id)

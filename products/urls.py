from django.urls import path

from products.views import BrandListAPIView, ProductListAPIView

app_name = 'products'

urlpatterns = [
    path('brands/', BrandListAPIView.as_view(), name='brand_list'),
    path('brands/<int:brand_id>/products/', ProductListAPIView.as_view(), name='product_list'),
]

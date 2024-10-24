from django.db import models


class Brand(models.Model):
    name = models.CharField(max_length=255, unique=True)
    amazon_brand_url = models.URLField(help_text="Amazon brand page URL")

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=255)
    asin = models.CharField(max_length=10, unique=True)
    sku = models.CharField(max_length=50, blank=True, null=True)
    image = models.URLField(blank=True, null=True)
    brand = models.ForeignKey(Brand, related_name='products', on_delete=models.CASCADE)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

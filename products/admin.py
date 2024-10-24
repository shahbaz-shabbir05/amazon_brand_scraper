from django.contrib import admin

from .models import Brand, Product


class ProductInline(admin.TabularInline):
    model = Product
    extra = 0
    readonly_fields = ('last_updated',)
    can_delete = False


# @admin.action(description='Scrape selected brands')
# def scrape_selected_brands(modeladmin, request, queryset):
#     for brand in queryset:
#         scrape_brand_products.delay(brand.id)
#     modeladmin.message_user(request, "Scraping tasks initiated for selected brands.")



@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'amazon_brand_url')
    search_fields = ('name',)
    inlines = [ProductInline]
    # actions = [scrape_selected_brands]


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'asin', 'sku', 'brand', 'last_updated')
    search_fields = ('name', 'asin', 'sku', 'brand__name')
    list_filter = ('brand',)

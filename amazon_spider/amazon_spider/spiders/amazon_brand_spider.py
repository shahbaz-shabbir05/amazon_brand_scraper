import logging
import random
import time
from urllib.parse import urljoin
from django.core.cache import cache

import scrapy

from products.models import Brand, Product

logger = logging.getLogger(__name__)


class AmazonBrandSpider(scrapy.Spider):
    name = 'amazon_brand_spider'

    def start_requests(self):
        brands = Brand.objects.all()
        for brand in brands:
            yield scrapy.Request(
                url=brand.amazon_brand_url,
                callback=self.parse,
                meta={'brand_id': brand.id},
            )

    def parse(self, response):
        if "captcha" in response.url.lower() or "captcha" in response.text.lower():
            # Capture CAPTCHA image or challenge
            captcha_image = response.css('img.captcha-image::attr(src)').get()
            # Send CAPTCHA to solving service
            solved_captcha = None  # solve_captcha(captcha_image)
            # Retry request with CAPTCHA solution
            yield scrapy.FormRequest.from_response(
                response,
                formdata={'captcha_field': solved_captcha},
                callback=self.parse
            )
        brand_id = response.meta['brand_id']
        cache_key = f"brand_{brand_id}_last_scraped"
        last_scraped = cache.get(cache_key)
        if last_scraped and (time.timezone.now() - last_scraped).total_seconds() < 21600:
            logger.info(f"Skipping brand ID {brand_id} - recently scraped.")
            return
        print("\n\n\nbrand_id: ", brand_id, "\n\n\n")
        brand = Brand.objects.get(id=brand_id)

        brand_id = response.meta['brand_id']
        try:
            brand = Brand.objects.get(id=brand_id)
        except Brand.DoesNotExist:
            logger.error(f"Brand with id {brand_id} does not exist.")
            return

        # Parse product listings
        # products = response.css('div.s-main-slot div[data-component-type="s-search-result"]')
        products = response.css('div.s-main-slot div.s-result-item[data-asin]')
        print("\n\n\nPRODUCTS: ", products, "\n\n\n")
        print("\n\n\nPRODUCTS: ", len(products), "\n\n\n")

        for product in products:
            name = product.css('h2 a span::text').get()
            asin = product.attrib.get('data-asin')
            asin_1 = product.css('::attr(data-asin)').get()
            print("\n\n\nASIN", asin == asin_1, "ASIN\n\n\n")
            sku = product.css('span.sku::text').get(default='').strip()
            # sku = product.css('::attr(data-sku)').get()
            image = product.css('img.s-image::attr(src)').get()
            # image = product.css('.s-image::attr(src)').get()

            product_url = product.css('.a-link-normal::attr(href)').get()
            print("\n\n\nproduct_url: ", product_url, "\n\n\n")

            # Complete product URL
            if product_url:
                product_url = urljoin(response.url, product_url)
                print("\n\n\nproduct_url_new: ", product_url, "\n\n\n")

            # If the ASIN is available, follow the product detail page to extract SKU
            if asin and product_url:
                yield scrapy.Request(
                    url=product_url,
                    callback=self.parse_product_detail,
                    meta={
                        'asin': asin,
                        'name': name,
                        'image': image,
                        'brand_id': brand_id
                    }
                )
                cache.set(cache_key, time.timezone.now(), timeout=21600)  # 6 hours

            # 1
            # name = product.css('.product-name::text').get()
            # asin = product.css('.asin::text').get()
            # sku = product.css('.sku::text').get(default='')
            # image = product.css('.product-image::attr(src)').get()

            # 2
            # name = product.css('.a-text-normal::text').get()
            # asin = product.css('::attr(data-asin)').get()  # Extract ASIN
            # sku = product.css('.s-sku::text').get(default='')
            # image = product.css('.s-image::attr(src)').get()

            # if asin:
            #     Product.objects.update_or_create(
            #         asin=asin,
            #         defaults={
            #             'name': name,
            #             'sku': sku,
            #             'image': image,
            #             'brand': brand
            #         }
            #     )

        # Handle pagination
        # next_page = response.css('ul.a-pagination li.a-last a::attr(href)').get()
        # if next_page:
        #     yield response.follow(next_page, callback=self.parse, meta={'brand_id': brand.id})

        # next_page = response.css('ul.a-pagination li.a-last a::attr(href)').get()
        next_page = response.css('.s-pagination-next::attr(href)').get()
        if next_page:
            next_page_url = urljoin(response.url, next_page)
            yield scrapy.Request(url=next_page_url, callback=self.parse, meta={'brand_id': brand.id})
        else:
            print(f"\n\n\nNo more pages to scrape for brand: {brand.name}\n\n\n")

        # Introduce random sleep to mimic human behavior
        time.sleep(random.uniform(1, 3))

    def parse_product_detail(self, response):
        brand_id = response.meta['brand_id']
        asin = response.meta['asin']
        name = response.meta['name']
        image = response.meta['image']
        brand = Brand.objects.get(id=brand_id)

        # Extract SKU from product detail page
        sku = response.css('#productDetails_detailBullets_sections1 th:contains("Item model number") + td::text').get()
        print("\n\n\nsku: ", sku, "\n\n\n")
        # If the SKU is not found, try another common selector
        if not sku:
            sku = response.css('#productDetails_techSpec_section_1 th:contains("Item model number") + td::text').get()

        # If SKU is still not found, set to None
        sku = sku.strip() if sku else None

        # Update or create the product record in the database
        Product.objects.update_or_create(
            asin=asin,
            defaults={
                'name': name,
                'sku': sku,
                'image': image,
                'brand': brand
            }
        )

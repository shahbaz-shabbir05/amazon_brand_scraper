# from .spiders.amazon_brand_spider import AmazonBrandSpider
import logging

from celery import shared_task

from amazon_spider.amazon_spider.scrapy_runner import run_spider

logger = logging.getLogger(__name__)


@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def scrape_all_brands(self):
    try:
        run_spider()
        logger.info(f"Successfully scraped all brands")
    except Exception as e:
        logger.error(f"Error scraping brands: {str(e)}")
        self.retry(exc=e)

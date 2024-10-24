import logging

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from amazon_spider.amazon_spider.spiders.amazon_brand_spider import AmazonBrandSpider

logger = logging.getLogger(__name__)


def run_spider():
    try:
        process = CrawlerProcess(get_project_settings())
        process.crawl(AmazonBrandSpider)
        process.start()
        logger.info("Successfully scraped all brands.")
    except Exception as e:
        logger.error(f"Error in scraping brands: {e}")
        raise e

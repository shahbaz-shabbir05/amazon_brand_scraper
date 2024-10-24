import os
import sys

import django

# Define the path to the Django project directory
# Adjust the number of os.path.pardir based on your project structure
# Here, '../../../' navigates from scrapy_spiders/amazon_spider/amazon_spider/ to amazon_brand_scraper/
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
sys.path.append(project_root)
# Set the default Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'amazon_scraper.settings')
# Initialize Django
django.setup()

# Scrapy's settings for amazon_spider project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = "amazon_spider"

SPIDER_MODULES = ["amazon_spider.spiders"]
NEWSPIDER_MODULE = "amazon_spider.spiders"

# Crawl responsibly by identifying yourself (and your website) on the user-agent
# import random

# USER_AGENTS = [
#     # Chrome on Windows
#     'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
#     ' Chrome/115.0.0.0 Safari/537.36',
#
#     # Firefox on macOS
#     'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko)'
#     ' Version/15.1 Safari/605.1.15',
#
#     # Safari on iPhone
#     'Mozilla/5.0 (iPhone; CPU iPhone OS 16_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko)'
#     ' Version/16.5 Mobile/15E148 Safari/604.1',
#
#     # Edge on Windows
#     'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
#     ' Chrome/115.0.0.0 Safari/537.36 Edg/115.0.0.0',
#
#     # Opera on Windows
#     'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
#     ' Chrome/115.0.0.0 Safari/537.36 OPR/101.0.0.0',
#
#     # Chrome on Linux
#     'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko)'
#     ' Chrome/115.0.0.0 Safari/537.36',
#
#     # Firefox on Android
#     'Mozilla/5.0 (Android 13; Mobile; rv:116.0) Gecko/116.0 Firefox/116.0',
#
#     # Chrome on macOS
#     'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko)'
#     ' Chrome/115.0.0.0 Safari/537.36',
#
#     # Safari on iPad
#     'Mozilla/5.0 (iPad; CPU OS 16_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko)'
#     ' Version/16.5 Mobile/15E148 Safari/604.1',
#
#     # Chrome on Windows (different version)
#     'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
#     ' Chrome/114.0.0.0 Safari/537.36',
#
#     # Firefox on Windows
#     'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:116.0) Gecko/20100101 Firefox/116.0',
#
#     # Edge on macOS
#     'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko)'
#     ' Chrome/115.0.0.0 Safari/537.36 Edg/115.0.0.0',
# ]

# USER_AGENT = random.choice(USER_AGENT_LIST)

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 8

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also auto throttle settings and docs
DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
# CONCURRENT_REQUESTS_PER_DOMAIN = 2
# CONCURRENT_REQUESTS_PER_IP = 2

# Disable cookies (enabled by default)
# COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
# TELNETCONSOLE_ENABLED = False

# Override the default request headers:
# DEFAULT_REQUEST_HEADERS = {
#    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
#    "Accept-Language": "en",
# }

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
# SPIDER_MIDDLEWARES = {
#    "amazon_spider.middlewares.AmazonSpiderSpiderMiddleware": 543,
# }

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
# DOWNLOADER_MIDDLEWARES = {
#    "amazon_spider.middlewares.AmazonSpiderDownloaderMiddleware": 543,
# }

DOWNLOADER_MIDDLEWARES = {
    'scrapy_user_agents.middlewares.RandomUserAgentMiddleware': 400,
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
    'scrapy.downloadermiddlewares.retry.RetryMiddleware': 90,
    'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 110,
}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
# EXTENSIONS = {
#    "scrapy.extensions.telnet.TelnetConsole": None,
# }

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
# ITEM_PIPELINES = {
#    "amazon_spider.pipelines.AmazonSpiderPipeline": 300,
# }

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
AUTOTHROTTLE_ENABLED = True
# The initial download delay
AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
# HTTPCACHE_ENABLED = True
# HTTPCACHE_EXPIRATION_SECS = 0
# HTTPCACHE_DIR = "httpcache"
# HTTPCACHE_IGNORE_HTTP_CODES = []
# HTTPCACHE_STORAGE = "scrapy.extensions.httpcache.FilesystemCacheStorage"

import scrapy.utils.ossignal

scrapy.utils.ossignal.dont_install = True

# Set settings whose default value is deprecated to a future-proof value
REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
# TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"

RETRY_ENABLED = True
RETRY_TIMES = 3
RETRY_HTTP_CODES = [429, 500, 502, 503, 504]

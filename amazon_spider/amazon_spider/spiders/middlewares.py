from scrapy import signals
import random

from ..settings import USER_AGENTS


class RandomUserAgentMiddleware:
    def process_request(self, request, spider):
        user_agent = random.choice(USER_AGENTS)
        request.headers.setdefault('User-Agent', user_agent)

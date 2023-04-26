import random
from urllib.parse import urlparse

import scrapy
from scrapy_playwright.page import PageMethod

from demo.demo.settings import PLAYWRIGHT_PROXY_SERVERS


class ExampleSpider(scrapy.Spider):
    name = "example"
    allowed_domains = ["example.com"]
    start_urls = ["http://example.com/"]

    def start_requests(self):
        for url in self.start_urls:
            parsed_proxy = urlparse(random.choice(PLAYWRIGHT_PROXY_SERVERS))
            proxy = {
                'server': f"http://{parsed_proxy.hostname}:{parsed_proxy.port}",
                'username': parsed_proxy.username,
                'password': parsed_proxy.password
            }
            yield scrapy.Request(url, callback=self.parse, meta=dict(
                playwright=True,
                # playwright_page_methods={
                #     "evaluate": PageMethod("evaluate", "(function() { return contenidoaguardar; })()"),
                # },
                playwright_context_kwargs={
                    "java_script_enabled": True,
                    "ignore_https_errors": True,
                    "proxy": proxy
                },
                errback=self.close_context_on_error,
                playwright_context=f'{parsed_proxy.hostname}',
            ), )

    async def close_context_on_error(self, failure):
        page = failure.request.meta["playwright_page"]
        await page.context.close()

    def parse(self, response):
        self.logger.info('Crawling link: {}'.format(response.url))
        # ...
        pass
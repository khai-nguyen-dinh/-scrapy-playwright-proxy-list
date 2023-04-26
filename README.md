# scrapy-playwright with proxy list

Create new context base on proxy. Each proxy will be one context.

```python
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
            playwright_context_kwargs={
                "java_script_enabled": True,
                "ignore_https_errors": True,
                "proxy": proxy
            },
            errback=self.close_context_on_error,
            # Create new context for each proxy
            playwright_context=f'{parsed_proxy.hostname}',
            )
        )
```
You can consider to limit playwright context to prevent overloading for your resources. Specify a value for the `PLAYWRIGHT_MAX_CONTEXTS` setting to limit the amount of concurent contexts. Use with caution: it's possible to block the whole crawl if contexts are not closed after they are no longer used (refer to the above section to dinamically close contexts). 
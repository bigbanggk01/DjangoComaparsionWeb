from product_spider import ProductSpider
from scrapy.crawler import CrawlerProcess

class runner():
    def __init__(self,spider,url,items_xpath,url_xpath,name_xpath,price_xpath,image_xpath):
        self.settings = {
            'SPASH_URL': 'http://localhost:8050',
            'DOWNLOADER_MIDDLEWARES' : {
                'scrapy_splash.SplashCookiesMiddleware': 723,
                'scrapy_splash.SplashMiddleware': 725,
                'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 810,
            },
            'SPIDER_MIDDLEWARES' : {
                'scrapy_splash.SplashDeduplicateArgsMiddleware': 100,
            },
            'DUPEFILTER_CLASS' : 'scrapy_splash.SplashAwareDupeFilter',
            'HTTPCACHE_STORAGE' : 'scrapy_splash.SplashAwareFSCacheStorage',
            'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
            'ROBOTSTXT_OBEY' : 'True',
            'BOT_NAME' : 'ProductScrapyBot',
            'DEFAULT_REQUEST_HEADERS' : {
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'en',
            },
            'DOWNLOAD_TIMEOUT' : '180',
            'LOG_ENABLED' : 'True',

        }
        self.process = CrawlerProcess(self.settings)
        self.process.crawl(
            spider,
            url = url,
            items_xpath = items_xpath,
            url_xpath = url_xpath,
            name_xpath = name_xpath,
            price_xpath = price_xpath,
            image_xpath=image_xpath
        )

    def run(self):
        self.process.start()
        
# r = runner(
#     ProductSpider,
#     'https://tiki.vn/search?q=giay+sneaker',
#     '//a[@class="product-item"]',
#     './/@href',
#     './/div[@class="name"]/span/text()',
#     './/div[@class="price-discount__price"]/text()',
#     './/picture[@class="webpimg-container"]/img/@src[1]'
# )
# r = runner(
#     ProductSpider,
#     'https://shopee.vn/search?keyword=dien+thoai+samsung',
#     '//div[@class = "shopee-search-item-result__item"]',
#     './/a[@data-sqe = "link"]/@href',
#     './/div[@data-sqe = "name"]/div/div/text()',
#     './/span[@class = "_1d9_77"/text()',
#     './/div[@class = "customized-overlay-image"]/img/@src[1]',
# )
#r.run()

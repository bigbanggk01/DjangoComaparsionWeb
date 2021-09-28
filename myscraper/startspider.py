from myscraper.spiders import spider
from scrapy.crawler import CrawlerProcess
class runner():
    def __init__(self,urls,items_xpath,url_xpath,name_xpath,price_xpath,image_xpath):
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
            'ROBOTSTXT_OBEY' : 'False',
            'BOT_NAME' : 'Product',
            'DEFAULT_REQUEST_HEADERS' : {
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'en',
            },
            'DOWNLOAD_TIMEOUT' : '180',
            'LOG_ENABLED' : 'False',
        }
        self.process = CrawlerProcess(self.settings)
        self.process.crawl(
            spider.productSpider,
            urls = urls,
            items_xpath = items_xpath,
            url_xpath = url_xpath,
            name_xpath = name_xpath,
            price_xpath = price_xpath,
            image_xpath=image_xpath
        )

    def run(self):
        self.process.start()
        
r = runner(
    [
        ['https://www.lazada.vn/catalog/?q=dien+thoai+nokia', 3]
    ],
    '//div[@data-qa-locator="product-item"]',
    './/a[1]/@href',
    './/a[1]/@title',
    './/span[@class="Q78Jz"]/text()',
    './/a[1]/img/src[1]'
)
r.run()

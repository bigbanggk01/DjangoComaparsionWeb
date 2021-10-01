from myscraper.spiders import spider
from scrapy.crawler import CrawlerRunner
from twisted.internet import reactor
from scrapy.utils.log import configure_logging
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
        self.process = CrawlerRunner(self.settings)
        self.d = self.process.crawl(
            spider.productSpider,
            urls = urls,
            items_xpath = items_xpath,
            url_xpath = url_xpath,
            name_xpath = name_xpath,
            price_xpath = price_xpath,
            image_xpath=image_xpath
        )

    def run(self):
        configure_logging({'LOG_FORMAT': '%(levelname)s: %(message)s'})
        self.d.addBoth(lambda _: reactor.stop())
        reactor.run()
        return 
        


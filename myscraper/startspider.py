from myscraper.spiders import spider
from scrapy.crawler import CrawlerRunner
from twisted.internet import reactor
from scrapy.utils.log import configure_logging
class runner():
    def __init__(self,urls,items_xpath,url_xpath,name_xpath,price_xpath,image_xpath, next_xpath):
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
            'LOG_ENABLED' : 'True',
            'CLOSESPIDER_PAGECOUNT':'50',
        }
        self.process = CrawlerRunner(self.settings)
        self.d = self.process.crawl(
            spider.productSpider,
            urls = urls,
            items_xpath = items_xpath,
            url_xpath = url_xpath,
            name_xpath = name_xpath,
            price_xpath = price_xpath,
            image_xpath=image_xpath,
            next_xpath = next_xpath,
        )

    def run(self):
        configure_logging({'LOG_FORMAT': '%(levelname)s: %(message)s'})
        self.d.addBoth(lambda _: reactor.stop())
        reactor.run()
        return 
        

r = runner(urls=[
        ['https://shopee.vn/search?keyword=dien+thoai+samsung', 2],
        ['https://shopee.vn/search?keyword=dien%20thoai%20samsung&page=1',2],
        ['https://shopee.vn/search?keyword=dien%20thoai%20samsung&page=2',2],
        ['https://shopee.vn/search?keyword=dien%20thoai%20samsung&page=3',2],
        ['https://shopee.vn/search?keyword=dien%20thoai%20samsung&page=4',2],
        ['https://shopee.vn/search?keyword=dien%20thoai%20samsung&page=7',2],
        ['https://shopee.vn/search?keyword=dien%20thoai%20samsung&page=8',2],
        ['https://shopee.vn/search?keyword=dien%20thoai%20samsung&page=9',2],
        ['https://shopee.vn/search?keyword=dien%20thoai%20samsung&page=10',2],
        ['https://shopee.vn/search?keyword=dien%20thoai%20samsung&page=11',2],
        ['https://shopee.vn/search?keyword=dien%20thoai%20samsung&page=12',2],
    ],
    items_xpath='//div[@data-sqe="item"]',
    url_xpath = './/a[@data-sqe="link"]/@href',
    name_xpath ='.//div[@data-sqe="name"]/div[1]/div[1]/text()',
    price_xpath = './/div[@class="zp9xm9"]/text()',
    image_xpath = './/a[@data-sqe="link"]/div[1]/div[1]/div[1]/img/@src[1]',
    next_xpath = '//button[@class="shopee-icon-button shopee-icon-button--right "]'
)

r.run()
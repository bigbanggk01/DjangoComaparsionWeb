from product_spider import ProductSpider
from scrapy.crawler import CrawlerProcess

class runner():
    def __init__(self,spider,url,items_xpath,url_xpath,name_xpath,price_xpath,image_xpath):
        # self.url = url
        # self.items_xpath = items_xpath
        # self.url_xpath = url_xpath
        # self.name_xpath = name_xpath
        # self.price_xpath = price_xpath
        # self.image_xpath = image_xpath
        self.settings = {
            'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
            'ROBOTSTXT_OBEY' : 'True',
            'BOT_NAME' : 'ProductScrapyBot',
            'DEFAULT_REQUEST_HEADERS' : {
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'en',
            },
            'DOWNLOAD_TIMEOUT' : '180',
            'LOG_ENABLED' : 'False',
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
        
r = runner(ProductSpider,
'https://tiki.vn/search?q=dien+thoai+samsung',
'//a[@class="product-item"]',
'//@href',
'//div[@class="name"]/span/text()',
'//div[@class="price-discount__price"]/text()',
'//picture[@class="webpimg-container"]/img/@src[1]')
r.run()
# process = CrawlerProcess(
#     {
#         'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
#         'ROBOTSTXT_OBEY' : 'True',
#         'BOT_NAME' : 'Development bot',
#         'DEFAULT_REQUEST_HEADERS' : {
#             'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#             'Accept-Language': 'en',
#         }
#     }
# )

# process.crawl(ProductSpider,url='https://tiki.vn/search?q=dien+thoai+samsung',
# items_xpath='//a[@class="product-item"]',
# url_xpath='//@href',
# name_xpath='//div[@class="name"]/span/text()',
# price_xpath='//div[@class="price-discount__price"]/text()',
# image_xpath='//picture[@class="webpimg-container"]/img/@src[1]')
# def runScrapy():
#     process.start()

import scrapy
from items import ProductItem

class ProductSpider(scrapy.Spider):
    name = "products"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.url = kwargs['url']
        self.items_xpath = kwargs['items_xpath']
        self.url_xpath = kwargs['url_xpath']
        self.name_xpath = kwargs['name_xpath']
        self.price_xpath = kwargs['price_xpath']
        self.image_xpath = kwargs['image_xpath']
    
    def start_requests(self):
        meta = {
            'items_xpath': self.items_xpath,
            'url_xpath' : self.url_xpath, 
            'name_xpath': self.name_xpath, 
            'price_xpath': self.price_xpath, 
            'image_xpath': self.image_xpath,
            }
        yield scrapy.Request(self.url, callback=self.parse, meta=meta)

    def parse(self, response):
        item = ProductItem()
        products = response.xpath(response.meta['items_xpath'])
        for product in products:
            item['url'] = product.xpath(response.meta['url_xpath']).get()
            print(item['url'])
            item['name'] = product.xpath(response.meta['name_xpath']).get()
            item['price'] = product.xpath(response.meta['price_xpath']).get()
            item['image_link'] = product.xpath(response.meta['image_xpath']).get()
            yield item
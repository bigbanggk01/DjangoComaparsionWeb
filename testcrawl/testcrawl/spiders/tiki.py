import scrapy
from scrapy import signals
from testcrawl.items import TestcrawlItem
import mysql.connector
import json
class productSpider(scrapy.Spider):
    name = "tiki"
    allow_domain = ['tiki.vn']
    urls = ['https://tiki.vn/api/personalish/v1/blocks/categories?block_code=featured_categories&trackity_id=743b4454-fdec-5096-0b9c-11010162879c']
    mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="testscrape"
    )
    mycursor = mydb.cursor()
    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(productSpider, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_closed, signal=signals.spider_closed)
        return spider

    def spider_closed(self, spider):
        self.mycursor.close()
        self.mydb.close()
        spider.logger.info('Spider closed: %s', spider.name)

    def start_requests(self):
        for url in self.urls:
            yield scrapy.Request(url=url, callback=self.parse_category)

    def parse_category(self, response):
        resp = json.loads(response.body)
        items = resp.get('items')
        category_id = []
        product_urls = []
        
        for item in items:
            product_urls.append(f'https://tiki.vn/api/personalish/v1/blocks/listings?limit=48&category={item["id"]}') 

        for i in range(1,3):
            for item in product_urls:
                item = item + f'&page={i}'
        
        for url in product_urls:
            yield scrapy.Request(url=url,callback=self.parse)
        
    def parse(self, response):
        item = TestcrawlItem()
        resp = json.loads(response.body)
        products = resp.get('data')
        for product in products:
            item['url'] = product['url_path']
            item['name'] = product['name']
            item['price'] = product['price']
            item['image_link'] = product['thumbnail_url']
            yield item
            # sql = "INSERT INTO product (url, name, price, image_link) VALUES (%s, %s, %s, %s)"
            # val = (item['url'], item['name'], item['price'], item['image_link'])
            # self.mycursor.execute(sql, val)
            # self.mydb.commit()

    
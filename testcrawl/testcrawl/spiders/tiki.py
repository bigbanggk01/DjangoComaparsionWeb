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

    def spider_closed(self):
        self.mycursor.close()
        self.mydb.close()

    def start_requests(self):
        for url in self.urls:
            yield scrapy.Request(url=url, callback=self.parse_category)

    def parse_category(self, response):
        resp = json.loads(response.body)
        items = resp.get('items')
        tmp_product_urls = []
        product_urls = []
        for item in items:
            tmp_product_urls_item = {}
            tmp_product_urls_item['url'] = f'https://tiki.vn/api/personalish/v1/blocks/listings?limit=48&category={item["id"]}&page='
            tmp_product_urls_item['category'] = item["name"]
            tmp_product_urls.append(tmp_product_urls_item)

        for item in tmp_product_urls:
            for i in range(1,130):
                product_urls_item = {}
                product_urls_item['url'] = item['url']+str(i)
                product_urls_item['category'] = item['category']
                product_urls.append(product_urls_item)
        
        for item in product_urls:
            yield scrapy.Request(url=item['url'],callback=self.parse, meta=item)

    def parse(self, response):
        item = TestcrawlItem()
        resp = json.loads(response.body)
        products = resp.get('data')
        print(response.meta)
        if(products != []):
            for product in products:
                item['url'] = product['url_path']
                item['name'] = product['name']
                item['price'] = product['price']
                item['image_link'] = product['thumbnail_url']
                item['description'] = product['short_description']
                item['brand'] = product['brand_name']
                item['category'] = response.meta['category']
                yield item
                sql = "INSERT INTO product (url, name, price, image_link, description, brand, category) VALUES (%s, %s, %s, %s, %s, %s, %s)"
                val = (item['url'], item['name'], item['price'], item['image_link'], item['description'], item['category'], item['brand'])
                self.mycursor.execute(sql, val)
                self.mydb.commit()

    
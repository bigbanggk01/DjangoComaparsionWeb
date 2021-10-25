import scrapy
from scrapy import signals
from testcrawl.items import TestcrawlItem
import mysql.connector
import json

class productSpider(scrapy.Spider):
    name = "shopee"
    allow_domain = ['shopee']
    urls = ['https://shopee.vn/api/v4/pages/get_homepage_category_list']
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
        items = resp.get('data')
        items = items['category_list']
        tmp_product_urls = []
        product_urls = []
        for item in items:
            tmp_product_urls_item = {}
            tmp_product_urls_item['url'] = f'https://shopee.vn/api/v4/search/search_items?by=relevancy&limit=60&match_id={item["catid"]}&order=desc&page_type=search&scenario=PAGE_OTHERS&version=2&newest='
            tmp_product_urls_item['category'] = item["display_name"]
            tmp_product_urls.append(tmp_product_urls_item)

        for item in tmp_product_urls:
            for i in range(0,2):
                product_urls_item = {}
                product_urls_item['url'] = item['url']+str(i*60)
                product_urls_item['category'] = item['category']
                product_urls.append(product_urls_item)
        
        for item in product_urls:
            yield scrapy.Request(url=item['url'],callback=self.parse, meta=item)

    def parse(self, response):
        item = TestcrawlItem()
        resp = json.loads(response.body)
        products = resp.get('items')
        if(products != []):
            for product in products:
                item['url'] = f'https://shopee.vn/x-i.{product["item_basic"]["shopid"]}.{product["item_basic"]["itemid"]}?sp_atk=2b6a67f8-2a86-4f5e-b25a-12282aaeb4b3'
                item['name'] = product['item_basic']['name']
                item['price'] = str(product['item_basic']['price'])[:-5]
                item['image_link'] = 'https://cf.shopee.vn/file/'+product['item_basic']['image']
                item['category'] = response.meta['category']
                item['brand'] = product['item_basic']['brand']
                yield item
                sql = "INSERT INTO product_shopee (url, name, price, image_link, brand, category) VALUES (%s, %s, %s, %s, %s, %s)"
                val = (item['url'], item['name'], item['price'], item['image_link'], item['brand'], item['category'])
                self.mycursor.execute(sql, val)
                self.mydb.commit()

    
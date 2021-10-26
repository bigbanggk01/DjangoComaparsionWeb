from logging import exception
from time import sleep
import scrapy
from scrapy import signals
from scrapy.http import request
from testcrawl.items import TestcrawlItem
import mysql.connector
import json
import random
from fake_useragent import UserAgent
class productSpider(scrapy.Spider):
    name = "lazada"
    allow_domain = ['lazada.vn']
    urls = ['https://www.lazada.vn/']
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="testscrape"
    )
    mycursor = mydb.cursor()

    def start_requests(self):
        for url in self.urls:
            yield scrapy.Request(url=url, callback=self.parse_category)

    def parse_category(self, response):
        urls = response.xpath('//li[@class="sub-item-remove-arrow"] | //li[@class="lzd-site-menu-sub-item"]')
        tmp_product_urls = []
        product_urls = []

        for url in urls:
            tmp_product_url = {}
            tmp_product_url['url'] = url.xpath('.//a/@href').get()[2:]+f'?ajax=true&page='
            tmp_product_url['category'] = tmp_product_url['url'][14:].replace('-',' ').replace('/','').split("?")[0]
            tmp_product_urls.append(tmp_product_url)

        for item in tmp_product_urls:
            for i in range(0,2):
                product_urls_item = {}
                product_urls_item['url'] = 'https://' + item['url']+str(i)
                product_urls_item['category'] = item['category']
                product_urls.append(product_urls_item)

        for item in product_urls:
            yield scrapy.Request(url=item['url'],callback=self.parse, meta=item)

    def parse(self, response):
        item = TestcrawlItem()
        resp = json.loads(response.body)
        try:
            products = resp.get('mods')['listItems']

            if(products != []):
                for product in products:
                    item['url'] = product['productUrl']
                    item['name'] = product['name']
                    item['price'] = product['price']
                    item['image_link'] = product['image']
                    item['category'] = response.meta['category']
                    item['brand'] = product['brandName']
                    item['description'] = product['description']
                    yield item
                    sql = "INSERT INTO product_shopee (url, name, price, image_link, brand, category) VALUES (%s, %s, %s, %s, %s, %s)"
                    val = (item['url'], item['name'], item['price'], item['image_link'], item['brand'], item['category'])
                    self.mycursor.execute(sql, val)
                    self.mydb.commit()
        except Exception as e:
            body = resp.get('rgv587_flag')
            if(body == 'sm'):
                print('Got some bans')
                print(response.url)
                self.mycursor.execute("INSERT INTO failurl (url) VALUES ('%s')"%response)
                self.mydb.commit()
                sleep(5)
                yield scrapy.Request(url=response.url[3:],callback=self.parse, meta=response.meta)
            else:
                pass            

        

    
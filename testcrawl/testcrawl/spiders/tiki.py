import scrapy
from testcrawl.items import TestcrawlItem
import mysql.connector



class productSpider(scrapy.Spider):
    name = "tiki"
    mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="testscrape"
    )
    mycursor = mydb.cursor()
    def start_requests(self):
        urls = ['https://tiki.vn/nha-cua-doi-song/c1883',]
        
        return [scrapy.Request(url=url, callback=self.parse)
            for url in urls]
            
    def parse(self, response):
        item = TestcrawlItem()
        products = response.xpath('//a[@class="product-item"]')
        if products != []:
            for product in products:
                item['url'] = product.xpath('.//@href').get()
                item['name'] = product.xpath('.//div[@class="name"]/span/text()').get()
                item['price'] = product.xpath('.//div[@class="price-discount__price"]/text()').get()
                item['image_link'] = product.xpath('.//picture[@class="webpimg-container"]/img/@src[1]').get()
                yield item
                print(item)
                sql = "INSERT INTO product (url, name, price, image_link) VALUES (%s, %s, %s, %s)"
                val = (item['url'], item['name'], item['price'], item['image_link'])
                self.mycursor.execute(sql, val)
                self.mydb.commit()
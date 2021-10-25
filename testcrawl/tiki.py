import scrapy
from testcrawl.items import TestcrawlItem
import mysql.connector
from scrapy.crawler import CrawlerProcess

class productSpider(scrapy.Spider):
    name = "tiki"
    count = 2
    mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="testscrape"
    )
    mycursor = mydb.cursor()
    def start_requests(self):
        urls = ['https://tiki.vn/nha-cua-doi-song/c1883?page=1',]
        
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
        if(self.count < 10):
            newresponse = response.url[:-7] + f'?page={self.count}'
        elif(self.count >= 10):
            newresponse = response.url[:-8] + f'?page={self.count}'
        next_page_link = newresponse
        print(next_page_link)
        self.count += 1
        yield scrapy.Request(url=next_page_link, callback=self.parse)
            
process = CrawlerProcess(settings={
    'ROBOTSTXT_OBEY' : False,
    'DOWNLOAD_DELAY' : 5,
    'USER_AGENT' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36',
    'HTTPCACHE_ENABLED' : False,
    'FEED_URI':'test.csv',
    'FEED_FORMAT':'csv',
})
process.crawl(productSpider)
process.start()
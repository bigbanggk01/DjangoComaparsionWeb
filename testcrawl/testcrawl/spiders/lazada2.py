from logging import exception
from time import sleep
import scrapy
from scrapy import signals
from scrapy.http import request
from testcrawl.items import TestcrawlItem
import mysql.connector
import json
from scrapy_splash import SplashRequest

class productSpider(scrapy.Spider):
    name = "splashlazada"
    allow_domain = ['lazada.vn']
    urls = ['https://www.lazada.vn/']
    script_1 = """
    function main(splash)
        splash:init_cookies(splash.args.cookies)
        local num_scrolls = 10
        local scroll_delay = 1
        local scroll_to = splash:jsfunc("window.scrollTo")
        local get_body_height = splash:jsfunc(
            "function() {return document.body.scrollHeight;}"
        )
        assert(splash:go(splash.args.url))
        splash:wait(splash.args.wait)
        for _ = 1, num_scrolls do
            local height = get_body_height()
            for i = 1, 10 do
                scroll_to(0, height * i/10)
                splash:wait(scroll_delay/10)
            end
        end        
        return {
            cookies = splash:get_cookies(),
            html = splash:html(),
        }
    end
    """

    name = "lazada2"
    allow_domain = ['lazada.vn']
    urls = ['https://www.lazada.vn/']
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
        urls = response.xpath('//li[@class="sub-item-remove-arrow"] | //li[@class="lzd-site-menu-sub-item"]')
        tmp_product_urls = []
        product_urls = []

        for url in urls:
            tmp_product_url = {}
            tmp_product_url['url'] = url.xpath('.//a/@href').get()[2:]
            tmp_product_url['category'] = tmp_product_url['url'][14:].replace('-',' ').replace('/','').split("?")[0]
            tmp_product_urls.append(tmp_product_url)

        for item in tmp_product_urls:
            for i in range(0,2):
                product_urls_item = {}
                product_urls_item['url'] = 'https://' + item['url'] +"?page="+str(i)
                product_urls_item['category'] = item['category']
                product_urls.append(product_urls_item)

        for item in product_urls:
            yield SplashRequest(url=item['url'],callback=self.parse, meta=item)

    def parse(self, response):
        item = TestcrawlItem()
        products = response.xpath('//div[@data-qa-locator="product-item"]')
        if products != []:
            for product in products:
                item['url'] = product.xpath('.//a[1]/@href').get()
                item['name'] = product.xpath('.//a[1]/@title').get()
                item['price'] = product.xpath('.//span[@class="Q78Jz"]/text()').get()
                item['image_link'] = product.xpath('.//a[1]/img/src[1]').get()
                yield item
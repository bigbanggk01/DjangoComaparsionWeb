import scrapy
from myscraper.items import MyscraperItem
from scrapy_splash import SplashRequest

class productSpider(scrapy.Spider):
    name = "products"
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
    script_2 = """
    function main(splash)
        splash:init_cookies(splash.args.cookies)
        local url = splash.args.url
        assert(splash:go(url))
        splash:wait(splash.args.wait)
        return {
            cookies = splash:get_cookies(),
            html = splash:html(),
        }
    end
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.urls = kwargs['urls']
        self.items_xpath = kwargs['items_xpath']
        self.url_xpath = kwargs['url_xpath']
        self.name_xpath = kwargs['name_xpath']
        self.price_xpath = kwargs['price_xpath']
        self.image_xpath = kwargs['image_xpath']
        self.next_xpath = kwargs['next_xpath']
        print('spider start successfully')

    def start_requests(self):
        meta = {
            'items_xpath': self.items_xpath,
            'url_xpath' : self.url_xpath, 
            'name_xpath': self.name_xpath, 
            'price_xpath': self.price_xpath, 
            'image_xpath': self.image_xpath,
            'next_xpath' : self.next_xpath,
            }
        for url in self.urls:
            if url[1] == 1:
                yield scrapy.Request(url[0], callback=self.parse, meta=meta)
                
            elif url[1] == 2:
                yield SplashRequest(url[0], self.parse, endpoint='execute',
                                args={'wait':2,'lua_source': self.script_1},meta=meta)
            elif url[1] == 3:
                yield SplashRequest(url[0], self.parse, endpoint='execute',
                                args={'wait':2,'lua_source': self.script_2},meta=meta)
            
    def parse(self, response):
        item = MyscraperItem()
        products = response.xpath(response.meta['items_xpath'])
        if products != []:
            for product in products:
                item['url'] = product.xpath(response.meta['url_xpath']).get()
                item['name'] = product.xpath(response.meta['name_xpath']).get()
                item['price'] = product.xpath(response.meta['price_xpath']).get()
                item['image_link'] = product.xpath(response.meta['image_xpath']).get()
                yield item
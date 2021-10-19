import scrapy
from testcrawl.items import TestcrawlItem
from scrapy_splash import SplashRequest
class productSpider(scrapy.Spider):
    name = "shopee"
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
    # script_2 = """
    # function main(splash)
    #     splash:init_cookies(splash.args.cookies)
    #     local url = splash.args.url
    #     assert(splash:go(url))
    #     splash:wait(splash.args.wait)
    #     return {
    #         cookies = splash:get_cookies(),
    #         html = splash:html(),
    #     }
    # end
    # """
    def start_requests(self):
        urls = ['https://shopee.vn/Th%E1%BB%9Di-Trang-Nam-cat.11035567',]
        
        for url in urls:
            yield SplashRequest(url, self.parse, endpoint='execute', args={'wait':10,'lua_source': self.script_1})
            
    def parse(self, response):
        item = TestcrawlItem()
        f = open('shopee.xpath','r')
        xpath = []
        for line in enumerate(f):
            xpath.append(line[1].strip())
        f.close()
        products = response.xpath(xpath[1])
        if products != []:
            for product in products:
                item['url'] = product.xpath(xpath[2]).get()
                item['name'] = product.xpath(xpath[3]).get()
                item['price'] = product.xpath(xpath[4]).get()
                item['image_link'] = product.xpath(xpath[5]).get()
                yield item
                print(item)
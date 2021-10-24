import scrapy
from testcrawl.items import TestcrawlItem
from scrapy_splash import SplashRequest
class productSpider(scrapy.Spider):
    name = "lazada"
    script = """
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
    def start_requests(self):
        urls = ['https://www.lazada.vn/tai-nghe-nhet-tai/?spm=a2o4n.home.categories.10.1905e182E94egw&up_id=290738102&clickTrackInfo=236599f3-eab7-4a21-a875-1e8cd2414be9__4585__290738102__static__0.0985132925088989__158075__7253&from=hp_categories&item_id=290738102&version=v2',
        'https://www.lazada.vn/tai-nghe-nhet-tai/?clickTrackInfo=236599f3-eab7-4a21-a875-1e8cd2414be9__4585__290738102__static__0.0985132925088989__158075__7253&from=hp_categories&item_id=290738102&page=2&spm=a2o4n.home.categories.10.1905e182E94egw&up_id=290738102&version=v2',
        'https://www.lazada.vn/thoi-trang-giay-cho-be-trai/?spm=a2o4n.home.cate_9.6.3675e182WAsqQQ',
        ]
        
        for url in urls:
            yield SplashRequest(url, self.parse, endpoint='execute', args={'wait':5,'lua_source': self.script_1})
            
    def parse(self, response):
        item = TestcrawlItem()
        # f = open('shopee.xpath','r')
        # xpath = []
        # for line in enumerate(f):
        #     xpath.append(line[1].strip())
        # f.close()
        products = response.xpath('//div[@data-qa-locator="product-item"]')
        if products != []:
            for product in products:
                item['url'] = product.xpath('.//a[1]/@href').get()
                item['name'] = product.xpath('.//a[1]/@title').get()
                item['price'] = product.xpath('.//span[@class="Q78Jz"]/text()').get()
                item['image_link'] = product.xpath('.//a[1]/img/src[1]').get()
                yield item
                print(item)
import scrapy
from scrapy_splash import SplashRequest

script = """
function main(splash)
    splash:init_cookies(splash.args.cookies)

    local num_scrolls = 10
    local scroll_delay = 1.0

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
        html = splash:html()
    }
end
"""
script2 = """
function main(splash)
    splash:init_cookies(splash.args.cookies)
    local url = splash.args.url
    assert(splash:go(url))
    splash:wait(splash.args.wait)

    return {
        cookies = splash:get_cookies(),
        html = splash:html()
    }
end
"""
class productSpider(scrapy.Spider):
    name='product_spider'
    allowed_domains = ['shopee.vn']

    start_urls =['https://shopee.vn/search?keyword=dien%20thoai%20samsung']
    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url, self.parse, endpoint='execute',
                                args={'wait':2,'lua_source': script})

    def parse(self, response):
        items = response.xpath('//div[@data-sqe="item"]')
        getitem={}
        for item in items:
            getitem['link'] = item.xpath('.//a[@data-sqe="link"]/@href').get()
            getitem['name'] = item.xpath('.//div[@data-sqe="name"]/div[1]/div[1]/text()').get()
            yield getitem
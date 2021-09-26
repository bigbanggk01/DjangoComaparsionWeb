import scrapy
from scrapy.selector import Selector

class ProductSpider(scrapy.Spider):
    name = "products"
    def start_requests(self):
        meta = {'items_xpath': f'{self.items_xpath}','url_xpath' : f'{self.url_xpath}', 'name_xpath': f'{self.name_xpath}', 
        'price_xpath': f'{self.price_xpath}', 'image_xpath': f'{self.image_xpath}'}
        yield scrapy.Request(f'{self.url}', callback=self.parse, meta=meta)

    def parse(self, response):
        items_xpath = response.meta['items_xpath']
        url_xpath= response.meta['url_xpath']
        name_xpath = response.meta['name_xpath']
        price_xpath = response.meta['price_xpath']
        image_xpath = response.meta['image_xpath']
        items = Selector(response).xpath(items_xpath).extract()
        print(name_xpath)
        list_of_dictionary = []
        for item in items:
            dictionary = {}
            dictionary['url'] = Selector(text=item).xpath(url_xpath).get()
            dictionary['name'] = Selector(text=item).xpath(name_xpath).get()
            dictionary['price'] = Selector(text=item).xpath(price_xpath).get()
            dictionary['image'] = Selector(text=item).xpath(image_xpath).get()
            list_of_dictionary.append(dictionary)
        for dictionary in list_of_dictionary:
            print(dictionary)
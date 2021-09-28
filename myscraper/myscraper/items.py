# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class MyscraperItem(scrapy.Item):
    url =scrapy.Field()
    name = scrapy.Field()
    price = scrapy.Field()
    image_link = scrapy.Field()

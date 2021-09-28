from scrapy.item import Item, Field

class ProductItem(Item):
    url = Field()
    name = Field()
    price = Field()
    image_link = Field()
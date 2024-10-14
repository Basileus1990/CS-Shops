'''
About: Item for storing the scraped product info from the Star Trek shop (https://shop.startrek.com)
    Gathered and created by the CSSpider.
    Can be used in the StarTrekShopPipeline and StarTrekProductImagesPipeline to process and save the scraped data
Author: Marek Szymański
'''


# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class StarTrekShopItem(scrapy.Item):
    '''
    Item for storing the scraped product info from the Star Trek shop (https://shop.startrek.com)

    Fields:
    - category - product category
    - subcategory - product subcategory
    - name - product name
    - price - product price in USD
    - id - product id
    - description_text - main paragraph of product description
    - description_list - list of specific product characteristics from it's description
    - *colors - available colors
    - *sizes - available sizes
    - image_urls - urls of the images of the product
    - **images - downloaded images of the product
    (* - optional fields, mostly used on clothing products
    (** - images are downloaded by the StarTrekProductImagesPipeline)
    '''

    # meta info about the product
    category = scrapy.Field()
    subcategory = scrapy.Field()

    # basic info
    name = scrapy.Field()
    price = scrapy.Field()
    id = scrapy.Field()
    description_text = scrapy.Field()
    description_list = scrapy.Field()

    # images
    image_urls = scrapy.Field()
    images = scrapy.Field()

    # optional fields
    colors = scrapy.Field()
    sizes = scrapy.Field()

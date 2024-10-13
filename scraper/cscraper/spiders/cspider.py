'''
About: Spider for the Star Trek shop website (https://shop.startrek.com).
    It scrapes the website for it's products, categories and subcategories.
    It yields each product as a StarTrekShopItem for further processing by the StarTrekShopPipeline and StarTrekProductImagesPipeline,
    Additionally, the categories and subcategories are dumped to a json file - categories_list.json.
Author: Marek Szymański
'''

import scrapy
import json
import re
import logging
import os

from cscraper.startrek_paths import *
from cscraper.items import StarTrekShopItem
from cscraper.utils import get_dump_path
from cscraper.settings import DATA_PATH, FLATTEN

class CSSpider(scrapy.Spider):
    '''
    Spider for the Star Trek shop website (https://shop.startrek.com).
    It scrapes the website for it's products, categories and subcategories.
    From each product it's name, price, id, description, images (and optionally available colors and sizes) are extracted.
    Each product is yielded as a StarTrekShopItem for further processing by the StarTrekShopPipeline and StarTrekProductImagesPipeline,
    while the categories and subcategories are dumped to a json file.

    Run with: `scrapy crawl cshop`
    use `-a dump_path=your_path` to specify the path for the scraped data dumps (default is './dumps/')
    '''
    name = "cscraper"
    start_urls = ["https://shop.startrek.com",]
    count = 0

    def parse(self, response):
        '''
        Parse the main page of the shop, 
        building and saving a list of categories and subcategories,
        and visit each subcategory page afterwards.
        '''

        self.log_page(response.url)

        # Read categories and subcategories and dump them to a file
        categories_list = self.read_categories(response.xpath(X_TOP_CATEGORIES_LIST))
        categories_path = get_dump_path(DATA_PATH, FLATTEN)
        os.makedirs(categories_path, exist_ok=True)
        json.dump(categories_list, open(categories_path + "categories_list.json", 'w'), indent=2)

        # Visit all the subcategories
        for top in categories_list:
            for sub in top['subcategories']:
                yield response.follow(
                    sub['link'], 
                    self.parse_subcategory, 
                    meta={
                        "category": top['name'],
                        "subcategory": sub['name'],
                    }
                )

    def read_categories(self, top_categories: scrapy.selector.unified.SelectorList):
        '''
        Read the categories and subcategories from the response
        
        Args:
            top_categories (scrapy.selector.unified.SelectorList): selector list of top categories
        
        Returns:
            categories_list: list of json-like dictionaries of categories and subcategories        
        '''
        return [
            {
                "name": top.xpath(X_CATEGORY_ITEM_NAME).get(),
                "link": top.xpath(X_CATEGORY_ITEM_LINK).get(),
                "subcategories": [
                    {
                        "name": sub.xpath(X_CATEGORY_ITEM_NAME).get(),
                        "link": sub.xpath(X_CATEGORY_ITEM_LINK).get(),
                    }
                    for sub in top.xpath(X_SUB_CATEGORIES_LIST)
                ]
            }
            for top in top_categories if top.css("ul")
        ]

    def parse_subcategory(self, response):
        '''
        Parse a single subcategory page, visit all the products and go to the next page if available.
        '''

        self.log_page(response.url)

        # visit all the products
        product_page_links = response.css(C_PRODUCT_PAGE_LINK)[:3]
        yield from response.follow_all(product_page_links, self.parse_product, meta=response.meta)

        # go to the next page 
        next_page = response.xpath(X_NEXT_SUBCATEGORY_PAGE_LINK).get()
        if next_page:
    	    yield response.follow(next_page, self.parse_subcategory, meta=response.meta)

    def parse_product(self, response):
        '''
        Parse a single product page and yield the product as items.StarTrekShopItem.
        '''

        self.log_page(response.url)

        yield self.build_item(response)

    def build_item(self, response):
        '''
        Extract the item from the response
        '''

        def extract_text_from_p(p_selector):
            '''
            Extract text from a p element, removing any html tags
           
            Args:
                p_selector (scrapy.selector.unified.Selector): selector of the p element
           
            Returns:
                p_text (str): text extracted from the p element
           '''

            return re.sub(r'<.*?>', '', p_selector.get())
        
        def extract_text_from_ul(ul_selector):
            '''
            Extract text from a ul element, removing any html tags
            and recursively extracting text from nested ul elements

            Args:
                ul_selector (scrapy.selector.unified.Selector): selector of the ul element

            Returns:
                contents: list of lists of strings (and possibly further lists for nested ul elements) 
                containing the text of the ul's li elements
            '''

            return [extract_text_from_li(li) for li in ul_selector.xpath('li') if li] if ul_selector else []
        
        def extract_text_from_li(li_selector):
            '''
            Extract text from a li element, removing any html tags,
            and recursively extracting text from nested ul elements.

            Args:
                li_selector (scrapy.selector.unified.Selector): selector of the li element

            Returns:
                contents: list of strings (and possibly further lists for nested ul elements)
                containing the text of the li element
            '''
            text = li_selector.xpath('text()').get() if li_selector else ""
            contents = [text.strip()] if text else []
            # contents= [(li_selector.xpath('text()').get().strip())] if li_selector else []
            nested_ul = li_selector.xpath('ul')
            if nested_ul:
                contents.append(extract_text_from_ul(nested_ul))
            return contents

        category = response.meta.get('category')
        subcategory = response.meta.get('subcategory')

        name = response.css(C_PRODUCT_NAME).get()
        price = response.css(C_PRODUCT_PRICE).get()
        id = response.css(C_PRODUCT_ID).get()
        colors = response.xpath(X_PRODUCT_COLORS).getall()
        sizes = response.xpath(X_PRODUCT_SIZES).getall()
        description_text = response.css(C_PRODUCT_DESC_TEXT)
        description_list = response.xpath(X_PRODUCT_DESC_UL)
        image_urls = response.css(C_PRODUCT_IMAGE_SRC).getall()

        item = StarTrekShopItem()
        item['category'] = category           
        item['subcategory'] = subcategory
        item['name'] = name.strip() if name else ""
        item['price'] = price.replace("$", "") if price else ""
        item['id'] = id if id else ""
        item['colors'] = colors if colors else []
        item['sizes'] = sizes if sizes else []
        item['description_text'] = extract_text_from_p(description_text) if description_text else ""
        item['description_list'] = extract_text_from_ul(description_list[0]) if description_list else []
        item['image_urls'] = list(set(image_urls)) if image_urls else []
        item['images'] = []
        
        return item

    def log_page(self, url):
        '''
        Log (at INFO level) the current page url and increment the counter
        '''
        self.count += 1
        logging.log(logging.INFO, f"|{self.count}| Spider on: {url}")

'''
About: Item pipelines for processing and saving products from shop.startrek.com
    - StarTrekProductPipeline - saves the product info to a json file
    - StarTrekProductImagesPipeline - downloads the product images
    both pipelines use cscraper.items.StarTrekShopItem 
    and save the data in the same directory
Author: Marek Szymański
'''


import os
import json
import logging
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem
from scrapy import Request

from cscraper.items import StarTrekShopItem
from cscraper.utils import get_dump_path
from cscraper.settings import DATA_PATH, FLATTEN
    

class StarTrekProductPipeline:
    '''
    Pipeline for processing the scraped StarTrekShopItem items.
    It saves the item's info to a json file in the corresponding directory.

    The directory structure is as follows:
    - *dumps/
        - category/
            - subcategory/
                - product_name/
                    - info.json
    * - root directory can be specified in the spider's dump_path attribute

    The info.json file contains the following fields:
    - name - product name
    - price - product price in USD
    - id - product id
    - description_text - main paragraph of product description
    - description_list - list of specific product characteristics from it's description
    - *colors - available colors
    - *sizes - available sizes
    - image_urls - urls of the images of the product
    (* - optional fields, mostly used on clothing products)
    '''

    def process_item(self, item: StarTrekShopItem, spider):
        '''
        Process the scraped item, save it's info to a json file in the corresponding directory.
        Creates the directory structure if it doesn't exist.
        '''

        product_dir_path = get_dump_path(DATA_PATH, FLATTEN, item)
        os.makedirs(product_dir_path, exist_ok=True)

        info_path = os.path.join(product_dir_path, 'info.json')
        with open(info_path, 'w') as f:
            json.dump({
                "name": item['name'],
                "price": item['price'],
                "id": item['id'],
                "description_text": item['description_text'],
                "description_list": item['description_list'],
                "colors": item['colors'],
                "sizes": item['sizes'],
                "image_urls": item['image_urls'],
            }, f, indent=2)

        return item


class StarTrekProductImagesPipeline(ImagesPipeline):
    '''
    Pipeline for downloading the images of the scraped StarTrekShopItem items.
    It saves the images in the corresponding directory.
    Supports multiple images per product.
    
    The directory structure is as follows:
    - *dumps/
        - category/
            - subcategory/
                - product_name/
                    - image.jpg (for example)
    * - root directory can be specified in the spider's dump_path attribute

    The images are named after their url's name part.
    '''

    def get_media_requests(self, item: StarTrekShopItem, info):
        '''
        Create a request for each image url of the item.
        '''

        if item['image_urls']:
            for image_url in item['image_urls']:
                image_url = "https:" + image_url
                yield Request(image_url, meta={'item': item, 'image_url': image_url})
        else:
            raise DropItem("Missing image URLs in %s" % item)

    def file_path(self, request, response=None, *, info=None, item: StarTrekShopItem = None):
        '''
        Define the path for the downloaded image.
        '''

        item = request.meta['item']
        image_url = request.meta['image_url']
        image_guid = image_url.split('/')[-1].split('?')[0]  # Use the last part of the URL as the filename and skip the query part
        img_path = get_dump_path(DATA_PATH, FLATTEN, item) + image_guid
        return img_path

    def item_completed(self, results, item, info):
        '''
        Log the failed downloads.
        '''
        
        for ok, x in results:
            if not ok and x['status'] != 'completed':
                logging.error("Failed to download image %s for item %s", x['url'], item['name'])
        return item

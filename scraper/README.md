# CS-Scraper - The web scraper for CS-Shop
### Author: Marek Szymański
This is a web written scraper for E-Commerce course at GUT.  
It targets the official StarTrek shop (https://shop.startrek.com) and scrapes the product data from it.  
It is written in Python, using mainly Scrapy and Pillow modules.  

## Requirements
- Python 3.10
- Scrapy 2.11.2
- Pillow 10.4.0

## Installation
Clone this repository, create venv and run:
```
pip install -r requirements.txt
```

## Usage
To run the scraper, execute the following command:
```
scrapy crawl csscraper
```

## Output
The output will be placed in directory specified in `DATA_PATH` in `csraper/settings.py`, in the following format:

For each product, a directory will be created, containing:
- `info.json` - a JSON file with the product data
'''
{
    "category": "Product category",
    "subcategory": "Product subcategory",

    "name": "Product name",
    "price": "Product price in USD",
    "id": "Product ID",
    "description_text": "Product description",
    "description_list": "List of specific product characteristics from it's description",

    *"colors": ["Color1", "Color2", ...],
    *"sizes": ["Size1", "Size2", ...],

    "image_urls": ["URL to the product image", ...]
}
(* - optional fields, empty for products without color/size options)
'''
- `image1.jpg`, `image2.jpg`, ... - images of the product


## Options
In the `csraper/settings.py` file, you can set the following options:
- `DATA_PATH` - the path to the directory where the scraped data will be saved
- `FLATTEN` - if set to `False`, the data will be saved in a nested directory structure, mirroring the categories and subcategories of the shop, otherwise all products will be saved in a single directory. Default is `False`
> Default (nested) directory structure:
```
DATA_PATH
├── category1
│   ├── subcategory1
│   │   ├── product1
|   |   |   ├── info.json
|   |   |   ├── image1.jpg
|   |   |   ├── image2.jpg
|   |   |   └── ...
│   │   ├── product2
│   │   └── ...
│   └── ...
└── ...
```
> Flattened directory structure:
```
DATA_PATH
├── product1
|   ├── info.json
|   ├── image1.jpg
|   └── ...
├── product2
└── ...
```




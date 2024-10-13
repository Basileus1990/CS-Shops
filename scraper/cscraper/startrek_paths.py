'''
About: Selector paths for the accesing various elements of Star Trek shop website (https://shop.startrek.com) spider.
    Used by the CSSpider to scrape the website.
    Path markers explanation:
        - 'URL_' is for web urls
        - 'X_' is for XPATH expressions
        - 'C_' is for CSS selectors
Author: Marek Szymański
'''


# URLs
URL_MAIN = "https://shop.startrek.com"


# categories (and subcategories) and their details
X_TOP_CATEGORIES_LIST = "//li[a/span/span[text()='Shop by Product']]/ul/div/li"
X_SUB_CATEGORIES_LIST = "ul/li"                                             # from each item of top_categories_list
X_CATEGORY_ITEM_NAME = "a/span/text()"                                      # from each item of top_categories_list or sub_categories_list
X_CATEGORY_ITEM_LINK = "a/@href"                                            # from each item of top_categories_list or sub_categories_list


# subcategory page
C_PRODUCT_PAGE_LINK = "div.card__inner a.full-unstyled-link::attr(href)"    # links to specific product pages
X_NEXT_SUBCATEGORY_PAGE_LINK = "//a[@aria-label='Next page']/@href"         # link to the next page of the subcategory
                                                                            # (won't be available if there's only one page)


# product page
# always available
C_PRODUCT_NAME = "h1::text"                                                 
C_PRODUCT_PRICE = "span.price-item::text"                                   # the format is $XX.XX as string
C_PRODUCT_ID = "span.product-sku::text"                                                  
# description is divided into 1 paragraph and 1 list of characteristics
C_PRODUCT_DESC_TEXT = "div.product__description p"                          # main part of the description
X_PRODUCT_DESC_UL = "//div[@class='product__description rte']/ul"           # some listed characteristics, may contain deeper lists

# not always available fields
X_PRODUCT_COLORS = "//input[@name='Color']/@value"  
X_PRODUCT_SIZES = "//input[@name='Size']/@value"    

# images
C_PRODUCT_IMAGE_SRC = "slider-component img::attr(src)"                     # only the images of this specific product


'''
About: Utility functions for the cscraper package
Author: Marek Szymański
'''

import os

def get_dump_path(base_path: str, flatten: bool = False, item: dict = None):
    '''
    Get the path for the scraped data dumps
    
    Args:
        base_path (str): the base path for the dumps
        flatten (bool): whether or not to flatten the directory structure
        item (dict): the item to get the path for
    
    Returns:
        dump_path (str): the path for the scraped data dumps
    '''

    if item is not None:
        # if an item is provided, return the path for the item's category and subcategory or the general dump path
        if flatten:
            return base_path + '/' + item['name'] + '/'
        else:
            return os.path.join(base_path, item['category'], item['subcategory'], item['name']) + '/'
    else:
        return base_path + '/'
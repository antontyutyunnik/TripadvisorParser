import re

import lxml.html
import tqdm
from lxml.cssselect import CSSSelector
from bs4 import BeautifulSoup as bs
from tqdm import tqdm as progress

class  Restaurants_parser:

    def get_urls_restoraunts_from_cities(self, urls):
        city_parsed = urls[2]

        if city_parsed == 1:
            return







    def parsed_restaurants(self, urls, server):
        check = self.get_urls_restoraunts_from_cities(urls)
        print(check)




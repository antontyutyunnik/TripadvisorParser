import re

import lxml.html
import tqdm
from lxml.cssselect import CSSSelector
from bs4 import BeautifulSoup as bs
from tqdm import tqdm as progress
from lxml.html.clean import Cleaner


class Restaurants_parser:

    def get_unparsed_cities_url(self, cities):

        list = []
        for city in cities:
            parsed = city[2]
            if parsed == 0:
                list.append(city)
        return list


    def get_pagination(self, server, urls):
        base_url = 'https://www.tripadvisor.de'
        list = []
        resp = server.get(urls[1])
        tree = lxml.html.fromstring(resp.text)
        sel = CSSSelector('#EATERY_LIST_CONTENTS > div.deckTools.btm > div > div > :last-child')

        pageNum = sel(tree)

        if len(pageNum) != 0:
            count_of_page = pageNum[0].get('data-page-number')
            dynamic_url = pageNum[0].get('href')
        else:
            list.append(urls[1])
            return list


        page_numbers = range(0, int(count_of_page), 1)
        for page in tqdm.tqdm(page_numbers):
            link_number = int(page) * 30
            dynamic_url = re.sub(r"-oa\d*", "-oa" + str(link_number), dynamic_url)
            list.append(base_url + dynamic_url)
        return list

    def remove_marketing(self, tree):
        marketing_sel = CSSSelector('#component_2 > div > div:nth-child(1) > div.restaurants-list-ListCell__cellWrapper'
                                    '--1htQm > div.restaurants-list-ListCell__infoWrapper--3agHz > div.restaurants-list'
                                    '-ListCell__titleRow--3rRCX.ui_columns.is-gapless.is-mobile.is-multiline > div:nth'
                                    '-child(1) > div > div > div')
        marketing = marketing_sel(tree)

        for elem in marketing:
            child = elem.getparent().getparent().getparent().getparent().getparent().getparent()
            parent = child.getparent()
            parent.remove(child)

        return tree

    def get_urls(self, city, server):
        base_url = 'https://www.tripadvisor.de'
        link = 'Folse'
        href = []
        city_id = city[0]
        parsed = 0

        pagination = self.get_pagination(server, city)

        for page in tqdm.tqdm(pagination):
            resp = server.get(page)
            tree = lxml.html.fromstring(resp.text)
            tree = self.remove_marketing(tree)

            foto_sel = CSSSelector(
                '#component_2 > div > div > div.restaurants-list-ListCell__cellWrapper--1htQm > div.'
                'restaurants-list-ListCell__photoWrapper--1umtU > span > a > div')

            foto_list = foto_sel(tree)

            # if not foto_list:
                # href.append({'link': link, 'parsed': parsed, 'cityID': city_id})
                # return
            # else:

            for foto in foto_list:
                a_elem = foto.getparent()
                href.append({
                    'link': base_url + a_elem.get('href'),
                    'parsed': parsed,
                    'cityID': city_id
                })

        return href








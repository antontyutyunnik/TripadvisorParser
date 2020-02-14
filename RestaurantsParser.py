import re
from db import *
from Server import *
import lxml.html
import tqdm
from lxml.cssselect import CSSSelector
from multiprocessing import Pool
from functools import partial

class Restaurants_parser:

    def get_unparsed_cities_url(self, cities):

        list = []
        for city in cities:
            parsed = city[3]
            id = city[0]
            if parsed == 0:
                # if id == 1:
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
        marketing_sel = CSSSelector('#component_2 > div > div> span > div._1kNOY9zw > div._2Q7zqOgW > div._2kbTRHSI > div._1j22fice > div > div')
        marketing = marketing_sel(tree)

        for elem in marketing:
            child = elem.getparent().getparent().getparent().getparent().getparent()
            parent = child.getparent()
            parent.remove(child)

        return tree

    def get_urls(self,city_id, page):
        server = Server()
        base_url = 'https://www.tripadvisor.de'
        link = 'Folse'
        href = []
        parsed = 0

        resp = server.get(page)
        tree = lxml.html.fromstring(resp.text)
        tree = self.remove_marketing(tree)

        foto_sel = CSSSelector(
            '#component_2 > div > div > span > div._1kNOY9zw > div._2jF2URLh > span > a')
        foto_list = foto_sel(tree)

        for foto in foto_list:
            a_elem = foto
            href.append({
                'link': base_url + a_elem.get('href'),
                'parsed': parsed,
                'cityID': city_id
            })
        return href

    def start_get_urls(self, city, server):
        city_id = city[0]

        pagination = self.get_pagination(server, city)

        func = partial(self.get_urls, city_id)

        with Pool(20) as pool:
            href = list(tqdm.tqdm(pool.imap(func, pagination)))
        pool.close()
        pool.join()

        for len_num in href:
            if len(len_num) == 0:
                return None

        return href
import lxml.html
from lxml.cssselect import CSSSelector
from bs4 import BeautifulSoup as bs
from tqdm import tqdm as progress

class Cities_parser:

    def get_urls_from_front_page(self, response):
        lxml = bs(response.content, 'lxml')
        cities = lxml.find_all('div', attrs={'class': 'geo_name'})

        list = []
        base_url = 'https://www.tripadvisor.de'
        parsed = 0

        for city in cities:
            link = city.find('a', href=True)['href']
            city_name = city.find('a').text
            city_name = city_name.replace('Restaurants ', '')
            list.append({
                'link': base_url + link,
                'city_name': city_name,
                'parsed': parsed
            })
        return list

    def get_pagination(self, server, url):

        resp = server.get(url)
        tree = lxml.html.fromstring(resp.text)
        sel = CSSSelector('#SDTOPDESTCONTENT > div.deckTools.btm > div > div > :last-child')

        pageNum = sel(tree)

        if len(pageNum) != 0:
            count_of_page = pageNum[0].get('data-page-number')
        else:
            count_of_page = 1

        page_numbers = range(0, int(count_of_page), 1)
        for page in page_numbers:
            link_number = int(page) * 20

        return link_number

    def generate_pagination(self, get_pagination):

        count = get_pagination
        urls = []
        for i in progress(range(20, count, 20)):
            url = 'https://www.tripadvisor.de/Restaurants-g187275-oa{}-Germany.html#LOCATION_LIST'.format(i)
            urls.append(url)
        return urls


    def get_urls_from_pagination(self, server, pagination):
        list = []
        for url in progress(pagination):
            base_url = 'https://www.tripadvisor.de'
            parsed = 0

            response = server.get(url)
            response_in_lxml = bs(response.content, 'lxml')

            cities = response_in_lxml.find_all('ul', attrs={'class': 'geoList'})
            for city in cities:
                for li in city.find_all('li'):
                    link = li.find('a', href=True)['href']
                    city_name = li.find('a').text
                    city_name = city_name.replace('Restaurants ', '')
                    list.append({
                        'link': base_url + link,
                        'city_name': city_name,
                        'parsed': parsed
                    })
        return list



    def get_city_urls(self, server):
        url = 'https://www.tripadvisor.de/Restaurants-g187275-oa{page_num}-Germany.html#LOCATION_LIST'
        response = server.get(url)
        city_urls_front = self.get_urls_from_front_page(response)
        get_pagination = self.get_pagination(server, url)
        pagination = self.generate_pagination(get_pagination)
        city_urls_pagination = self.get_urls_from_pagination(server, pagination)
        city_urls = city_urls_front + city_urls_pagination
        return city_urls
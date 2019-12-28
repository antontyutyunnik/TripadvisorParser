from bs4 import BeautifulSoup as bs
from tqdm import tqdm as progress

class Cities_parser:

    def get_urls_from_front_page(self, response):
        lxml = bs(response.content, 'lxml')
        cities = lxml.find_all('div', attrs={'class': 'geo_name'})

        list = []
        base_url = 'https://www.tripadvisor.de'

        for city in cities:
            link = city.find('a', href=True)['href']
            list.append({
                'link': base_url + link,
            })
        return list


    def generate_pagination(self, url):
        urls = []
        for i in progress(range(20, 7000, 20)):
            url = 'https://www.tripadvisor.de/Restaurants-g187275-oa{}-Germany.html#LOCATION_LIST'.format(i)
            urls.append(url)
        return urls


    def get_urls_from_pagination(self, server, pagination):
        for url in progress(pagination):
            base_url = 'https://www.tripadvisor.de'
            list = []

            response = server.get(url)
            response_in_lxml = bs(response.content, 'lxml')

            cities = response_in_lxml.find_all('ul', attrs={'class': 'geoList'})
            for city in cities:
                for li in city.find_all('li'):
                    link = li.find('a', href=True)['href']
                    list.append({
                        'link': base_url + link,
                    })
        return list

    def get_city_urls(self, server):
        url = 'https://www.tripadvisor.de/Restaurants-g187275-oa{page_num}-Germany.html#LOCATION_LIST'
        response = server.get(url)
        city_urls = self.get_urls_from_front_page(response)
        pagination = self.generate_pagination(url)
        city_urls.append(self.get_urls_from_pagination(server, pagination))
        return city_urls
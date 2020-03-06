import time
from functools import partial

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from Server import *
from DataRestaurantsParser import *
from multiprocessing.dummy import Pool as ThreadPool
from selenium import webdriver
from datetime import datetime
from multiprocessing import Pool





class PhotoRestParsed:

    def get_unparsed_restaurants_url(self, restaurants):
        list = []

        for rest in restaurants:
            photo_parsed = rest[4]
            if photo_parsed == 0:
                list.append(rest)
        return list


    def find_photos_in_hero_list(self, driver):
        button_sel = 'tinyThumb '
        urls = []
        try:
            is_exist = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.CLASS_NAME, button_sel)))
            button = driver.find_elements_by_class_name(button_sel)
            server_response_in_html = bs(driver.page_source, 'html.parser')
            photos = server_response_in_html.find_all('div', attrs={'class': 'tinyThumb'})
            for photo in enumerate(photos):
                if photo[0] == 10:
                    break
                else:
                    url = photo[1]
                    urls.append(url['data-bigurl'])
            return urls
        except:
            pass

    def get_rest_foto(self, driver, url, id_rest):
        new_url = url + '#photos;aggregationId=&albumid=101&filter=7'
        driver.get(new_url)
        time.sleep(2)
        photo_urls = []
        parsed = 0
        parsed_photo_none = 2
        button_sel = 'photoGridBox'
        try:
            is_exist = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.CLASS_NAME, button_sel)))
            button = driver.find_elements_by_class_name(button_sel)
            server_response_in_html = bs(driver.page_source, 'html.parser')
            photos = server_response_in_html.find_all('div', attrs={'class': 'albumGridItem'})
            if len(photos) == 0:
                photos = self.find_photos_in_hero_list(driver)
                for photo in enumerate(photos):
                    photo_url = photo[1]
                    photo_urls.append({'restaurantID': id_rest,
                                       'photo_url': photo_url,
                                       'parsed': parsed})
            else:
                for photo in enumerate(photos):
                    if photo[0] == 9:
                        break
                    else:
                        url = photo[1].find('img')
                        photo_url = url['src']
                        photo_urls.append({'restaurantID': id_rest,
                                           'photo_url': photo_url,
                                           'parsed': parsed})
            return photo_urls

        except:
            # pass
            photo_urls.append({'restaurantID': id_rest,
                               'parsed': parsed_photo_none})
            return photo_urls





    def start_photo_parse(self, driver, restaurant):

        # for rest_urls in tqdm.tqdm(restaurantsList):
        url = restaurant[1]
        id_rest = restaurant[0]
        foto_url = self.get_rest_foto(driver, url, id_rest)

        return foto_url
















































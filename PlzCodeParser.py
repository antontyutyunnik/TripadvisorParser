import re
import time

import tqdm
from db import *
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup as bs
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import random
import requests



def get_city_from_db():
    db = DB()
    city_from_db = db.get_all_cities_from_DB()
    return city_from_db


def get_city_name_from_url(city_from_db):
    list = []
    regex = r"\d[-].+[.html]"
    test_str = 'https://www.tripadvisor.de/Restaurants-g187371-Cologne_North_Rhine_Westphalia.html'
    for city in city_from_db:
        city_url = city[1]
        city_id = city[0]
        matches = re.finditer(regex, city_url, re.MULTILINE)

        for matchNum, match in enumerate(matches):
            url_format = ("{match}".format(match=match.group()))
            url_replace = url_format.replace('_', ' ')
            url_replace = url_replace.replace('.html', '')
            url = url_replace[:2]
            url_re = re.sub(url, '', url_replace)
            list.append({'id': city_id, 'city': url_re})
    return list

def driver():
    driver = webdriver.Chrome(executable_path=r'C:\driver\chromedriver.exe')
    driver.set_window_position(2000, 400)
    driver.set_window_size(900, 1200)
    driver.get('https://worldpostalcode.com/lookup')
    return driver

def input_search_name(city, driver):
    city_name = city['city']
    input_search = driver.find_element_by_xpath("//*[@id='search']")
    input_search.clear()
    for name in city_name:
        input_search.send_keys(name)
        time.sleep(0.3)
    input_search.send_keys(Keys.RETURN)
    time.sleep(1)

def get_plz_code(city, driver):
    list = []
    city_id = city['id']
    plz_code_sel = '#map_canvas > div.leaflet-pane.leaflet-map-pane > div.leaflet-pane.leaflet-popup-pane >' \
               ' div >div.leaflet-popup-content-wrapper > div > div.lookup_result > b'
    latitude_and_longitude_sel = '#map_canvas > div.leaflet-pane.leaflet-map-pane > div.leaflet-pane.leaflet-popup-pane >' \
                             ' div > div.leaflet-popup-content-wrapper > div > div.latlng'

    try:
        plz_elem = WebDriverWait(driver, 3).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, plz_code_sel))
        )
        plz_text = plz_elem.text
        latitude_and_longitude_text = driver.find_element_by_css_selector(latitude_and_longitude_sel).text
        latitude_and_longitude_text = latitude_and_longitude_text.replace('\nLongitude: ', '-')
        latitude_and_longitude = latitude_and_longitude_text.replace('Latitude: ', '')
        latitude = latitude_and_longitude.split('-')[0]
        longitude = latitude_and_longitude.split('-')[1]
        list.append({'id': city_id,
                     'plz_code': plz_text,
                     'latitude': latitude,
                     'longitude': longitude})
    except:
        pass
    return list

def add_plzcode_to_db(rest_urls):
    db = sqlite3.connect('C:/Users/sumyt/PycharmProjects/TripadvisorParser/tripadvisorNew.db')
    cursor = db.cursor()
    if not rest_urls:
        return
    try:
        for rest_url in rest_urls:
            # cursor.execute("INSERT INTO Cities(link, parsed, cityID) VALUES(:link, :parsed,  :cityID)", rest_url)
            cursor.execute("UPDATE Cities SET parsed = 0 WHERE id = :id", rest_url)
            cursor.execute("UPDATE Cities SET plz_code = :plz_code WHERE id = :id", rest_url)
            cursor.execute("UPDATE Cities SET latitude = :latitude WHERE id = :id", rest_url)
            cursor.execute("UPDATE Cities SET longitude = :longitude WHERE id = :id", rest_url)
        cursor.close()
        db.commit()
        db.close()
        print('Add restaurants from to DB')
    except sqlite3.Error as e:
        print(e)
        db.rollback()
        db.close()
        print("Insert DB error")

def get_unparsed_cities_parsed(unparsed_cities):
    list = []
    for city in unparsed_cities:
        parsed = city[3]
        if parsed == 1:
            list.append(city)
    return list



city_from_db = get_city_from_db()
unparsed_cities = get_unparsed_cities_parsed(city_from_db)
city_id_and_name = get_city_name_from_url(unparsed_cities)
driver = driver()
for city in tqdm.tqdm(city_id_and_name):
    input_search_name(city, driver)
    city_id_plz_local = get_plz_code(city, driver)
    if len(city_id_plz_local) == 0:
        driver.close()
        break
    else:
        add_plzcode_to_db(city_id_plz_local)
























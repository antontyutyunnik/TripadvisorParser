from telnetlib import EC
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup as bs
import json
import re

class Data_restaurants_parser:

    def get_unparsed_restaurants_url(self, restaurants):
        list = []
        for rest in restaurants:
            parsed = rest[2]
            city_id = rest[3]
            id = rest[0]
            if parsed == 0:
                if city_id == 5:
                    # if id == 12055:
                    list.append(rest)
        return list

    def get_page_json(self, server, restaurant_link):
        request = server.get(restaurant_link)
        server_response_in_html = bs(request.content, 'lxml')
        script_tags = server_response_in_html.body.find_all('script')
        for script_tag in script_tags:
            text = script_tag.text
            if 'window.__WEB_CONTEXT__'.lower() in text.lower():
                json = text.replace('window.__WEB_CONTEXT__={pageManifest', '{"pageManifest"')
                cut_string = ";(window.$WP=window.$WP||[]).push({id:'@ta/features',e:['@ta/features/bootstrap']," \
                             "m:{'@ta/features/bootstrap':function(m){m.exports=__WEB_CONTEXT__.pageManifest.features;}}});"
                json = json.replace(cut_string, '')
                return json

    def get_id_from_url(self, url):
        regex = r"[d]\d*[-]"
        matches = re.finditer(regex, url, re.MULTILINE)

        for match in matches:
            id = match.group()
            id = id.replace('d', '')
            id = id.replace('-', '')
            return id

    def if_exists(self, element):
        if element:
            return element
        else:
            return ''

    def get_latitude(self, restaurant_data):
        latitude = restaurant_data.get('latitude')
        if_latitude = self.if_exists(latitude)
        return if_latitude

    def get_longitude(self, restaurant_data):
        longitude = restaurant_data.get('longitude')
        if_longitude = self.if_exists(longitude)
        return if_longitude

    def get_timezone(self, restaurant_data):
        timezone = restaurant_data.get('timezone')
        if_timezone = self.if_exists(timezone)
        return if_timezone

    def get_phone(self, restaurant_data):
        phone = restaurant_data.get('phone')
        if_phone = self.if_exists(phone)
        return if_phone

    def get_website(self, restaurant_data):
        website = restaurant_data.get('website')
        if_website = self.if_exists(website)
        return if_website

    def get_email(self, restaurant_data):
        email = restaurant_data.get('email')
        if_email = self.if_exists(email)
        return if_email

    def get_address(self, restaurant_data):
        address = restaurant_data.get('address')
        if_address = self.if_exists(address)
        return if_address

    def get_street(self, restaurant_data):
        street = restaurant_data.get('address_obj')
        self.if_exists(street)
        street1 = restaurant_data['address_obj']['street1']
        return street1

    def get_city(self, restaurant_data):
        city = restaurant_data.get('address_obj')
        self.if_exists(city)
        if_city = restaurant_data['address_obj']['city']
        return if_city

    def get_state(self, restaurant_data):
        state = restaurant_data.get('address_obj')
        self.if_exists(state)
        if_state = restaurant_data['address_obj']['state']
        return if_state

    def get_country(self, restaurant_data):
        country = restaurant_data.get('address_obj')
        self.if_exists(country)
        if_country = restaurant_data['address_obj']['country']
        return if_country

    def get_postalcode(self, restaurant_data):
        postalcode = restaurant_data.get('address_obj')
        self.if_exists(postalcode)
        if_postalcode = restaurant_data['address_obj']['postalcode']
        return if_postalcode

    def get_work_time(self, restaurant_data):
        work_hours = []
        work_time = restaurant_data.get('display_hours')
        if_work_time = self.if_exists(work_time)
        for days in if_work_time:
            day = days.get('days')
            times = days.get('times')
            work_hours.append({'day': day, 'times': times})
        return work_hours

    def get_description(self, restaurant_data):
        description = restaurant_data.get('description')
        self.if_exists(description)
        return description

    def get_price_level(self, restaurant_data):
        price_level = restaurant_data.get('price_level')
        self.if_exists(price_level)
        return price_level

    def get_cuisine(self, restaurant_data):
        cuisine_name = []
        cuisines = restaurant_data.get('cuisine')
        self.if_exists(cuisines)
        for cuisine in cuisines:
            name = cuisine.get('name')
            cuisine_name.append(name)
        return cuisine_name

    def get_photos(self, server, url):
        response = server.get(url)
        response_in_lxml = bs(response.content, 'lxml')
        photos = response_in_lxml.find_all('div', attrs={'class': 'heroThumbnails showOnHover anchor'})
        for photo in photos:
            img = photo.find('img')



    def get_dict_from_restaurant_record(self, server, record):
        data = []
        url = record[1]
        # photos = self.get_photos(server, url)
        json_string = self.get_page_json(server, url)
        obj = json.loads(json_string)
        restaurant_id = self.get_id_from_url(url)
        restaurant_data = obj['pageManifest']['redux']['api']['responses']['/data/1.0/location/' + restaurant_id]['data']
        rest_name = restaurant_data['name']
        latitude = self.get_latitude(restaurant_data)
        longitude = self.get_longitude(restaurant_data)
        latitude_and_longitude = latitude + ',' + longitude
        timezone = self.get_timezone(restaurant_data)
        phone = self.get_phone(restaurant_data)
        website = self.get_website(restaurant_data)
        email = self.get_email(restaurant_data)
        # address = self.get_address(restaurant_data)
        street = self.get_street(restaurant_data)
        city = self.get_city(restaurant_data)
        state = self.get_state(restaurant_data)
        country = self.get_country(restaurant_data)
        postalcode = self.get_postalcode(restaurant_data)
        work_hours = self.get_work_time(restaurant_data)
        description = self.get_description(restaurant_data)
        price_level = self.get_price_level(restaurant_data)
        cuisine = self.get_cuisine(restaurant_data)

        data.append({'rest_name': rest_name,
                     'latitude_and_longitude': latitude_and_longitude,
                     'timezone': timezone,
                     'phone': phone,
                     'website': website,
                     'email': email,
                     'street': street,
                     'city': city,
                     'state': state,
                     'country': country,
                     'postalcode': postalcode,
                     'work_hours': work_hours,
                     'description': description,
                     'price_level': price_level,
                     'cuisine': cuisine})
        return data

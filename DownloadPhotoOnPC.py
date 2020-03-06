import time
from DataRestaurantsParser import *
import urllib.request
import os

file_path = 'images/'

class DownloadPhoto:

    def get_unparsed_photo(self, restaurants):
        rest_list = []

        for rest in restaurants:
            photo_parsed = rest[4]
            id = rest[0]

            if photo_parsed == 1:
                # if id == 1409600:
                rest_list.append(rest)
        return rest_list

    def country_directory_creation(self, country):
        try:
            os.mkdir(file_path + country)
        except OSError:
            return file_path + country + '/'
        else:
            return file_path + country + '/'

    def city_directory_creation(self, country_directory, city):
        try:
            os.mkdir(country_directory + city)
        except OSError:
            return country_directory + city + '/'
        else:
            return country_directory + city + '/'

    def id_rest_directory_creation(self, city_directory, rest_id):
        try:
            os.mkdir(city_directory + rest_id)
        except OSError:
            return city_directory + rest_id + '/'
        else:
            return city_directory + rest_id + '/'

    def name_rest_directory_creation(self, id_rest_directory, rest_name):
        try:
            os.mkdir(id_rest_directory + rest_name)
        except OSError:
            return id_rest_directory + rest_name + '/'
        else:
            return id_rest_directory + rest_name + '/'

    def re_name_rest(self, rest_name):
        name = rest_name.replace('/', '')
        name = name.replace(',', '')
        name = name.replace('.', '')
        name = name.replace("'", '_')
        name = name.replace('`', '-')
        name = name.replace('-&', '')
        name = name.replace('"', '')
        name = name.replace('-|', '')
        name = name.replace('„', '')
        name = name.replace('“', '')
        name = name.replace(' ', '-')
        name = name.replace('---', '-')
        return name

    def directory_creation(self, country, city, rest_id):
        country_directory = self.country_directory_creation(country)
        city_directory = self.city_directory_creation(country_directory, city)
        id_rest_directory = self.id_rest_directory_creation(city_directory, rest_id)
        # name_rest_directory = self.name_rest_directory_creation(id_rest_directory, re_rest_name)
        return id_rest_directory

    def url_to_jpg(self, urls, directory, rest_id):
        list = []
        server = Server()

        for i, url in enumerate(urls, start=1):
            url = url.replace(' ', '%20')
            resp = server.get_photo(url)

            if resp is not None:
                time.sleep(0.5)
                filename = '{}.jpg'.format(i)
                full_path = '{}{}'.format(directory, filename)
                urllib.request.urlretrieve(url, full_path)
                list.append({'restaurantID': rest_id,
                             'path': full_path})

        return list


    def downlod_photo(self, restaurant):
        db = DB()

        rest_id = str(restaurant[0])
        country = db.get_country_from_db_data_rest(restaurant)
        city = db.get_city_from_db_data_rest(restaurant)
        # rest_name = db.get_rest_name_from_db_data_rest(restaurant)
        # re_rest_name = re_name_rest(rest_name)

        photo_urls = db.get_photo_urls_from_db_data_rest(restaurant)
        directory = self.directory_creation(country, city, rest_id)
        path = self.url_to_jpg(photo_urls, directory, rest_id)

        return path





























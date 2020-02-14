from multiprocessing import Pool

from Server import *
from Json import *
from CityParser import *
from db import *
from RestaurantsParser import *
from DataRestaurantsParser import *
from Json import *






def get_cities():
    city_parser = Cities_parser()
    city_urls = city_parser.get_city_urls(server)
    write_cities = db.write_cities(city_urls)


def get_restaurants():
    server = Server()
    db = DB()
    cities = db.get_all_cities_from_DB()
    rest_parser = Restaurants_parser()
    unparsed_cities = rest_parser.get_unparsed_cities_url(cities)

    for city in tqdm.tqdm(unparsed_cities):
        rest_urls = rest_parser.start_get_urls(city, server)
        if rest_urls is not None:
            rest_write = db.write_restaurants(rest_urls)


def get_data_restaurants(unparsed_rest):
    data_rest_parser = Data_restaurants_parser()
    db = DB()
    rest_dict, work_time = data_rest_parser.get_dict_from_restaurant_record(unparsed_rest)
    if len(rest_dict) > 0:
        rest_record = db.restaurant_record(rest_dict)
        if work_time is not None:
            work_time_record = db.work_time_restaurant_record(work_time)

def pool_get_data_restaurants():
    data_rest_parser = Data_restaurants_parser()
    restaurants = db.get_all_restaurants_from_DB()
    unparsed_rest = data_rest_parser.get_unparsed_restaurants_url(restaurants)

    with Pool(20) as pool:
        rest = list(tqdm.tqdm(pool.imap(get_data_restaurants, unparsed_rest)))
    pool.close()
    pool.join()


if __name__ == '__main__':
    server = Server()
    db = DB()
    # get_restaurants()
    pool_get_data_restaurants()
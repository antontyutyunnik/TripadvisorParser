from Server import *
from Json import *
from CityParser import *
from db import *
from RestaurantsParser import *
from DataRestaurantsParser import *
from Json import *


if __name__ == '__main__':

    server = Server()
    db = DB()


    # city_parser = Cities_parser()
    # city_urls = city_parser.get_city_urls(server)
    # write_cities = db.write_cities(city_urls)


    #
    # cities = db.get_all_cities_from_DB()
    # rest_parser = Restaurants_parser()
    # unparsed_cities = rest_parser.get_unparsed_cities_url(cities)
    #
    # for city in tqdm.tqdm(unparsed_cities):
    #     rest_urls = rest_parser.get_urls(city, server)
    #     rest_write = db.write_restaurants(rest_urls)



    data_rest_parser = Data_restaurants_parser()
    restaurants = db.get_all_restaurants_from_DB()
    unparsed_rest = data_rest_parser.get_unparsed_restaurants_url(restaurants)

    for restaurant in tqdm.tqdm(unparsed_rest):
        rest_dict, work_time = data_rest_parser.get_dict_from_restaurant_record(server, restaurant)
        rest_record = db.restaurant_record(rest_dict)
        print(rest_dict)
        if work_time is not None:
            work_time_record = db.work_time_restaurant_record(work_time)







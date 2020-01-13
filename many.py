from Server import *
from CityParser import *
from db import *
from RestaurantsParser import *

if __name__ == '__main__':

    server = Server()
    # city_parser = Cities_parser()
    #
    # city_urls = city_parser.get_city_urls(server)
    #
    db = DB()
    # write_cities = db.write_cities(city_urls)

    cities = db.get_all_cities_from_DB()

    rest_parser = Restaurants_parser()
    unparsed_cities = rest_parser.get_unparsed_cities_url(cities)

    for city in tqdm.tqdm(unparsed_cities):
        rest_urls = rest_parser.get_urls(city, server)
        rest_write = db.write_restaurants(rest_urls)









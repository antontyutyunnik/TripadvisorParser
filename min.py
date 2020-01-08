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

    get_cities_urls = db.get_all_cities_from_DB()

    rest_parser = Restaurants_parser()
    cities_urls = rest_parser.parsed_restaurants(get_cities_urls, server)








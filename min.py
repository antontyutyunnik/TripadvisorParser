from Server import *
from CityParser import *
from db import *

if __name__ == '__main__':

    server = Server()
    city_parser = Cities_parser()

    city_urls = city_parser.get_city_urls(server)

    db = DB()
    write_cities = db.write_cities(city_urls)








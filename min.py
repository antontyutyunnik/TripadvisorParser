from Server import *
from CityParser import *

if __name__ == '__main__':

    server = Server()
    city_parser = Cities_parser()

    city_urls = city_parser.get_city_urls(server)






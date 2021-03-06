import requests
import logging
from mkad.settings import AppSettings
from flask_restful import Resource
from flask_restful import Resource, reqparse
from .response_handlers import generate_response
from mkad.app.helpers.data_manipulation import build_address, build_polygon
from mkad.app.helpers import input_checkers

# Configuring Request Parser
mkad_post_parser = reqparse.RequestParser()
mkad_post_parser.add_argument('country',  dest='country')
mkad_post_parser.add_argument('provinces',  dest='provinces', action='append')
mkad_post_parser.add_argument('area',  dest='area')
mkad_post_parser.add_argument('locality',  dest='locality')
mkad_post_parser.add_argument('street',  dest='street')
mkad_post_parser.add_argument('house',  dest='house')

generic_post_parser = reqparse.RequestParser()
generic_post_parser.add_argument('lonlat_list',  dest='lonlat_list', action= 'append', required= True)
generic_post_parser.add_argument('country',  dest='country')
generic_post_parser.add_argument('provinces',  dest='provinces', action='append')
generic_post_parser.add_argument('area',  dest='area')
generic_post_parser.add_argument('locality',  dest='locality')
generic_post_parser.add_argument('street',  dest='street')
generic_post_parser.add_argument('house',  dest='house')


class DistanceFromMKAD(Resource):
    """It interprets the payload arguments, makes a request to the Yandex API to get the latitude and longitude, and returns the distance from the point to MKAD. 
    \n If the address passed is within MKAD, the distance is given as 0.
    \n Only the http post method is allowed.
    """
    
    def post(self):
        # Builds the required data
        logging.info(f"{'-' * 50} REQUEST {'-' * 50}")
        args= mkad_post_parser.parse_args()
        input_checkers.has2arguments(args)
        address= build_address(args)
        logging.info("-> Searched address: %s", address.encode('utf8'))
        payload= {
            "apikey": AppSettings.get_str("yandex_api_key"),
            "geocode": address ,
            "format": "json",
            "lang": "en_US" 
        }

        # Makes a request to the Yandex api
        r = requests.get('https://geocode-maps.yandex.ru/1.x/', params=payload)

        #Checks the distance
        response = generate_response(r)
        logging.info(f"{'-' * 47} END OF REQUEST {'-' * 46}")
        return response


class DistanceFromGeneric(Resource):
    """It interprets the payload arguments, makes a request to the Yandex API to get the latitude and longitude, and returns the distance from 
    \n the point to polygon passed in arguments. 
    \n If the address passed is within polygon, the distance is given as 0.
    \n Only the http post method is allowed.
    """
    
    def post(self):
        # Builds the required data
        logging.info(f"{'-' * 50} REQUEST {'-' * 50}")
        args= generic_post_parser.parse_args()
        input_checkers.has2arguments(args)
        input_checkers.has_len_shorter_than(args.lonlat_list, 50)
        address= build_address(args)
        logging.info("-> Searched address: %s", address.encode('utf8'))
        payload= {
            "apikey": AppSettings.get_str("yandex_api_key"),
            "geocode": address ,
            "format": "json",
            "lang": "en_US" 
        }

        # Makes a request to the Yandex api
        r = requests.get('https://geocode-maps.yandex.ru/1.x/', params=payload)

        
        #Checks the distance
        response = generate_response(r, build_polygon(args.lonlat_list))
        logging.info(f"{'-' * 47} END OF REQUEST {'-' * 46}")
        return response


class Root(Resource):
    """
    Default answers for http methods in / 
    """

    def get(self):
        return {'Server Status': 'Working!!'}


    def post(self):
        return {'Server Status': 'Working!!'}

    
    def put(self):
        return {'Server Status': 'Working!!'}


    def patch(self):
        return {'Server Status': 'Working!!'}


    def delete(self):
        return {'Server Status': 'Working!!'}
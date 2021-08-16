import requests
import logging
from mkad.settings import AppSettings
from flask_restful import Resource
from flask_restful import Resource, reqparse
from .response_handlers import handle_yandex_response
from mkad.app.helpers.data_manipulation import build_address
from mkad.app.helpers import input_checkers

# Configuring Request Parser
mkad_post_parser = reqparse.RequestParser()
mkad_post_parser.add_argument('country',  dest='country')
mkad_post_parser.add_argument('provinces',  dest='provinces', action='append')
mkad_post_parser.add_argument('area',  dest='area')
mkad_post_parser.add_argument('locality',  dest='locality')
mkad_post_parser.add_argument('street',  dest='street')
mkad_post_parser.add_argument('house',  dest='house')


class DistanceFromMKAD(Resource):
    """It interprets the payload arguments, makes a request to the Yandex API to get the latitude and longitude, and returns the distance from the point to MKAD. 
    \n If the address passed is within MKAD. The distance is given as 0.
    \n Only the http post method is allowed.
    """
    
    def post(self):
        # Builds the required data
        args= mkad_post_parser.parse_args()
        input_checkers.has2arguments(args)
        address= build_address(args)
        logging.info(f"{'-' * 50} REQUEST {'-' * 50}")
        logging.info("-> Searched address: %s", address.encode('utf8'))
        payload= {
            "apikey": AppSettings.get_str("yandex_api_key"),
            "geocode": address ,
            "format": "json",
            "lang": "en_US" 
        }

        # Makes a request to the Yandex api
        r = requests.get('https://geocode-maps.yandex.ru/1.x/', params=payload)

        #Checks the location of the point
        response = handle_yandex_response(r)
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
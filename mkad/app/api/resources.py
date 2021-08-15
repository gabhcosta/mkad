import requests
import logging
from mkad.settings import AppSettings
from flask_restful import Resource
from flask_restful import Resource, reqparse
from .response_handlers import handle_yandex_response
from mkad.app.helpers.data_manipulation import build_address
from mkad.app.helpers import input_checkers


post_parser = reqparse.RequestParser()
post_parser.add_argument('country',  dest='country')
post_parser.add_argument('provinces',  dest='provinces', action='append')
post_parser.add_argument('area',  dest='area')
post_parser.add_argument('locality',  dest='locality')
post_parser.add_argument('street',  dest='street')
post_parser.add_argument('house',  dest='house')

class DistanceFromMKAD(Resource):
    def post(self):
        args= post_parser.parse_args()
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
        r = requests.get('https://geocode-maps.yandex.ru/1.x/', params=payload)

    
        response = handle_yandex_response(r)
        logging.info(f"{'-' * 47} END OF REQUEST {'-' * 46}")
        return response

class Root(Resource):
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
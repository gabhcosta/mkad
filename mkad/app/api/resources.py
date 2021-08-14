import requests
import logging
from mkad.settings import AppSettings
from flask_restful import Resource
from flask_restful import Resource, reqparse
from .response_handlers import handle_yandex_response
from mkad.app.helpers.data_manipulation import build_address


post_parser = reqparse.RequestParser()
post_parser.add_argument('country', dest='country')
post_parser.add_argument('provinces', dest='provinces', action='append')
post_parser.add_argument('area', dest='area')
post_parser.add_argument('locality', dest='locality')
post_parser.add_argument('street', dest='street')
post_parser.add_argument('house', dest='house')

class DistanceFromMKAD(Resource):
    def get(self):
        return {'It\'s Working!!'}

    def post(self):
        args= post_parser.parse_args()
        address= build_address(args)
        logging.info(f"{'-' * 50} REQUEST {'-' * 50}")
        logging.info(f"-> Searched address: {address}")
        payload= {
            "apikey": AppSettings.get_str("yandex_api_key"),
            "geocode": address ,
            "format": "json",
            "lang": "en_US" 
        }
        r = requests.get('https://geocode-maps.yandex.ru/1.x/', params=payload, stream= True)
        response = handle_yandex_response(r)
        logging.info(f"{'-' * 47} END OF REQUEST {'-' * 46}")
        return response
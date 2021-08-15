from mkad.settings import AppSettings
from flask import Flask, Blueprint
from flask_restful import Api
from .resources import DistanceFromMKAD, Root

AppSettings.setup() # Configuring global variables

# API Configs
app = Flask(__name__)
api_bp = Blueprint('api', __name__)
mkad_api = Api(api_bp)
mkad_api.add_resource(Root, '/') # Default answers for http methods in / 
mkad_api.add_resource(DistanceFromMKAD, '/api')
app.register_blueprint(api_bp)


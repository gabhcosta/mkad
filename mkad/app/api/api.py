from mkad.settings import AppSettings
from flask import Flask, Blueprint
from flask_restful import Api

from .resources import DistanceFromMKAD

AppSettings.setup()
app = Flask(__name__)
api_bp = Blueprint('api', __name__)
api = Api(api_bp)


api.add_resource(DistanceFromMKAD, '/')
app.register_blueprint(api_bp)

from flask import Blueprint
from modulefinder import importlib

api_blueprint = Blueprint('api', __name__)

importlib.import_module(f'{__name__}.handler')

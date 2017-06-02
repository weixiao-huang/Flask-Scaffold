"""
flask app
"""

from config import configs
from flask import Flask

from modulefinder import importlib


def create_app(name):
    app = Flask(__name__)
    app.config.from_object(configs[name])

    main = importlib.import_module('app.main')
    api = importlib.import_module('app.api')
    app.register_blueprint(main.main_blueprint, url_prefix='/')
    app.register_blueprint(api.api_blueprint, url_prefix='/api/v1')

    return app

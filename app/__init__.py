"""
flask app
"""

from config import configs
from flask import Flask

from modulefinder import importlib


def create_app(name):
    app = Flask(__name__, static_folder='../static')
    app.config.from_object(configs[name])

    main = importlib.import_module('app.main')
    app.register_blueprint(main.main_blueprint)

    return app

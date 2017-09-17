"""
flask app
"""

from config import configs
from flask import Flask
from flask_redis import FlaskRedis

from modulefinder import importlib

redis_store = FlaskRedis()


def create_app(name):
    app = Flask(__name__, static_folder='../static')
    app.config.from_object(configs[name])

    redis_store.init_app(app)

    main = importlib.import_module('app.main')
    api = importlib.import_module('app.api')
    app.register_blueprint(main.main_blueprint)
    app.register_blueprint(api.api_blueprint, url_prefix='/api/v1')

    return app

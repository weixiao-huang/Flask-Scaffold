"""
flask app
"""

from config import configs
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app(name):
    app = Flask(__name__)
    app.config.from_object(configs[name])

    db.init_app(app)

    return app

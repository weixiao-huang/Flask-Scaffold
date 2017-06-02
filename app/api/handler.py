from app.api import api_blueprint
from flask import render_template


@api_blueprint.route('/')
def index():
    return 'hello world'

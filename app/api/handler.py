from app.api import api_blueprint
from flask import render_template, request, jsonify
from .util import get_img_by_name


@api_blueprint.route('/img_by_name', methods=['POST'])
def index():
    name = request.json['name']
    url = get_img_by_name(name)
    return url

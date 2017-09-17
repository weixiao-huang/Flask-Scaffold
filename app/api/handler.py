from app.api import api_blueprint
from flask import request, jsonify
from .util import get_result_url_by_name


@api_blueprint.route('/sports', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        try:
            name = request.json['name']
            if name is None or name == '':
                raise ValueError
            result, bgRGB = get_result_url_by_name(name)
            return jsonify({'result': result, 'bg': bgRGB})
        except ValueError:
            return 'ValueError', 400
    else:
        return 'hello world'

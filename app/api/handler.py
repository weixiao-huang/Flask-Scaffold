from app.api import api_blueprint
from flask import request, jsonify
from .util import get_result_url_by_name


@api_blueprint.route('/sports', methods=['POST'])
def index():
    try:
        name = request.form['name']
        if name is None or name == '':
            raise ValueError
        result, bgRGB = get_result_url_by_name(name)
        return jsonify({'result': result, 'bg': bgRGB})
    except ValueError:
        return 'ValueError', 400

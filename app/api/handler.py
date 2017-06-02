from app.api import api_blueprint
from flask import request, jsonify
from .util import get_result_url_by_name


@api_blueprint.route('/img_by_name', methods=['POST'])
def index():
    name = request.form['name']
    result, bg = get_result_url_by_name(name)
    return jsonify({'result': result, 'bg': bg})

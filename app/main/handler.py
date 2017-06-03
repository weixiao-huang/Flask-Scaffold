from app.main import main_blueprint
from flask import render_template, request
from app.api.util import get_img_by_name


@main_blueprint.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        name = request.form['name']
        result = get_img_by_name(name)
        return render_template("result.html", result=result)
    else:
        return render_template('index.html')

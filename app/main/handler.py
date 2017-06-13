from flask import render_template, request
from app.main import main_blueprint
from .util import get_result_url_by_name_and_id


@main_blueprint.route('/')
def index():
    return render_template('index.html',
                           imgs=[1, 2, 3, 4, 5, 6])


@main_blueprint.route('/draw', methods=['GET', 'POST'])
def draw():
    if request.method == 'GET':
        try:
            id = int(request.args.get('id'))
            return render_template('draw.html', id=id)
        except (ValueError, TypeError) as e:
            return render_template('index.html',
                                   imgs=[1, 2, 3, 4, 5, 6])
    else:
        id = int(request.form['id'])
        name = request.form['name']
        print('1231231231', id, name)
        url = get_result_url_by_name_and_id(name, id)
        print(url)
        return render_template('result.html',
                               url=url,
                               id=id,
                               name=name)


@main_blueprint.route('/result')
def result():
    url = get_result_url_by_name_and_id('黄维啸', 1)
    return render_template('result.html', url=url)

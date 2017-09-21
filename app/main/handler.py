from flask import render_template, request
from app.main import main_blueprint
from .util import get_result_url_by_name_and_id


@main_blueprint.route('/')
def index():
    return render_template('index.html',
                           imgs=[1, 2, 3, 4, 5, 6])


@main_blueprint.route('/sports')
def sports():
    return render_template('sports.html')


@main_blueprint.route('/draw', methods=['GET', 'POST'])
def draw():
    if request.method == 'GET':
        try:
            id = int(request.args.get('id'))
            name = request.args.get('name')
            if name is not None:
                return render_template('draw.html', id=id, name=name)
            return render_template('draw.html', id=id)
        except (ValueError, TypeError) as e:
            return render_template('index.html',
                                   imgs=[1, 2, 3, 4, 5, 6])
    else:
        id = int(request.form.get('id'))
        name = request.form.get('name')

        if id is None:
            return render_template('index.html',
                                   imgs=[1, 2, 3, 4, 5, 6])
        elif name is None or name == '':
            return render_template('empty.html')

        pId = request.form.get('personalityId')
        try:
            if pId is not None:
                pId = int(pId) + 1
            url, pId = get_result_url_by_name_and_id(name, id, pId)
        except ValueError:
            url, pId = get_result_url_by_name_and_id(name, id)
        return render_template('result.html',
                               url=url,
                               id=id,
                               name=name,
                               pId=pId)


@main_blueprint.route('/result')
def result():
    url = get_result_url_by_name_and_id('黄维啸', 1)
    return render_template('result.html', url=url)

from app.main import main_blueprint
from flask import render_template, request, redirect, url_for
from app.api.util import get_result_url_by_name


@main_blueprint.route('', methods=['POST', 'GET'])
def index():
    try:
        if request.method == 'POST':
            name = request.form['name']
            if name is None or name == '':
                raise ValueError
            return redirect(url_for('main.shake', name=name))
        else:
            return render_template('index.html')
    except ValueError:
        return 'ValueError', 400


@main_blueprint.route('shake', methods=['GET', 'POST'])
def shake():
    try:
        if request.method == 'GET':
            name = request.args.get('name')
            result, bg = get_result_url_by_name(name)
            return render_template('shake.html', result=result, bg=bg)
    except Exception as e:
        return e, 400


@main_blueprint.route('result', methods=['GET'])
def result():
    try:
        return render_template('result.html',
                               result=request.args.get('result'),
                               bg=request.args.get('bg'))
    except Exception as e:
        return e, 400

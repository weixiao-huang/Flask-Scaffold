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
            result = get_result_url_by_name(name)
            # return redirect(url_for('main.shake', name=name))
            return render_template('result.html', result=result)
        else:
            return render_template('index.html')
    except ValueError:
        return render_template('empty.html')

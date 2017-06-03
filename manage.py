from flask_script import Manager
from gunicorn.app.base import Application
from app import create_app
import os

app = create_app(os.getenv('FLASK_CONFIG', 'default'))
manager = Manager(app)


class GunicornApplication(Application):
    def init(self, parser, opts, args):
        return dict(bind='0.0.0.0:5001', workers=4)

    def load(self):
        return app


@manager.command
def run_gunicorn():
    GunicornApplication().run()


@manager.command
def lint():
    # TODO: call from library
    os.system('pep8 --show-source --show-pep8 app')


@manager.command
def compile_requirements():
    # TODO: call from library
    os.system('pip-compile')


if __name__ == '__main__':
    manager.run()

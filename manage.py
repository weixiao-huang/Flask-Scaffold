from flask_script import Manager
from app import create_app, db
import os

app = create_app(os.getenv('FLASK_CONFIG', 'default'))
manager = Manager(app)


@manager.command
def lint():
    # TODO: call from library
    os.system('pep8 --show-source --show-pep8 app')


@manager.command
def compile_requirements():
    # TODO: call from library
    os.system('pip-compile')


@manager.command
def create_all():
    db.create_all()


@manager.command
def drop_all():
    db.drop_all()


if __name__ == '__main__':
    manager.run()

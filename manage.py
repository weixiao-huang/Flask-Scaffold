from flask_script import Manager
from app import create_app
import os

app = create_app(os.getenv('FLASK_CONFIG', 'default'))
manager = Manager(app)


@manager.command
def lint():
    # TODO: call from library
    os.system('pep8 --show-source --show-pep8 app')


if __name__ == '__main__':
    manager.run()

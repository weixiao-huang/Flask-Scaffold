from app.main import main_blueprint


@main_blueprint.route('/')
def index():
    return 'Hello World from new config'

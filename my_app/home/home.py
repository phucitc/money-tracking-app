from flask import Blueprint

home_blueprint = Blueprint('homepage', __name__, template_folder='templates')

@home_blueprint.route('/')
def index():

    return "<p>Hello, World!</p>"

from flask import Blueprint, render_template

# VueJS need to build, then copy dist folder to this folder and rename to vuejs_webapp
home_blueprint = Blueprint('homepage', __name__, template_folder='vuejs_webapp', static_folder='vuejs_webapp/assets')

@home_blueprint.route('/')
def index():
    return render_template('index.html')

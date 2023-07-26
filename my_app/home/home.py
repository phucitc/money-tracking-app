from flask import Blueprint, render_template

# VueJS need to build, then copy dist folder to this folder and rename to vuejs_webapp
home_blueprint = Blueprint('homepage', __name__, template_folder='vuejs_webapp', static_folder='vuejs_webapp/assets')

@home_blueprint.route('/')
def index():
    return render_template('index.html')

@home_blueprint.route('/<slug>')
def redirect_link(slug):
    if slug is not None:
        # these are routes in VueJS
        spa_routes = ['home', 'login', 'signup', 'logout', 'profile', 'dashboard', 'about', 'callback' ]
        if slug in spa_routes:
            return render_template('index.html')
        print(slug)
        return slug
    else:
        return 'No link'


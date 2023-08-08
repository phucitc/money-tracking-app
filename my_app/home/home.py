from flask import Blueprint, render_template, redirect

from model.url import URL

# VueJS need to build, then copy dist folder to this folder and rename to vuejs_webapp
home_blueprint = Blueprint('homepage', __name__, template_folder='vuejs_webapp', static_folder='vuejs_webapp/assets')


@home_blueprint.route('/')
def index():
    print("AAAAAAAAAAAAAAA")
    return render_template('index.html')


@home_blueprint.route('/<slug>')
def redirect_link(slug):
    print("BBB")
    if slug is not None:
        # these are routes in VueJS
        spa_routes = ['home', 'login', 'signup', 'logout', 'profile', 'dashboard', 'about', 'callback']
        if slug in spa_routes:
            return render_template('index.html')
        print(slug)

        url = URL()
        item = url.get_by_public_id(slug)
        if item:
            # Process to track click here
            return redirect(item['destination_link'], code=301)
        else:
            return render_template('index.html'), 404
    else:
        return 'No link'

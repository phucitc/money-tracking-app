import os

from authlib.integrations.flask_client import OAuth
from flask import Flask, send_from_directory, current_app, session
from flask_cors import CORS
from flask_restful import Api
from flask_wtf.csrf import CSRFProtect

from dotenv import load_dotenv

from api.admin_resource import AdminResource
from api.auth_resource import AuthResource
from model.model import Model
from myapp.account.account import account_blueprint

load_dotenv()

from api.url_resource import URLResource
from classes.todo_resource import TodoResource
from classes.user_resource import UserResource
from myapp.home.home import home_blueprint

# Setup template_folder and static_folder are from VueJS build
app = Flask(__name__, static_folder='static')
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['WTF_CSRF_CHECK_DEFAULT'] = False

# Comment out this line if you want to use VueJS in localhost
# TODO Uncomment this line if you want deploy app to Production
csrf = CSRFProtect()
csrf.init_app(app)
# api = Api(app)
# CORS(app, resources={r"/*": {"origins": ["http://localhost:5173", "http://zipit.link", "https://zipit.link"]}})
CORS(app, origins=["http://localhost:5173", "http://localhost:5000", "http://zipit.link", "https://zipit.link"])

# Load environment variables
for key, value in os.environ.items():
    app.config[key] = value


# Define your middleware function
# def app_middleware(next_handler):
#     def middleware(*args, **kwargs):
#         # Perform any pre-request processing here
#         print("Executing custom middleware before request")
#         if session is None or 'user' not in session:
#             session['user'] = None
#         # Call the next handler in the chain
#         response = next_handler(*args, **kwargs)
#         # Perform any post-request processing here
#         print("Executing custom middleware after request")
#         # model = Model()
#         # model.get_plsql().close()
#         return response
#     return middleware
def app_middle(next_handler):
    @app.before_request
    def before_request():
        print("Executing custom middleware before request")
        if session is None or 'user' not in session or not session['user']:
            session['user'] = {
                'id': None
            }

    @app.after_request
    def after_request(response):
        print("Executing custom middleware after request")
        model = Model()
        model.get_plsql().close()
        return response

    # def middleware(*args, **kwargs):
    #     print("Executing custom middleware before request")
    #     if session is None or 'user' not in session:
    #         session['user'] = None
    #     response = next_handler(*args, **kwargs)
    #     print("Executing custom middleware after request")
    #     model = Model()
    #     model.get_plsql().close()
    #     return response
    #
    # return middleware


app_middle(app)

# Apply the middleware to all routes
# app.wsgi_app = app_middle(app.wsgi_app)
# Add the resource to the API
# api.add_resource(TodoResource, '/todos/<int:todo_id>')
# api.add_resource(AuthResource, '/auth')
# api.add_resource(UserResource, '/user/<int:user_id>')
# api.add_resource(URLResource, '/api/url/short-url')
# api.add_resource(AdminResource, '/admin-api/<string:action>')
# route
# @app.route('/favicon.ico')
# def favicon():
#     return send_from_directory(os.path.join(app.root_path, 'static'),
#                                'favicon.ico', mimetype='image/vnd.microsoft.icon')
#
# @app.route('/sitemap.xml')
# def return_sitemap():
#     result = open('sitemap.xml', 'r').read()
#     return result, 200, {'Content-Type': 'application/xml; charset=utf-8'}
#
#
# @app.route('/robots.txt')
# def return_robots():
#     result = open('robots.txt', 'r').read()
#     return result, 200, {'Content-Type': 'text/plain; charset=utf-8'}

app.register_blueprint(home_blueprint)
app.register_blueprint(account_blueprint)
oauth = OAuth(app)

oauth.register(
    "auth0",
    client_id=app.config["AUTH0_CLIENT_ID"],
    client_secret=app.config["AUTH0_CLIENT_SECRET"],
    client_kwargs={
        "scope": "openid profile email",
    },
    server_metadata_url=f'https://{app.config["AUTH0_DOMAIN"]}/.well-known/openid-configuration'
)
app.config["oauth"] = oauth

# @app.route("/app")
# def hello():
#     return "Hello"


if __name__ == '__main__':
    app.run(debug=True, port=os.getenv('PORT'))

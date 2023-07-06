from flask import Flask
from flask_cors import CORS
from flask_restful import Api

from classes.auth_resource import AuthResource
from classes.todo_resource import TodoResource
from classes.user_resource import UserResource

app = Flask(__name__)
api = Api(app)
CORS(app, resources={r"/*": {"origins": "http://localhost:5173"}})


# Define your middleware function
def app_middleware(next_handler):
    def middleware(*args, **kwargs):
        # Perform any pre-request processing here
        print("Executing custom middleware before request")
        # Call the next handler in the chain
        response = next_handler(*args, **kwargs)
        # Perform any post-request processing here
        print("Executing custom middleware after request")
        return response
    return middleware

# Apply the middleware to all routes
app.wsgi_app = app_middleware(app.wsgi_app)

# Add the resource to the API
api.add_resource(TodoResource, '/todos/<int:todo_id>')
api.add_resource(AuthResource, '/callback')
api.add_resource(UserResource, '/user/<int:user_id>')

if __name__ == '__main__':
    app.run(debug=True)
# Decorator for authentication
from functools import wraps

from flask import request
from flask_wtf import CSRFProtect

from classes.constant import Constant
from py.helper import Helper


def authenticate(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # Get the Authorization header from the request
        auth_header = request.headers.get('Authorization')
        if auth_header:
            # Extract the token from the header
            token = auth_header.split()[1]  # Assuming 'Bearer <token>'
            print('token', token)
            # Check if the token is valid (example check)
            if token == 'your_token':  # Replace with your authentication logic
                return func(*args, **kwargs)
        # Unauthorized access
        return {'error': 'Unauthorized'}, 401
    return wrapper

def authenticate_admin(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # Get the Authorization header from the request
        auth_header = request.headers.get('Authorization')
        if auth_header:
            # Extract the token from the header
            token = auth_header.split()[1]  # Assuming 'Bearer <token>'
            if Helper.is_empty(token) is False:
                decode, code = Helper.decode_auth0_jwt(token)
                if code == 200 and decode['email'] in Constant.ADMIN_EMAILS:
                    return func(*args, **kwargs)
        # Unauthorized access
        return {'error': 'Unauthorized'}, 401
    return wrapper


def check_csrf(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if Helper.is_production():
            print("CHECK CSRF")
            CSRFProtect().protect()
        else:
            print("NOT CHECK CSRF")

        return func(*args, **kwargs)

    return wrapper

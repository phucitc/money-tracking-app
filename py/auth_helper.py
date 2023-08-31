# Decorator for authentication
from functools import wraps

from flask import request

from classes.constant import Constant
from py.helper import is_empty, decode_auth0_jwt


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
            if is_empty(token) is False:
                decode, code = decode_auth0_jwt(token)
                if code == 200 and decode['email'] in Constant.ADMIN_EMAILS:
                    return func(*args, **kwargs)
        # Unauthorized access
        return {'error': 'Unauthorized'}, 401
    return wrapper
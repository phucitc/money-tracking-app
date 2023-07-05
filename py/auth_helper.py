# Decorator for authentication
from functools import wraps

from flask import request


def authenticate(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # Get the Authorization header from the request
        auth_header = request.headers.get('Authorization')
        if auth_header:
            # Extract the token from the header
            token = auth_header.split()[1]  # Assuming 'Bearer <token>'
            # Check if the token is valid (example check)
            if token == 'your_token':  # Replace with your authentication logic
                return func(*args, **kwargs)
        # Unauthorized access
        return {'error': 'Unauthorized'}, 401
    return wrapper
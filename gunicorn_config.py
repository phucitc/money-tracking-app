import os
from decouple import config

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Load environment variables from .env file
APP_ENV = config('APP_ENV', default='')
DEBUG = config('DEBUG', default=False, cast=bool)
AUTH0_API_DOMAIN = config('AUTH0_API_DOMAIN', default='')
DWH = config('DWH', default='')
print(DWH)
APP_DOMAIN = config('APP_DOMAIN', default='')
PORT = config('PORT', default='')

workers = 4
bind = 'localhost:8000'
accesslog = './logs/access.log'
errorlog = './logs/error.log'

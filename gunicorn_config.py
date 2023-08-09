from decouple import Config

# Initialize the Config class
config = Config()

# Load environment variables from .env file
APP_ENV = config('APP_ENV', default='')
DEBUG = config('DEBUG', default=False, cast=bool)
AUTH0_API_DOMAIN = config('AUTH0_API_DOMAIN', default='')
DWH = config('DWH', default='')
APP_DOMAIN = config('APP_DOMAIN', default='')
PORT = config('PORT', default='')

workers = 4
bind = 'localhost:8000'
accesslog = './logs/access.log'
errorlog = './logs/error.log'

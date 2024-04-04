import datetime
import hashlib
import os
import uuid
from urllib.parse import urlparse

import qrcode
import jwt
from jwt import PyJWKClient

from classes.constant import Constant


class Helper:
    @staticmethod
    def decode_auth0_jwt(token):
        # Retrieve the JSON Web Key Set (JWKS) from Auth0
        jwks_url = 'https://{domain}/.well-known/jwks.json'.format(domain=os.getenv('AUTH0_API_DOMAIN'))
        print(jwks_url)
        jwks_client = PyJWKClient(jwks_url)
        signing_key = jwks_client.get_signing_key_from_jwt(token)

        # We should cache this cache
        # webkey = {
        #     "alg": "RS256",
        #     "kty": "RSA",
        #     "use": "sig",
        #     "n": "u9JdTxEYmiAvAXgAzqL1Uh3xL339Y-EsLVMXC_nguemuaB5tGvhIGtzpjLZI2B6n37pvZvFpjXOuhKYnU5LQWo1J30aWMm91zxoX3f_s8ViYr94xQKHivbC3n9ooB0zvIj-5w62zCRBoRI-xu1POzBY4ftptineMAiFPyTvWRTa1jDj60WCCCwjcdMiA2INNfkLI_M4eRLHB5KJuavzT9c9_CJ9mtstZh6E5butIbFPc3wqP20K-5Dnr7yB9HgCB1LRUl9C_AYp74b8qR0lXsyXaO0Ylxwrmcug1Qq0OHtb9Z3DzYFcjOvf1hCnncgpyjNGRmRxYqDZjU2lmmEa1SQ",
        #     "e": "AQAB",
        #     "kid": "5G3Ofy_H_kgXJgUcxZ_NU",
        #     "x5t": "AYxQtAeu_9NyZxO6HOZY4Gl5T9Q",
        #     "x5c": [
        #         "MIIDHTCCAgWgAwIBAgIJAXdt6BcThEs3MA0GCSqGSIb3DQEBCwUAMCwxKjAoBgNVBAMTIWRldi1lMGhuOGJ3NG9zZzUwd3F6LnVzLmF1dGgwLmNvbTAeFw0yMzA2MjgwMTUwNTZaFw0zNzAzMDYwMTUwNTZaMCwxKjAoBgNVBAMTIWRldi1lMGhuOGJ3NG9zZzUwd3F6LnVzLmF1dGgwLmNvbTCCASIwDQYJKoZIhvcNAQEBBQADggEPADCCAQoCggEBALvSXU8RGJogLwF4AM6i9VId8S99/WPhLC1TFwv54LnprmgebRr4SBrc6Yy2SNgep9+6b2bxaY1zroSmJ1OS0FqNSd9GljJvdc8aF93/7PFYmK/eMUCh4r2wt5/aKAdM7yI/ucOtswkQaESPsbtTzswWOH7abYp3jAIhT8k71kU2tYw4+tFgggsI3HTIgNiDTX5CyPzOHkSxweSibmr80/XPfwifZrbLWYehOW7rSGxT3N8Kj9tCvuQ56+8gfR4AgdS0VJfQvwGKe+G/KkdJV7Ml2jtGJccK5nLoNUKtDh7W/Wdw82BXIzr39YQp53IKcozRkZkcWKg2Y1NpZphGtUkCAwEAAaNCMEAwDwYDVR0TAQH/BAUwAwEB/zAdBgNVHQ4EFgQURiSJlPfSz4QzMYwVrzy2i9NPQJwwDgYDVR0PAQH/BAQDAgKEMA0GCSqGSIb3DQEBCwUAA4IBAQBvUNH/ovzO+9PfVfzHD6s0YLNXr4ePJwqBy1ocy3O4XdLaJpOi6mZAfBcj7RdVzexa7VGXiBx9VZADiTjW7ohmdS3TX9Ch1iYiWwstJ9Iugci4+CtAFY6xLC+cFIbGi2CCLc3ErDcODuZZodsWZuZhor2xc5ZoAXFikeL5werkDLmHXBhFLSxzDW+ESFudGjKBfqJObc4MA/BeNLg/lTj73Oq9IJ444RXZIpaoS/nvCoI42lqg8/A4xsKJbI59LtAF+M6U8/tbjRB7x6faNZqfP0lXLLD9GoQRTvOlnKB7E/T7hX2MvR45TMptIiP4u0Gpoom7QFYs4ENFwXFbU9fT"
        #     ]
        # }
        # signing_key = jwt.algorithms.RSAAlgorithm.from_jwk(webkey)

        try:
            # Decode and verify the token using the signing keys
            decoded = jwt.decode(token, signing_key.key, algorithms=['RS256'],
                                 options={'verify_aud': False, 'verify_iat': False})
            print(decoded)
            return decoded, 200
        except jwt.ExpiredSignatureError as e:
            print('Error 1', str(e))

            # Token has expired
            return {'error': 'Expired token'}, 401
        except jwt.InvalidTokenError as e:
            # Invalid token
            print('Error 2', str(e))
            return {'error': 'Invalid token'}, 401

    @staticmethod
    def calculate_md5_hash(input_string):
        # Create an MD5 hash object
        md5_hash = hashlib.md5()

        # Update the hash object with the input string encoded as bytes
        md5_hash.update(input_string.encode('utf-8'))

        # Get the hexadecimal representation of the hash
        md5_hex_digest = md5_hash.hexdigest()

        return md5_hex_digest

    @staticmethod
    def is_empty(value):
        if value in [None, '']:
            return True
        return False

    @staticmethod
    def create_simple_qrcode(content):
        try:
            data = content
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(data)
            qr.make(fit=True)

            img = qr.make_image(fill_color="black", back_color="white")
            # get root path
            root_path = os.path.dirname(os.path.abspath(__file__))
            # go up one level
            root_path = os.path.dirname(root_path)
            filename = Helper.calculate_md5_hash(content) + ".png"
            # save image
            related_path = f"storage/qrcode/{filename}"
            filename = root_path + "/" + related_path
            img.save(filename)

            return related_path
        except Exception as e:
            print(e)
            return ''

    @staticmethod
    def return_link(value):
        return os.getenv('APP_DOMAIN') + '/' + value

    @staticmethod
    def get_qrcode_link(public_id):
        return Helper.return_link('qrcode/' + public_id)

    @staticmethod
    def get_root_path():
        current_dir = os.path.abspath(os.path.dirname(__file__))

        while not os.path.isfile(os.path.join(current_dir, "README.md")):
            current_dir = os.path.dirname(current_dir)
            if current_dir == os.path.dirname(current_dir):
                break

        return current_dir

    @staticmethod
    def is_development():
        return os.getenv('APP_ENV') == 'development'

    @staticmethod
    def is_production():
        return os.getenv('APP_ENV') == 'production'

    @staticmethod
    def convert_space_to_dash(value):
        return value.replace(' ', '-')

    @staticmethod
    def generate_jwt(id, seconds=15):
        # Because we run heartbeats every 10 seconds, we need to add 5 seconds to the JWT
        # Define the payload for the JWT
        payload = {
            'id': id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=seconds),
        }
        # Define a secret key (keep this secret!)
        secret_key = os.getenv('SECRET_KEY')

        # Generate the JWT
        return jwt.encode(payload, secret_key, algorithm='HS256')

    @staticmethod
    def decode_jwt(token):
        try:
            # Decode the JWT
            # options = {'verify_signature': False}
            return jwt.decode(token, os.getenv('SECRET_KEY'), algorithms=['HS256'])
        except Exception as e:
            print("Expired token " + str(e))
            return None

    @staticmethod
    def generate_uuid():
        return hashlib.sha256(os.urandom(1024)).hexdigest()

    @staticmethod
    def get_cookie(request, key):
        cookie_data = request.headers.get('Cookie', '')
        if cookie_data == '':
            return None
        cookie_value = None
        cookie_data = cookie_data.split(';')
        for item in cookie_data:
            data = item.split('=')
            if data[0] == key:
                cookie_value = data[1]
        if not cookie_value and 'Zipit-Uuid' in request.headers:
            cookie_value = request.headers['Zipit-Uuid']
        return cookie_value

    @staticmethod
    def remove_protocol(url):
        return url.replace('http://', '').replace('https://', '')

    @staticmethod
    def get_hostname(url):
        parsed_uri = urlparse(url)
        return parsed_uri.hostname

    @staticmethod
    def get_favicon_by_domain(url, size=64):
        # remove https and http
        hostname = Helper.get_hostname(url)
        uri = 'https://t1.gstatic.com/faviconV2?client=SOCIAL&type=FAVICON&fallback_opts=TYPE,SIZE,URL&url=https://{domain}&size={size}'
        return uri.format(domain=hostname, size=size)

    @staticmethod
    def is_crawler_bot(user_agent):
        user_agent_bots = Constant.USER_AGENT_BOTS
        # cast user_agent_bots to lower case
        user_agent_bots = [x.lower() for x in user_agent_bots]
        user_agent = user_agent.lower()

        # find user_agent in user_agent_bots
        for bot in user_agent_bots:
            if bot in user_agent:
                return True
        return False

    @staticmethod
    def alllow_domains(domain):
        if domain in [
            'zipit.link',
            'www.zipit.link',
            'localhost'
        ]:
            return True
        return False

    @staticmethod
    def uuid_v4():
        return str(uuid.uuid4())

    @staticmethod
    def app_domain():
        return os.getenv('APP_DOMAIN')

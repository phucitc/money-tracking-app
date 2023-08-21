import hashlib
import os

import qrcode
import jwt
from jwt import PyJWKClient

def decode_jwt(token):
    # Retrieve the JSON Web Key Set (JWKS) from Auth0
    jwks_url = 'https://{domain}/.well-known/jwks.json'.format(domain=os.getenv('AUTH0_API_DOMAIN'))
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
        decoded = jwt.decode(token, signing_key.key, algorithms=['RS256'], options={'verify_aud': False, 'verify_iat': False})
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


def calculate_md5_hash(input_string):
    # Create an MD5 hash object
    md5_hash = hashlib.md5()

    # Update the hash object with the input string encoded as bytes
    md5_hash.update(input_string.encode('utf-8'))

    # Get the hexadecimal representation of the hash
    md5_hex_digest = md5_hash.hexdigest()

    return md5_hex_digest


def is_empty(value):
    if value in [None, '']:
        return True
    return False


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
        filename = calculate_md5_hash(content) + ".png"
        # save image
        related_path = f"storage/qrcode/{filename}"
        filename = root_path + "/" + related_path
        img.save(filename)

        return related_path
    except Exception as e:
        print(e)
        return ''


def return_link(value):
    return os.getenv('APP_DOMAIN') + value


def get_qrcode_link(public_id):
    return return_link('qrcode/' + public_id)


def get_root_path():
    current_dir = os.path.abspath(os.path.dirname(__file__))

    while not os.path.isfile(os.path.join(current_dir, "README.md")):
        current_dir = os.path.dirname(current_dir)
        if current_dir == os.path.dirname(current_dir):
            break

    return current_dir


def is_production():
    return os.getenv('APP_ENV') == 'production'


def get_webapp_url():
    if is_production():
        return os.getenv('APP_DOMAIN')
    return 'http://localhost:5173/'

import os

import jwt
from jwt import PyJWKClient

def decode_jwt(token):
    # Retrieve the JSON Web Key Set (JWKS) from Auth0
    jwks_url = 'https://{domain}/.well-known/jwks.json'.format(domain=os.environ.get('AUTH0_API_DOMAIN'))
    jwks_client = PyJWKClient(jwks_url)
    signing_key = jwks_client.get_signing_key_from_jwt(token)
    try:
        # Decode and verify the token using the signing keys
        decoded = jwt.decode(token, signing_key.key, algorithms=['RS256'], options={'verify_aud': False})
        return decoded, 200
    except jwt.ExpiredSignatureError:
        # Token has expired
        return {'error': 'Expired token'}, 401
    except jwt.InvalidTokenError:
        # Invalid token
        return {'error': 'Invalid token'}, 401




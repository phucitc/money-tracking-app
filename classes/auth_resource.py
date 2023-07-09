import json

from flask import request, current_app
from flask_restful import Resource
from pip._vendor import requests


class AuthResource(Resource):

    def post(self):
        # process to sign up user
        print('Callback')
        print(request.args)
        auth0_code = request.args.get('auth0_code')
        auth0_code = "O2_9Z1YE7w3wCGd95JnJmuIxntP0d6eX1GK-VoT7ixgpy"

        # token_payload = {
        #     'client_id': current_app.config['AUTH0_API_CLIENT_ID'],
        #     'client_secret': current_app.config['AUTH0_API_CLIENT_SECRET'],
        #     'redirect_uri': current_app.config['AUTH0_API_CALLBACK_URL'],
        #     'code': auth0_code,
        #     'grant_type': 'authorization_code',
        #     # 'grant_type': 'client_credentials',
        #     # 'audience': 'https://dev-e0hn8bw4osg50wqz.us.auth0.com/api/v2/',
        # }
        # toke_url = 'https://{domain}/oauth/token'.format(domain=current_app.config['AUTH0_API_DOMAIN'])
        #
        # token_results = requests.post(toke_url,
        #                               data=json.dumps(token_payload),
        #                               headers={'content-type': 'application/json'}).json()
        # print(token_results)
        # if 'access_token' in token_results:
        access_token = 'eyJhbGciOiJkaXIiLCJlbmMiOiJBMjU2R0NNIiwiaXNzIjoiaHR0cHM6Ly9kZXYtZTBobjhidzRvc2c1MHdxei51cy5hdXRoMC5jb20vIn0..3pMDOdK3z0TcBRfJ.P4A9GFBQjmG1A0lzR3leGvWiq4A_5A4uKbqcJL4jxFS3rRT8xZXCewbOYN4nbJDTuzpWMymfWSERRCGVHKgWG8GBnhNT_cbml-Qf7TTrFPpv67ah1PpLnUoC-3NOJ6aHrcbEdNSwVJwvu8r1m8Tn6jUPwA5uYPxw9s_qyDKdFDVcPZ7zee94uisT3PXvJ0OXjIp1DwnUN82X7TUl3n0-fwtvCCp87gxTC04PxHHs6d9IMc8uMPllqjlPOam5fMzeH9VP1ZkZTsywQPdCGxF1AZ454WEDDjMDmkI2PvLzvRapzwwp64jUEU2NPf5ReGfIHzPmH9DKlUsCNQ2GOqcs15sw.2Cs8FSsoSj8kNdjbU8axAg'
        results = requests.get('https://{domain}/userinfo?access_token={access_token}'.format(
            domain=current_app.config['AUTH0_API_DOMAIN'],
            access_token=access_token))
        print(results.content)

        return {'message': 'Callback'}

    def get(self):
        print('Callback GET')
        params = request.args
        print(params)
        return {'message': 'Callback GET'}

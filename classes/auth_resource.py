import json

from flask import request, current_app
from flask_restful import Resource
from pip._vendor import requests

from py.helper import decode_jwt


class AuthResource(Resource):

    def post(self):
        # process to sign up user
        print('Callback')
        print(request.args)
        token = request.headers.get('token')
        decode, code = decode_jwt(token)
        if code == 200:
            print(decode)
            return {'message': 'success'}, 200
        else:
            return {'message': 'failed'}, 401

        # access_token = 'eyJhbGciOiJkaXIiLCJlbmMiOiJBMjU2R0NNIiwiaXNzIjoiaHR0cHM6Ly9kZXYtZTBobjhidzRvc2c1MHdxei51cy5hdXRoMC5jb20vIn0..3pMDOdK3z0TcBRfJ.P4A9GFBQjmG1A0lzR3leGvWiq4A_5A4uKbqcJL4jxFS3rRT8xZXCewbOYN4nbJDTuzpWMymfWSERRCGVHKgWG8GBnhNT_cbml-Qf7TTrFPpv67ah1PpLnUoC-3NOJ6aHrcbEdNSwVJwvu8r1m8Tn6jUPwA5uYPxw9s_qyDKdFDVcPZ7zee94uisT3PXvJ0OXjIp1DwnUN82X7TUl3n0-fwtvCCp87gxTC04PxHHs6d9IMc8uMPllqjlPOam5fMzeH9VP1ZkZTsywQPdCGxF1AZ454WEDDjMDmkI2PvLzvRapzwwp64jUEU2NPf5ReGfIHzPmH9DKlUsCNQ2GOqcs15sw.2Cs8FSsoSj8kNdjbU8axAg'
        # results = requests.get('https://{domain}/userinfo?access_token={access_token}'.format(
        #     domain=current_app.config['AUTH0_API_DOMAIN'],
        #     access_token=access_token))
        # print(results.content)


    def get(self):
        print('Callback GET')
        params = request.args
        print(params)
        return {'message': 'Callback GET'}

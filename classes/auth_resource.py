from flask import request
from flask_restful import Resource

class AuthResource(Resource):

    def post(self):
        # process to sign up user
        print('Callback')
        params = request.args
        print(params)
        return {'message': 'Callback'}

    def get(self):
        print('Callback GET')
        params = request.args
        print(params)
        return {'message': 'Callback GET'}
from flask_restful import Resource

from py.auth_helper import authenticate


class UserResource(Resource):

    @authenticate
    def get(self):
        return {'message': 'Access granted'}

    @authenticate
    def post(self):
        print('Post method')
        return {'message': 'Post method'}
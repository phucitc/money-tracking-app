from flask_restful import Resource

from py.auth_helper import authenticate


class UserResource(Resource):

    def get(self):
        return {'message': 'URL get'}

    def post(self):
        print('Post method')
        return {'message': 'URL post'}
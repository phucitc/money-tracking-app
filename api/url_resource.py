import os

from flask import request, abort
from flask_restful import Resource, reqparse

from classes.constant import Constant
from model.url import URL


class URLResource(Resource):

    def __init__(self):
        # Define the request parser with the expected parameters
        self.parser = reqparse.RequestParser()

    def get(self):
        return {'message': 'URL get'}

    def post(self):
        short_link = ''
        if request.is_json:
            payload = request.get_json()

            url = URL()
            data = dict()
            data['destination_link'] = payload['long_url'].strip()
            row = url.get_by_destination_link_hash(data['destination_link'])
            if row:
                short_link = os.getenv('APP_DOMAIN') + row['public_id']
            else:
                row = url.insert(data)
                short_link = os.getenv('APP_DOMAIN') + row['public_id']
        else:
            abort(Constant.HTTP_BAD_REQUEST, message="Invalid JSON")
        return {'short_link': short_link}


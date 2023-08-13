import os

from flask import request, abort
from flask_restful import Resource, reqparse

from classes.constant import Constant
from model.url import URL
from py.helper import is_empty, create_simple_qrcode, return_link, get_qrcode_link


class URLResource(Resource):

    def __init__(self):
        # Define the request parser with the expected parameters
        self.parser = reqparse.RequestParser()

    def get(self):
        return {'message': 'URL get'}

    def post(self):
        public_id = ''
        if request.is_json:
            payload = request.get_json()

            url = URL()
            data = dict()
            data['destination_link'] = payload['long_url'].strip()

            row = url.get_by_destination_link(data['destination_link'])
            if row is None:
                row = url.insert(data)

            if is_empty(row.qrcode_path):
                qrcode_path = create_simple_qrcode(return_link(public_id))
                url.update({'qrcode_path': qrcode_path})
            public_id = row.public_id
        else:
            abort(Constant.HTTP_BAD_REQUEST, message="Invalid JSON")
        return {
            'short_link': return_link(public_id),
            'qrcode': get_qrcode_link(public_id)
        }


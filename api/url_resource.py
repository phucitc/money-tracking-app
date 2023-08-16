import base64
from io import BytesIO

from PIL import Image
from flask import request, abort
from flask_restful import Resource, reqparse

from classes.constant import Constant
from model.url import URL
from py.helper import is_empty, create_simple_qrcode, return_link, get_qrcode_link, get_root_path


class URLResource(Resource):

    def __init__(self):
        # Define the request parser with the expected parameters
        self.parser = reqparse.RequestParser()

    def get(self):
        return {'message': 'URL get'}

    def post(self):
        public_id = ''
        qrcode_base64 = ''
        if request.is_json:
            payload = request.get_json()

            url = URL()
            data = dict()
            data['destination_link'] = payload['long_url'].strip()

            row = url.get_by_destination_link(data['destination_link'])
            if row is None:
                row = url.insert(data)

            public_id = row.public_id
            if is_empty(row.qrcode_path):
                qrcode_path = create_simple_qrcode(return_link(public_id))
                row.qrcode_path = qrcode_path
                url.update({'qrcode_path': qrcode_path})

            qrcode_file_path = get_root_path() + '/' + row.qrcode_path
            img = Image.open(qrcode_file_path)
            buffered = BytesIO()
            img.save(buffered, format="PNG")
            qrcode_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')

        else:
            abort(Constant.HTTP_BAD_REQUEST, message="Invalid JSON")
        return {
            'short_link': return_link(public_id),
            'qrcode': get_qrcode_link(public_id),
            'qrcode_base64': 'data:image/png;base64,' + qrcode_base64
        }


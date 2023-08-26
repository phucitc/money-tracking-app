import base64
from io import BytesIO

from PIL import Image
from flask import request, abort
from flask_restful import Resource, reqparse

from classes.constant import Constant
from model.url import URL
from model.url_alias import URL_Alias
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
        list_alias = []
        if request.is_json:
            payload = request.get_json()

            url = URL()
            data = dict()
            data['destination_link'] = payload['long_url'].strip()

            row = url.get_by_destination_link(data['destination_link'])
            if row is None:
                row = url.insert(data)

            public_id = row.public_id

            data = dict()
            data['url_public_id'] = public_id
            # TODO split alias to other code block to easy maintenance
            data['alias_name'] = payload['alias_name'].strip()
            result = True
            if data['alias_name'] != '':
                # check if alias belong to this url and count alias name, if count > 2 then return error message to ask client sign up new account
                result = URL_Alias().insert_no_return(data)
            if result is False:
                return {'message': 'Invalid alias name'}, Constant.HTTP_BAD_REQUEST
            else:
                condition = [
                    {
                        'column': 'url_public_id',
                        'value': public_id
                    }
                ]
                url_aliases = URL_Alias().get_all(condition)
                for item in url_aliases:
                    list_alias.append({'alias_name': return_link(item.alias_name)})

            qrcode_base64 = self.handler_qrcode(row)
        else:
            abort(Constant.HTTP_BAD_REQUEST, message="Invalid JSON")
        return {
            'short_link': return_link(public_id),
            'qrcode': get_qrcode_link(public_id),
            'list_alias': list_alias,
            'qrcode_base64': qrcode_base64
        }

    @staticmethod
    def handler_qrcode(url):
        # url is URL object
        if is_empty(url.qrcode_path):
            qrcode_path = create_simple_qrcode(return_link(url.public_id))
            url.qrcode_path = qrcode_path
            url.update({'qrcode_path': qrcode_path})

        qrcode_file_path = get_root_path() + '/' + url.qrcode_path
        img = Image.open(qrcode_file_path)
        buffered = BytesIO()
        img.save(buffered, format="PNG")
        qrcode_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')
        return 'data:image/png;base64,' + qrcode_base64

    @staticmethod
    def handler_url_alias(url):
        list_alias = []
        return list_alias



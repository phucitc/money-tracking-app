from flask import request
from flask_restful import Resource, reqparse, abort

from classes.constant import Constant
from model.url import URL
from model.url_alias import URL_Alias
from py.auth_helper import authenticate, check_csrf
from py.helper import Helper
from py.url_helper import URL_Helper


class UserURLResource(Resource):
    def __init__(self):
        # Define the request parser with the expected parameters
        self.parser = reqparse.RequestParser()

    @check_csrf
    def get(self):
        return {'list_aliases': 'OK'}

    # @check_csrf
    @authenticate
    def post(self, **kwargs):
        # For non-user
        user = kwargs.get('user')
        if request.is_json:
            payload = request.get_json()

            url_obj = URL()
            url_alias_obj = URL_Alias()
            data = dict()
            data['destination_link'] = payload['long_url'].strip()

            url = url_obj.get_by_destination_link(data['destination_link'])
            if url is None:
                url = url_obj.insert(data)

            data_alias = dict()
            data_alias['url_id'] = url.id
            # TODO split alias to other code block to easy maintenance
            data_alias['alias_name'] = '' if 'alias_name' not in payload else payload['alias_name'].strip()
            data_alias['alias_name'] = Helper.convert_space_to_dash(data_alias['alias_name'])
            url_alias = None
            if data_alias['alias_name'] != '':
                # check if alias belong to this url and count alias name, if count > 2 then return error message to ask client sign up new account
                total_alias = url_alias_obj.get_total_alias_name_by_destination_link(url.destination_link, cookie_uuid)
                if total_alias >= Constant.MAX_URL_ALIAS_NON_USER:
                    return {'message': 'Short URLs limit reached for this URL.',
                            'type': 'alias_name'}, Constant.HTTP_BAD_REQUEST

                url_alias = url_alias_obj.get_by_alias_name_cookie_uuid(data_alias['alias_name'], cookie_uuid)
                if url_alias and url_alias.alias_name == data_alias['alias_name']:
                    return {'message': 'Alias name is not available.', 'type': 'alias_name'}, Constant.HTTP_BAD_REQUEST
                else:
                    # Create a new one alias name
                    url_alias = url_alias_obj.insert(data_alias)
                    if url_alias is False:
                        # Error when insert alias name
                        return {'message': 'Invalid alias name'}, Constant.HTTP_BAD_REQUEST

            if url_alias:
                public_id = url_alias.alias_name if url_alias.alias_name is not None else url_alias.public_id
            else:
                url_alias = url_alias_obj.get_by_url_id_cookie_uuid(url.id, data_alias['cookie_uuid'])
                if url_alias is None:
                    url_alias = url_alias_obj.insert(data_alias)
                public_id = url_alias.public_id
            qrcode_base64 = URL_Helper.handler_qrcode(url_alias)

            return {
                'public_id': public_id,
                'short_link': Helper.return_link(public_id),
                'qrcode': Helper.get_qrcode_link(public_id),
                'qrcode_base64': qrcode_base64,
                'destination_logo': Helper.get_favicon_by_domain(url.destination_link, 32)
            }
        else:
            abort(Constant.HTTP_BAD_REQUEST, message="Invalid JSON")

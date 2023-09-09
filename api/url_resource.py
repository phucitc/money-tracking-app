from flask import request, abort
from flask_restful import Resource, reqparse

from classes.constant import Constant
from model.url import URL
from model.url_alias import URL_Alias
from py.auth_helper import check_csrf
from py.helper import Helper
from py.url_helper import URL_Helper


class URLResource(Resource):

    def __init__(self):
        # Define the request parser with the expected parameters
        self.parser = reqparse.RequestParser()

    @check_csrf
    def get(self):
        cookie_uuid = Helper.get_cookie(request, 'Zipit-Uuid')
        if cookie_uuid is None and 'Zipit-Uuid' in request.headers:
            cookie_uuid = request.headers['Zipit-Uuid']

        url_alias_model = URL_Alias()
        urls = url_alias_model.get_list_by_cookie_uuid(cookie_uuid)
        results = []
        for url in urls:
            data = {
                'long_url': Helper.remove_protocol(url.destination_link),
                'public_id': url.public_id,
                'short_url': Helper.return_link(url.public_id),
                'qrcode': Helper.get_qrcode_link(url.public_id),
                'qrcode_base64': URL_Helper.handler_qrcode(url),
                'destination_logo': Helper.get_favicon_by_domain(url.destination_link, 32)
            }
            results.append(data)

        return {'list_alias': results}

    @check_csrf
    def post(self):
        public_id = ''
        qrcode_base64 = ''
        list_alias = []
        cookie_uuid = Helper.get_cookie(request, 'Zipit-Uuid')
        if cookie_uuid is None and 'Zipit-Uuid' in request.headers:
            cookie_uuid =request.headers['Zipit-Uuid']
            print("zipit_uuid in request.headers", request.headers['zipit_uuid'])
        print('zipit_uuid', cookie_uuid)
        if request.is_json:
            payload = request.get_json()

            url_obj = URL()
            url_alias_obj = URL_Alias()
            data = dict()
            data['destination_link'] = payload['long_url'].strip()

            url = url_obj.get_by_destination_link(data['destination_link'])
            if url is None:
                url = url_obj.insert(data)

            public_id = url.public_id

            data = dict()
            data['url_public_id'] = public_id
            # TODO split alias to other code block to easy maintenance
            data['alias_name'] = '' if 'alias_name' not in payload else payload['alias_name'].strip()
            result = True
            if data['alias_name'] != '':
                # TODO need check code block again
                data['alias_name'] = Helper.convert_space_to_dash(data['alias_name'])
                # check if alias belong to this url and count alias name, if count > 2 then return error message to ask client sign up new account
                url_alias = url_obj.get_by_alias_name_or_public_id(data['alias_name'])
                if url_alias is not None:
                    if url_alias.url_public_id != public_id:
                        return {'message': 'Alias name is not available.', 'type': 'alias_name'}, Constant.HTTP_BAD_REQUEST
                    elif url_alias.url_public_id == public_id:
                        total_alias = url.get_total_alias_name_by_destination_link(url.destination_link)
                        if total_alias >= Constant.MAX_URL_ALIAS_NON_USER:
                            return {'message': 'Short URLs limit reached for this URL.', 'type': 'alias_name'}, Constant.HTTP_BAD_REQUEST
                else:
                    # Create a new one alias name
                    result = url_alias_obj.insert_no_return(data)
            if result is False:
                # Error when insert alias name
                return {'message': 'Invalid alias name'}, Constant.HTTP_BAD_REQUEST
            else:
                url_alias = url_alias_obj.get_by_url_id_cookie_uuid(url.id, cookie_uuid)
                if url_alias is None:
                    data_insert = dict()
                    data_insert['url_id'] = url.id
                    data_insert['cookie_uuid'] = cookie_uuid
                    url_alias = url_alias_obj.insert(data_insert)

                public_id = url_alias.public_id
                if url_alias.alias_name is not None:
                    public_id = url_alias.alias_name
                # condition = [
                #     {
                #         'column': 'url_id',
                #         'value': row.id
                #     }
                # ]
                # url_aliases = URL_Alias().get_all(condition)
                # for item in url_aliases:
                #     list_alias.append({'alias_name': return_link(item.alias_name)})

            qrcode_base64 = URL_Helper.handler_qrcode(url_alias)
        else:
            abort(Constant.HTTP_BAD_REQUEST, message="Invalid JSON")
        return {
            'public_id': public_id,
            'short_link': Helper.return_link(public_id),
            'qrcode': Helper.get_qrcode_link(public_id),
            'list_alias': list_alias,
            'qrcode_base64': qrcode_base64,
            'destination_logo': Helper.get_favicon_by_domain(url.destination_link, 32)
        }

    @staticmethod
    def handler_url_alias(url):
        list_alias = []
        return list_alias



from flask import request
from flask_restful import Resource

from classes.constant import Constant
from model.url_alias import URL_Alias
from model.user import User
from py.helper import Helper


class AuthResource(Resource):

    # def post(self):
    #     # process to sign up user
    #     print('Callback')
    #     print(request.args)
    #     token = request.headers.get('token')
    #     decode, code = decode_jwt(token)
    #     if code == 200:
    #         print(decode)
    #         return {'message': 'success'}, Constant.HTTP_OK
    #     else:
    #         return {'message': 'failed'}, Constant.HTTP_UNAUTHORIZED

        # access_token = 'eyJhbGciOiJkaXIiLCJlbmMiOiJBMjU2R0NNIiwiaXNzIjoiaHR0cHM6Ly9kZXYtZTBobjhidzRvc2c1MHdxei51cy5hdXRoMC5jb20vIn0..3pMDOdK3z0TcBRfJ.P4A9GFBQjmG1A0lzR3leGvWiq4A_5A4uKbqcJL4jxFS3rRT8xZXCewbOYN4nbJDTuzpWMymfWSERRCGVHKgWG8GBnhNT_cbml-Qf7TTrFPpv67ah1PpLnUoC-3NOJ6aHrcbEdNSwVJwvu8r1m8Tn6jUPwA5uYPxw9s_qyDKdFDVcPZ7zee94uisT3PXvJ0OXjIp1DwnUN82X7TUl3n0-fwtvCCp87gxTC04PxHHs6d9IMc8uMPllqjlPOam5fMzeH9VP1ZkZTsywQPdCGxF1AZ454WEDDjMDmkI2PvLzvRapzwwp64jUEU2NPf5ReGfIHzPmH9DKlUsCNQ2GOqcs15sw.2Cs8FSsoSj8kNdjbU8axAg'
        # results = requests.get('https://{domain}/userinfo?access_token={access_token}'.format(
        #     domain=current_app.config['AUTH0_API_DOMAIN'],
        #     access_token=access_token))
        # print(results.content)

    def post(self):
        # Sign up user
        auth_header = request.headers.get('Authorization')
        if auth_header:
            # Extract the token from the header
            token = auth_header.split()[1]  # Assuming 'Bearer <token>'
            if Helper.is_empty(token) is False:
                redirect_uri = ''
                decode, code = Helper.decode_auth0_jwt(token)
                if code == 200:
                    data = {
                        'email': decode['email'],
                    }
                    user = User().check_and_insert_user(data)
                    if user:
                        user_id = user.id
                        payload = request.get_json()
                        flow = payload.get('flow')
                        print('flow', flow)
                        if flow == 'signup':
                            cookie_uuid = Helper.get_cookie(request, 'Zipit-Uuid')
                            if cookie_uuid is None and 'Zipit-Uuid' in request.headers:
                                cookie_uuid = request.headers['Zipit-Uuid']
                                url_alias_model = URL_Alias()
                                list_url = url_alias_model.get_list_by_cookie_uuid(cookie_uuid)
                                for url in list_url:
                                    if url.user_id is None:
                                        url.update({'user_id': user_id, 'cookie_uuid': None})

                        # if decode['email'] in Constant.ADMIN_EMAILS:
                        #     redirect_uri = 'admin'
                        # else:
                        #     redirect_uri = 'dashboard'

                return {'redirect_uri': redirect_uri}
        return {'error': 'Unauthorized'}, Constant.HTTP_UNAUTHORIZED

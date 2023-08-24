from flask import request
from flask_restful import Resource

from classes.constant import Constant
from model.user import User
from py.helper import decode_jwt, is_empty, get_webapp_url


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
        auth_header = request.headers.get('Authorization')
        if auth_header:
            # Extract the token from the header
            token = auth_header.split()[1]  # Assuming 'Bearer <token>'
            if is_empty(token) is False:
                redirect_uri = ''
                decode, code = decode_jwt(token)
                if code == 200:
                    User().check_and_insert_user(decode['email'])
                    # if decode['email'] in Constant.ADMIN_EMAILS:
                    #     redirect_uri = 'admin'
                    # else:
                    #     redirect_uri = 'dashboard'

                return {'redirect_uri': redirect_uri}
        return {'error': 'Unauthorized'}, Constant.HTTP_UNAUTHORIZED

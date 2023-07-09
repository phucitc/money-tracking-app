import json

from flask import request, current_app
from flask_restful import Resource
from pip._vendor import requests


class AuthResource(Resource):

    def post(self):
        # process to sign up user
        print('Callback')
        print(request.args)
        auth0_code = request.args.get('auth0_code')
        auth0_code = "O2_9Z1YE7w3wCGd95JnJmuIxntP0d6eX1GK-VoT7ixgpy"

        # token_payload = {
        #     'client_id': current_app.config['AUTH0_API_CLIENT_ID'],
        #     'client_secret': current_app.config['AUTH0_API_CLIENT_SECRET'],
        #     'redirect_uri': current_app.config['AUTH0_API_CALLBACK_URL'],
        #     'code': auth0_code,
        #     'grant_type': 'authorization_code',
        #     # 'grant_type': 'client_credentials',
        #     # 'audience': 'https://dev-e0hn8bw4osg50wqz.us.auth0.com/api/v2/',
        # }
        # toke_url = 'https://{domain}/oauth/token'.format(domain=current_app.config['AUTH0_API_DOMAIN'])
        #
        # token_results = requests.post(toke_url,
        #                               data=json.dumps(token_payload),
        #                               headers={'content-type': 'application/json'}).json()
        # print(token_results)
        # if 'access_token' in token_results:
        access_token = 'eyJhbGciOiJkaXIiLCJlbmMiOiJBMjU2R0NNIiwiaXNzIjoiaHR0cHM6Ly9kZXYtZTBobjhidzRvc2c1MHdxei51cy5hdXRoMC5jb20vIn0..eKfgHjkI_QZ5Hnrz.2CDHtwGmX4-rpsJuXo39Y-maxeNSWrbXBPHUX17diw8hnwxm7q37wJxds522u9VcNzB72DaSidxCeCl8VEMmJFTpg0XpNscgDN1Jxj9GGypfHNC5O5fjDFxqGhOX2AbOI7KOBJnL7JaQSgki9gKEuVQrCkjPbOe2L8LkcuJlB7VxBLoBoLclk-qqH6ytlMmzUuECOrvNzHvaF8mfiJv9AaIHktswAmzQLR7LlfC_czffVh4WPg0LilfK70EB1rTqKfY1DtMFbO0Xu0JYTWNuSas1sPxQsiS1D3LuqMo4CPx7lBEkF6pS3i6PU7Eq-FiAhRJjjRAGxD1f6TjJCiqdrm8M.gXmE3N_Rncfg5rnobfkraw'
        results = requests.get('https://{domain}/userinfo?access_token={access_token}'.format(
            domain=current_app.config['AUTH0_API_DOMAIN'],
            access_token=access_token))
        print(results.content)

        return {'message': 'Callback'}

    def get(self):
        print('Callback GET')
        params = request.args
        print(params)
        return {'message': 'Callback GET'}

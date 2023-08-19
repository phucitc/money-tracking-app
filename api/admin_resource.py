from flask_restful import Resource, reqparse

from model.url import URL


class AdminResource(Resource):

    def __init__(self):
        # Define the request parser with the expected parameters
        self.parser = reqparse.RequestParser()

    def get(self, action):
        results = []
        if action == 'get-urls':
            urls = URL().get_all()
            for url in urls:
                results.append(url.data)

        return {
            'data': results,
            'message': 'URL get'
        }



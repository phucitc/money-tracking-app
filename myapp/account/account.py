import multiprocessing
import os
from urllib.parse import urlencode, quote_plus

from flask import Blueprint, render_template, redirect, send_file, request, make_response, jsonify, url_for, \
    current_app, session

from classes.constant import Constant
from model.url import URL
from model.url_alias import URL_Alias
from model.url_click import URL_Click
from model.user import User
from py.helper import Helper
from py.url_helper import URL_Helper

# VueJS need to build, then copy dist folder to this folder and rename to vuejs_webapp
account_blueprint = Blueprint('account', __name__, template_folder='templates')

@account_blueprint.route('/urls')
def page_urls():
    data = dict()
    return render_template('urls.html',
                           session=session,
                           data=data)

@account_blueprint.route('/gw/urls', methods=['GET'])
def get_urls():
    model_user = User()
    data = dict()
    user_id = session['user']['id']
    app_domain = Helper.app_domain()

    params = {
        'limit': request.args.get('limit', 100),
        'page': request.args.get('page', 1),
    }
    results = model_user.get_list_urls(user_id, **params)
    rows = []
    for item in results:
        del item['user_id']
        print(item)
        item['cloak_url'] = f"{app_domain}/{item['alias_name']}"
        rows.append(item)
    data['rows'] = rows
    return make_response(jsonify(data), 200)
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

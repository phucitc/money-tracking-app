import multiprocessing
import os

from flask import Blueprint, render_template, redirect, send_file, request

from classes.constant import Constant
from model.url import URL
from model.url_alias import URL_Alias
from model.url_click import URL_Click
from py.helper import Helper

# VueJS need to build, then copy dist folder to this folder and rename to vuejs_webapp
home_blueprint = Blueprint('homepage', __name__, template_folder='vuejs_webapp', static_folder='vuejs_webapp/assets')


@home_blueprint.route('/debug')
def debug():
    print("Debug")
    print(request.headers)
    return ''

@home_blueprint.route('/')
def index():
    print("HOME")
    hostname = request.host
    domain = hostname.split(':')[0]

    if Helper.alllow_domains(domain):
        return render_template('index.html')
    else:
        return 'Sorry! Access restricted.'


@home_blueprint.route('/<slug>')
def redirect_link(slug):
    print("slug", slug)
    if slug is not None:
        slug = slug.strip()
        # these are routes in VueJS
        if slug in Constant.VUEJS_PAGES:
            print("Here, return vueJS template")
            return render_template('index.html')

        print(f"Query DB to get destination_link {slug}")
        url_alias_model = URL_Alias()
        slug = slug.strip()
        url = url_alias_model.get_by_alias_name_or_public_id(slug)
        if url:
            # Process to track click here
            # Create a process for the background task
            params = {
                'url_alias_id': url.url_alias_id,
                'flask_request': request,
                'alias_name': slug
            }

            # Start the background process
            background_process = multiprocessing.Process(target=background_task_tracking_click(params))
            background_process.start()

            return redirect(url.destination_link, code=301)
        else:
            return render_template('index.html'), 404
    else:
        return render_template('index.html'), 404

@home_blueprint.route('/admin/<page_name>')
def admin_pages(page_name):
    print("Admin page name", page_name)
    if page_name in Constant.VUEJS_ADMIN_PAGES:
        return render_template('index.html')
    return render_template('index.html'), 404

@home_blueprint.route('/qrcode/<url_public_id>')
def download_qrcode(url_public_id):
    url_alias_model = URL_Alias()
    item = url_alias_model.get_by_alias_name_or_public_id(url_public_id)
    if item and Helper.is_empty(item.qrcode_path) is False:
        root_path = os.path.dirname(os.path.abspath(__file__))
        # go up multi level
        root_path = os.path.dirname(root_path)
        root_path = os.path.dirname(root_path)

        file_path = root_path + '/' + item.qrcode_path
        # check file exist
        if os.path.isfile(file_path) is False:
            Helper.create_simple_qrcode(Helper.return_link(url_public_id))

        print("file_path", file_path)
        filename = url_public_id + '-qrcode-image.png'
        return send_file(file_path, as_attachment=True, download_name=filename)
    else:
        return render_template('index.html'), 404

def background_task_tracking_click(params):
    # TODO Need improve performance by using queue
    flask_request = params['flask_request']
    user_agent = flask_request.headers.get('User-Agent')
    if Helper.is_crawler_bot(user_agent):
        return

    url_alias_id = params['url_alias_id']
    data = {
        'url_alias_id': url_alias_id,
        'user_agent': flask_request.headers.get('User-Agent'),
        'ip_address': flask_request.headers.get('X-Real-Ip', '127.0.0.1'),
        'referer': flask_request.headers.get('Referer', ''),
        'alias_name': params['alias_name'] if 'alias_name' in params else ''
    }
    URL_Click().insert(data)

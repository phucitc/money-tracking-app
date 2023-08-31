import multiprocessing
import os

from flask import Blueprint, render_template, redirect, send_file, request, make_response, session

from classes.constant import Constant
from model.url import URL
from model.url_click import URL_Click
from py.helper import is_empty, create_simple_qrcode, return_link, generate_uuid, generate_jwt, get_cookie, decode_jwt

# VueJS need to build, then copy dist folder to this folder and rename to vuejs_webapp
home_blueprint = Blueprint('homepage', __name__, template_folder='vuejs_webapp', static_folder='vuejs_webapp/assets')


@home_blueprint.route('/')
def index():
    print("HOME")
    return render_template('index.html')


@home_blueprint.route('/<slug>')
def redirect_link(slug):
    print("slug", slug)
    if slug is not None:
        # these are routes in VueJS
        if slug in Constant.VUEJS_PAGES:
            print("Here, return vueJS template")
            return render_template('index.html')

        print(f"Query DB to get destination_link {slug}")
        url = URL()
        slug = slug.strip()
        item = url.get_by_public_id(slug)
        if item:
            # Process to track click here
            # Create a process for the background task
            params = {
                'url_id': item.id,
                'flask_request': request
            }
            background_process = multiprocessing.Process(target=background_task_tracking_click(params))
            background_process.start()
            # Start the background process

            return redirect(item.destination_link, code=301)
        else:
            # Check if slug is alias
            print(f"Query DB to get alias {slug}")
            alias_name = slug
            url = URL().get_by_alias_name(alias_name)
            if url:
                # Create a process for the background task
                params = {
                    'url_id': url.id,
                    'flask_request': request,
                    'alias_name': alias_name
                }
                background_process = multiprocessing.Process(target=background_task_tracking_click(params))
                background_process.start()
                # Start the background process

                return redirect(url.destination_link, code=301)
            return render_template('index.html'), 404
    else:
        return 'No link'

@home_blueprint.route('/admin/<page_name>')
def admin_pages(page_name):
    print("Admin page name", page_name)
    if page_name in Constant.VUEJS_ADMIN_PAGES:
        return render_template('index.html')
    return render_template('index.html'), 404

@home_blueprint.route('/qrcode/<url_public_id>')
def download_qrcode(url_public_id):
    url = URL()
    item = url.get_by_public_id(url_public_id)
    if item and is_empty(item.qrcode_path) is False:
        root_path = os.path.dirname(os.path.abspath(__file__))
        # go up multi level
        root_path = os.path.dirname(root_path)
        root_path = os.path.dirname(root_path)

        file_path = root_path + '/' + item.qrcode_path
        # check file exist
        if os.path.isfile(file_path) is False:
            create_simple_qrcode(return_link(url_public_id))

        print("file_path", file_path)
        filename = 'qrcode-image.png'
        return send_file(file_path, as_attachment=True, download_name=filename)
    else:
        return render_template('index.html'), 404


@home_blueprint.route('/api/heartbeat')
def heartbeat():
    zipit_uuid = get_cookie(request, 'zipit_uuid')

    if zipit_uuid is None:
        print("VAO DAY NHA")
        zipit_uuid = generate_uuid()

    token_in_cookie = get_cookie(request, 'token')
    if token_in_cookie is None:
        token_in_cookie = generate_jwt(zipit_uuid)
        print("token_in_cookies", token_in_cookie)
    else:
        result = decode_jwt(token_in_cookie)
        if result is None:
            # Expired and need to generate new token
            token_in_cookie = generate_jwt(zipit_uuid)

    response = make_response()
    # response.set_cookie('zipit_token', token_in_cookie, secure=True, expires=) #5s
    # response.set_cookie('zipit_uuid', zipit_uuid, secure=True, samesite=)
    response.set_cookie('zipit_uuid', zipit_uuid, max_age=60 * 60 * 24 * 30)  # 30 days
    response.set_cookie('zipit_token', token_in_cookie, max_age=60 * 60 * 24 * 30)  # 30 days

    print("heartbeat")
    return response, 204


def background_task_tracking_click(params):
    # TODO Need improve performance by using queue
    url_id = params['url_id']
    flask_request = params['flask_request']
    data = {
        'url_id': url_id,
        'user_agent': flask_request.headers.get('User-Agent'),
        'ip_address': flask_request.remote_addr,
        'referer': flask_request.headers.get('Referer', ''),
        'alias_name': params['alias_name'] if 'alias_name' in params else ''
    }
    URL_Click().insert(data)

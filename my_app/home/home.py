import multiprocessing
import os

from flask import Blueprint, render_template, redirect, send_file, request, make_response, session, abort
from flask_wtf import CSRFProtect

from classes.constant import Constant
from model.url import URL
from model.url_alias import URL_Alias
from model.url_click import URL_Click
from py.helper import Helper
from py.url_helper import URL_Helper

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
            url = URL().get_by_alias_name_or_public_id(alias_name)
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
        filename = 'qrcode-image.png'
        return send_file(file_path, as_attachment=True, download_name=filename)
    else:
        return render_template('index.html'), 404

# @home_blueprint.route('/api/url/short-url', methods=['POST'])
# def create_short_url():
#     public_id = ''
#     qrcode_base64 = ''
#     list_alias = []
#     cookie_uuid = get_cookie(request, 'Zipit-Uuid')
#     if cookie_uuid is None and 'Zipit-Uuid' in request.headers:
#         cookie_uuid = request.headers['Zipit-Uuid']
#     if request.is_json:
#         payload = request.get_json()
#
#         url_obj = URL()
#         url_alias_obj = URL_Alias()
#         data = dict()
#         data['destination_link'] = payload['long_url'].strip()
#
#         url = url_obj.get_by_destination_link(data['destination_link'])
#         if url is None:
#             url = url_obj.insert(data)
#
#         public_id = url.public_id
#
#         data = dict()
#         data['url_public_id'] = public_id
#         # TODO split alias to other code block to easy maintenance
#         data['alias_name'] = payload['alias_name'].strip()
#         result = True
#         if data['alias_name'] != '':
#             # TODO need check code block again
#             data['alias_name'] = convert_space_to_dash(data['alias_name'])
#             # check if alias belong to this url and count alias name, if count > 2 then return error message to ask client sign up new account
#             url_alias = url_obj.get_by_alias_name_or_public_id(data['alias_name'])
#             if url_alias is not None:
#                 if url_alias.url_public_id != public_id:
#                     return {'message': 'Alias name is not available.', 'type': 'alias_name'}, Constant.HTTP_BAD_REQUEST
#                 elif url_alias.url_public_id == public_id:
#                     total_alias = url.get_total_alias_name_by_destination_link(url.destination_link)
#                     if total_alias >= Constant.MAX_URL_ALIAS_NON_USER:
#                         return {'message': 'Short URLs limit reached for this URL.',
#                                 'type': 'alias_name'}, Constant.HTTP_BAD_REQUEST
#             else:
#                 # Create a new one alias name
#                 result = url_alias_obj.insert_no_return(data)
#         if result is False:
#             # Error when insert alias name
#             return {'message': 'Invalid alias name'}, Constant.HTTP_BAD_REQUEST
#         else:
#             url_alias = url_alias_obj.get_by_url_id_cookie_uuid(url.id, cookie_uuid)
#             if url_alias is None:
#                 data_insert = dict()
#                 data_insert['url_id'] = url.id
#                 data_insert['cookie_uuid'] = cookie_uuid
#                 url_alias = url_alias_obj.insert(data_insert)
#
#             public_id = url_alias.public_id
#             if url_alias.alias_name is not None:
#                 public_id = url_alias.alias_name
#             # condition = [
#             #     {
#             #         'column': 'url_id',
#             #         'value': row.id
#             #     }
#             # ]
#             # url_aliases = URL_Alias().get_all(condition)
#             # for item in url_aliases:
#             #     list_alias.append({'alias_name': return_link(item.alias_name)})
#
#         qrcode_base64 = URL_Helper.handler_qrcode(url_alias)
#     else:
#         abort(Constant.HTTP_BAD_REQUEST, message="Invalid JSON")
#     return {
#         'short_link': return_link(public_id),
#         'qrcode': get_qrcode_link(public_id),
#         'list_alias': list_alias,
#         'qrcode_base64': qrcode_base64
#     }


# @home_blueprint.route('/api/url/short-url', methods=['POST'])
# def create_short_url():
#     public_id = ''
#     qrcode_base64 = ''
#     list_alias = []
#     # request.headers['X-Csrftoken']
#     print("request.headers", request.headers)
#
#     history_uuid = get_cookie(request, 'Zipit-Uuid')
#     if history_uuid is None and 'Zipit-Uuid' in request.headers:
#         history_uuid =request.headers['Zipit-Uuid']
#         print("zipit_uuid in request.headers", request.headers['zipit_uuid'])
#     if request.is_json:
#         payload = request.get_json()
#         # 1 Add new url
#         # 2 Add new alias
#         # 3 Add history
#         url = URL()
#         data = dict()
#         data['destination_link'] = payload['long_url'].strip()
#         row = url.get_by_destination_link(data['destination_link'])
#         if row is None:
#             row = url.insert(data)
#
#         url_alias = URL_Alias()
#
#         public_id = row.public_id
#
#         data = dict()
#         data['url_public_id'] = public_id
#         # TODO split alias to other code block to easy maintenance
#         data['alias_name'] = payload['alias_name'].strip()
#         result = True
#         if data['alias_name'] != '':
#             data['alias_name'] = convert_space_to_dash(data['alias_name'])
#             # check if alias belong to this url and count alias name, if count > 2 then return error message to ask client sign up new account
#             # Check history and alias name
#
#             url_alias = url.get_by_alias_name(data['alias_name'])
#             if url_alias is not None:
#                 if url_alias.url_public_id != public_id:
#                     return {'message': 'Alias name is not available.', 'type': 'alias_name'}, Constant.HTTP_BAD_REQUEST
#                 elif url_alias.url_public_id == public_id:
#                     total_alias = url.get_total_alias_name_by_destination_link(row.destination_link)
#                     if total_alias >= Constant.MAX_URL_ALIAS_NON_USER:
#                         return {'message': 'Short URLs limit reached for this URL.',
#                                 'type': 'alias_name'}, Constant.HTTP_BAD_REQUEST
#             else:
#                 # Create a new one alias name
#                 result = URL_Alias().insert_no_return(data)
#         if result is False:
#             return {'message': 'Invalid alias name'}, Constant.HTTP_BAD_REQUEST
#         else:
#             condition = [
#                 {
#                     'column': 'url_public_id',
#                     'value': public_id
#                 }
#             ]
#             url_aliases = URL_Alias().get_all(condition)
#             for item in url_aliases:
#                 list_alias.append({'alias_name': return_link(item.alias_name)})
#
#         qrcode_base64 = URL_Helper.handler_qrcode(row)
#     else:
#         abort(Constant.HTTP_BAD_REQUEST, message="Invalid JSON")
#     return {
#         'short_link': return_link(public_id),
#         'qrcode': get_qrcode_link(public_id),
#         'list_alias': list_alias,
#         'qrcode_base64': qrcode_base64
#     }


# @home_blueprint.route('/api/heartbeat')
# def heartbeat():
#     zipit_uuid = get_cookie(request, 'zipit_uuid')
#
#     if zipit_uuid is None:
#         print("VAO DAY NHA")
#         zipit_uuid = generate_uuid()
#
#     print('zipit_uuid', zipit_uuid)
#     # token_in_cookie = get_cookie(request, 'token')
#     # if token_in_cookie is None:
#     #     token_in_cookie = generate_jwt(zipit_uuid)
#     #     print("token_in_cookies", token_in_cookie)
#     # else:
#     #     result = decode_jwt(token_in_cookie)
#     #     if result is None:
#     #         # Expired and need to generate new token
#     #         token_in_cookie = generate_jwt(zipit_uuid)
#
#     response = make_response()
#     # response.set_cookie('zipit_token', token_in_cookie, secure=True, expires=) #5s
#     # response.set_cookie('zipit_uuid', zipit_uuid, secure=True, samesite=)
#     response.set_cookie('zipit_uuid', zipit_uuid, max_age=60 * 60 * 24 * 30)  # 30 days
#     # response.set_cookie('zipit_token', token_in_cookie, max_age=60 * 60 * 24 * 30)  # 30 days
#
#     print("heartbeat")
#     return response, 204


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

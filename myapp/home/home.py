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
home_blueprint = Blueprint('homepage', __name__, template_folder='templates')


@home_blueprint.route('/')
def index():
    print(session.get('user'))
    return render_template('home.html',
                           session=session)


@home_blueprint.route('/components')
def components():
    return render_template('components.html',
                           session=session)


@home_blueprint.route('/about')
def about():
    return render_template('about.html',
                           session=session)


@home_blueprint.route('/login')
def login():
    oauth = current_app.config['oauth']
    return oauth.auth0.authorize_redirect(
        redirect_uri=url_for("homepage.callback", _external=True)
    )


@home_blueprint.route('/signup')
def signup():
    oauth = current_app.config['oauth']
    return oauth.auth0.authorize_redirect(
        redirect_uri=url_for("homepage.callback", _external=True),
        screen_hint="signup"
    )


@home_blueprint.route('/logout')
def logout():
    session.clear()
    return redirect(
        "https://" + current_app.config["AUTH0_DOMAIN"]
        + "/v2/logout?"
        + urlencode(
            {
                "returnTo": url_for("homepage.index", _external=True),
                "client_id": current_app.config["AUTH0_CLIENT_ID"],
            },
            quote_via=quote_plus,
        )
    )


@home_blueprint.route('/callback',  methods=["GET", "POST"])
def callback():
    oauth = current_app.config['oauth']
    token = oauth.auth0.authorize_access_token()
    if token is None:
        return redirect(url_for("homepage.index"))
    else:
        data = {
            'email': token['userinfo']['email']
        }
        user = User().check_and_insert_user(data)
        session["auth0_token"] = token
        session["user"] = user

    return redirect(url_for("homepage.index"))


@home_blueprint.route('/zip-url', methods=['POST'])
def zip_url():
    list_alias = []
    cookie_uuid = Helper.get_cookie(request, 'Zipit-Uuid')
    if cookie_uuid is None and 'Zipit-Uuid' in request.headers:
        cookie_uuid = request.headers['Zipit-Uuid']
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

        data_alias = dict()
        data_alias['url_id'] = url.id
        data_alias['cookie_uuid'] = cookie_uuid
        # TODO split alias to other code block to easy maintenance
        data_alias['alias_name'] = '' if 'alias_name' not in payload else payload['alias_name'].strip()
        data_alias['alias_name'] = Helper.convert_space_to_dash(data_alias['alias_name'])
        url_alias = None
        if data_alias['alias_name'] != '':
            # check if alias belong to this url and count alias name, if count > 2 then return error message to ask client sign up new account
            total_alias = url_alias_obj.get_total_alias_name_by_destination_link(url.destination_link, cookie_uuid)
            if total_alias >= Constant.MAX_URL_ALIAS_NON_USER:
                return {'message': 'Short URLs limit reached for this URL.',
                        'type': 'alias_name'}, Constant.HTTP_BAD_REQUEST

            url_alias = url_alias_obj.get_by_alias_name_cookie_uuid(data_alias['alias_name'], cookie_uuid)
            if url_alias and url_alias.alias_name == data_alias['alias_name']:
                return {'message': 'Alias name is not available.', 'type': 'alias_name'}, Constant.HTTP_BAD_REQUEST
            else:
                # Create a new one alias name
                url_alias = url_alias_obj.insert(data_alias)
                if url_alias is False:
                    # Error when insert alias name
                    return {'message': 'Invalid alias name'}, Constant.HTTP_BAD_REQUEST

        if url_alias:
            public_id = url_alias.alias_name if url_alias.alias_name is not None else url_alias.public_id
        else:
            url_alias = url_alias_obj.get_by_url_id_cookie_uuid(url.id, data_alias['cookie_uuid'])
            if url_alias is None:
                url_alias = url_alias_obj.insert(data_alias)
            public_id = url_alias.public_id
        qrcode_base64 = URL_Helper.handler_qrcode(url_alias)
        url_aliases = url_alias_obj.get_list_by_cookie_uuid(cookie_uuid, url_id=url.id)
        for item in url_aliases:
            # Ignore current alias name
            if item.public_id != public_id:
                list_alias.append({'alias_name': Helper.return_link(item.alias_name)})

        response = {
            'public_id': public_id,
            'short_link': Helper.return_link(public_id),
            'qrcode': Helper.get_qrcode_link(public_id),
            'list_alias': list_alias,
            'qrcode_base64': qrcode_base64,
            'destination_logo': Helper.get_favicon_by_domain(url.destination_link, 32)
        }
        return make_response(jsonify(response), Constant.HTTP_OK)
    else:
        return make_response(jsonify({'message': 'Invalid request'}), Constant.HTTP_BAD_REQUEST)



# @home_blueprint.route('/<slug>')
# def redirect_link(slug):
#     print("slug", slug)
#     if slug is not None:
#         slug = slug.strip()
#         # these are routes in VueJS
#         if slug in Constant.VUEJS_PAGES:
#             print("Here, return vueJS template")
#             return render_template('index.html')
#
#         print(f"Query DB to get destination_link {slug}")
#         url_alias_model = URL_Alias()
#         slug = slug.strip()
#         url = url_alias_model.get_by_alias_name_or_public_id(slug)
#         if url:
#             # Process to track click here
#             # Create a process for the background task
#             params = {
#                 'url_alias_id': url.url_alias_id,
#                 'flask_request': request,
#                 'alias_name': slug
#             }
#
#             # Start the background process
#             background_process = multiprocessing.Process(target=background_task_tracking_click(params))
#             background_process.start()
#
#             return redirect(url.destination_link, code=301)
#         else:
#             return render_template('index.html'), 404
#     else:
#         return render_template('index.html'), 404


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
    real_ip = flask_request.headers.get('Cf-Connecting-Ip')  # Cloudflare proxy
    country = flask_request.headers.get('Cf-Ipcountry', '')  # Cloudflare proxy
    if real_ip is None:
        real_ip = flask_request.remote_addr

    data = {
        'url_alias_id': url_alias_id,
        'user_agent': flask_request.headers.get('User-Agent'),
        'ip_address': real_ip,
        'referer': flask_request.headers.get('Referer', ''),
        'alias_name': params['alias_name'] if 'alias_name' in params else '',
        'country': country
    }
    URL_Click().insert(data)

import os

from flask import Blueprint, render_template, redirect, send_file

from classes.constant import Constant
from model.url import URL
from model.url_alias import URL_Alias
from py.helper import is_empty, create_simple_qrcode, return_link

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
            return redirect(item.destination_link, code=301)
        else:
            # Check if slug is alias
            print(f"Query DB to get alias {slug}")
            alias_name = slug
            url = URL().get_by_alias_name(alias_name)
            if url:
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

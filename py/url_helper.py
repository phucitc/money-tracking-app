import base64
from PIL import Image
from io import BytesIO


class URL_Helper:
    @staticmethod
    def handler_qrcode(url):
        from py.helper import Helper
        # url is URL object
        if Helper.is_empty(url.qrcode_path):
            qrcode_path = Helper.create_simple_qrcode(Helper.return_link(url.public_id))
            url.qrcode_path = qrcode_path
            url.update({'qrcode_path': qrcode_path})

        qrcode_file_path = Helper.get_root_path() + '/' + url.qrcode_path
        img = Image.open(qrcode_file_path)
        buffered = BytesIO()
        img.save(buffered, format="PNG")
        qrcode_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')
        return 'data:image/png;base64,' + qrcode_base64

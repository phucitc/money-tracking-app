
from model.url import URL
from dotenv import load_dotenv
load_dotenv()
url = URL()
item = url.get_by_public_id('TFBJK')
print(item.qrcode_path)

from model.model import Model


class URL_History(Model):
    TABLE = 'url_histories'
    COLS_IGNORE = ['id']
    COLS_EXE_FCT = []
    PUBLIC_ID_LENGTH = 5
    CACHED = {}

    def __init__(self):
        params = {
            'table_name': self.TABLE
        }
        super().__init__(**params)

    def get_by_cookie_uuid(self, cookie_uuid):
        return self.get_by_field('cookie_uuid', cookie_uuid)


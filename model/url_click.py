from model.model import Model


class URL_Click(Model):
    TABLE = 'url_clicks'
    COLS_IGNORE = ['id', 'created_at']
    COLS_EXE_FCT = []
    PUBLIC_ID_LENGTH = 5

    def __init__(self):
        params = {
            'table_name': self.TABLE
        }
        super().__init__(**params)

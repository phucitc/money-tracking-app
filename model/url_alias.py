from model.model import Model

class URL_Alias(Model):
    TABLE = 'url_aliases'
    COLS_IGNORE = ['created_at', 'updated_at']
    COLS_EXE_FCT = []
    PUBLIC_ID_LENGTH = 5

    def __init__(self):
        params = {
            'table_name': self.TABLE
        }
        super().__init__(**params)


from model.db import DB


class URL(DB):
    TABLE = 'urls'
    IGNORE_COLUMNS = ['created_at', 'updated_at']

    def __init__(self):
        params = {
            'table_name': self.TABLE
        }
        super().__init__(**params)

from model.db import DB


class User(DB):
    TABLE = 'users'
    COLS_IGNORE = ['user_id', 'created_at', 'updated_at']

    def __init__(self):
        params = {
            'table_name': self.TABLE
        }
        super().__init__(**params)

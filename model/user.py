from model.db import DB


class User(DB):
    TABLE = 'users'

    def __init__(self):
        params = {
            'table_name': self.TABLE
        }
        super().__init__(**params)

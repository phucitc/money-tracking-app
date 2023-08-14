from model.db import DB
from py.helper import calculate_md5_hash


class URL(DB):
    TABLE = 'urls'
    COLS_IGNORE = []
    COLS_EXE_FCT = ['public_id']
    PUBLIC_ID_LENGTH = 5

    def __init__(self):
        params = {
            'table_name': self.TABLE
        }
        super().__init__(**params)

    def insert(self, data):
        # public_id column generated by generate_public_id('urls'::text, 5) function so no need to insert
        data['public_id'] = f"generate_public_id('{self.TABLE}'::text, {self.PUBLIC_ID_LENGTH})"
        data['destination_link_hash'] = calculate_md5_hash(data['destination_link'])
        return super().insert(data)

    def get_by_destination_link(self, destination_link):
        destination_link_hash = calculate_md5_hash(destination_link)
        return self.get_by_field('destination_link_hash', destination_link_hash)

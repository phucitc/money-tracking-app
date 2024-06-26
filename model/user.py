from model.model import Model

class User(Model):
    TABLE = 'users'
    COLS_IGNORE = ['id', 'created_at', 'updated_at']
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
        return super().insert(data)

    def get_by_email(self, email):
        return self.get_by_field('email', email)

    def check_and_insert_user(self, data):
        user = self.get_by_email(data['email'])
        if user is None:
            user = self.insert(data)
        return user.get_data() if user else None

    def update(self, params):
        return super().update(params)

    def get_list_urls(self, user_id, **kwargs):
        page = kwargs.get('page', 1)
        limit = kwargs.get('limit', 100)
        offset = self.get_offset(page, limit)
        query = """
            SELECT
                ua.id,
                ua.user_id,
                ua.public_id,
                ua.qrcode_path,
                u.destination_link,
                CASE
                    WHEN ua.alias_name IN (NULL, '') THEN ua.public_id
                    ELSE ua.alias_name
				END AS alias_name
            FROM url_aliases ua
                LEFT JOIN urls u
                    ON u.id = ua.url_id 
            WHERE
                ua.user_id= %(user_id)s
            ORDER BY ua.created_at DESC
            LIMIT %(limit)s OFFSET %(offset)s
        """
        params = {
            'user_id': user_id,
            'limit': limit,
            'offset': offset
        }
        return self.get_plsql().fetch(query, params=params)
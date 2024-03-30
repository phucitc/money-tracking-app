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
        query = """
            SELECT
                *
            FROM
                url_aliases
            WHERE
                user_id = %s
            LIMIT %s OFFSET %s
        """
        params = [user_id, kwargs.get('limit', 100), kwargs.get('offset', 0)]
        return self.get_plsql().fetch(query, params=params)
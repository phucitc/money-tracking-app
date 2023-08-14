# DB class
import os

import psycopg2
from psycopg2.extras import RealDictCursor


class DB:
    COLS_EXE_FCT = []
    COLS_IGNORE = []

    def __init__(self, **kwargs):
        try:
            print(os.getenv('DWH'))
            self.connection = psycopg2.connect(os.getenv('DWH'))
            self.cursor = self.connection.cursor(cursor_factory=RealDictCursor)
            self.table_name = kwargs.get('table_name')
            self.columns = dict()
            self.data = dict()
            print('Connected to DB')
        except Exception as e:
            print(e)

    def get_columns(self):
        if self.table_name:
            query = f"SELECT column_name, data_type FROM information_schema.columns WHERE table_name = '{self.table_name}'"
            self.cursor.execute(query)

            # Fetch all column information as a list of tuples (column_name, data_type)
            results = self.cursor.fetchall()
            for row in results:
                self.columns[row['column_name']] = {
                    'type': row['data_type'],
                }
            return self.columns
        else:
            print('No table name provided')

    def insert(self, params):
        try:
            if len(params) == 0 or not isinstance(params, dict):
                raise Exception('No data to insert or data is not a dictionary')

            input_columns = set(params.keys())

            default_columns = self.get_columns()
            default_columns_name = default_columns.keys()
            return_columns_after_insert = default_columns_name

            default_columns_name = default_columns_name - set(self.COLS_IGNORE)

            invalid_columns = input_columns - default_columns_name
            # columns that are not in the table. Raise exception
            if len(invalid_columns):
                raise Exception(f'Invalid column(s): {invalid_columns}')

            return_columns_after_insert = ', '.join(return_columns_after_insert)
            columns_to_insert = ', '.join(params)
            holder = ''
            for key in params:
                if key in self.COLS_EXE_FCT:
                    holder += f"{params[key]},"
                else:
                    holder += f"%({key})s,"
            holder = holder[:-1]  # remove last comma

            query = f"INSERT INTO {self.table_name} ({columns_to_insert}) VALUES ({holder}) RETURNING {return_columns_after_insert}"
            self.execute(query, params=params)
            inserted_row = self.cursor.fetchone()
            self.data = inserted_row
            self.connection.commit()
            return self

        except Exception as e:
            print(e)
            return False

    def update(self, params):
        try:
            if len(params) == 0 or not isinstance(params, dict):
                raise Exception('No data to update or data is not a dictionary')

            return_columns_after_update = self.data.keys()
            return_columns_after_update = ', '.join(return_columns_after_update)
            holder = ''
            for key in params:
                if key in self.COLS_EXE_FCT:
                    continue
                else:
                    holder += f"{key} = %({key})s,"
            holder = holder[:-1]  # remove last comma

            query = f"UPDATE {self.table_name} SET {holder} WHERE id = {self.id} RETURNING {return_columns_after_update}"
            self.execute(query, params=params)
            updated_row = self.cursor.fetchone()
            self.data = updated_row
            self.connection.commit()
            return updated_row

        except Exception as e:
            print(e)
            return False

    def execute(self, query, params=None):
        try:
            self.cursor.execute(query, params)
            self.connection.commit()
        except Exception as e:
            print(e)
            return False

    def fetch(self, query):
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def fetch_one(self, query, params=None):
        self.cursor.execute(query, params)
        return self.cursor.fetchone()

    def close(self):
        self.cursor.close()
        self.connection.close()

    def get_by_field(self, field, value):
        query = 'SELECT * FROM {table_name} WHERE {field} = %(value)s'.format(table_name=self.table_name, field=field)
        params = {
            'value': value
        }
        row = self.fetch_one(query, params=params)
        if row:
            self.data = row
            return self
        return None

    def get_by_public_id(self, public_id):
        return self.get_by_field('public_id', public_id)

    def convert_row_to_dict(self, row):
        return dict(row)

    def __getattr__(self, column_name):
        if column_name in self.data:
            return self.data[column_name]
        return None

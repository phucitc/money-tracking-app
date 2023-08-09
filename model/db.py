# DB class
import os

import psycopg2
from psycopg2.extras import RealDictCursor

class DB:
    COLS_EXE_FCT = []
    COLS_IGNORE = []
    def __init__(self, **kwargs):
        try:
            self.connection = psycopg2.connect(os.getenv('DWH'))
            self.cursor = self.connection.cursor(cursor_factory=RealDictCursor)
            self.table_name = kwargs.get('table_name')
            self.columns = dict()
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

    def insert(self, data):
        try:
            if len(data) == 0 or not isinstance(data, dict):
                raise Exception('No data to insert or data is not a dictionary')

            input_columns = set(data.keys())

            default_columns = self.get_columns()
            default_columns_name = default_columns.keys()
            return_columns_after_insert = default_columns_name

            default_columns_name = default_columns_name - set(self.COLS_IGNORE)

            invalid_columns = input_columns - default_columns_name
            if len(invalid_columns):
                raise Exception(f'Invalid column(s): {invalid_columns}')

            return_columns_after_insert = ', '.join(return_columns_after_insert)
            columns_to_insert = ', '.join(data)
            holder = ''
            for key in data:
                if key in self.COLS_EXE_FCT:
                    holder += f"{data[key]},"
                else:
                    holder += f"%({key})s,"
            holder = holder[:-1]

            query = f"INSERT INTO {self.table_name} ({columns_to_insert}) VALUES ({holder}) RETURNING {return_columns_after_insert}"
            self.execute(query, params=data)
            inserted_row = self.cursor.fetchone()
            self.connection.commit()
            return inserted_row

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
        data = {
            'value': value
        }
        return self.fetch_one(query, params=data)

    def get_by_public_id(self, public_id):
        return self.get_by_field('public_id', public_id)



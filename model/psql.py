import os
import urllib.parse

import psycopg2
from psycopg2.extras import RealDictCursor


class PSQL:

    def __init__(self):
        try:
            # parse connection string
            DB_URL = urllib.parse.urlparse(os.getenv('DWH'))
            self.connection = psycopg2.connect(
                database=DB_URL.path[1:],
                user=DB_URL.username,
                password=DB_URL.password,
                host=DB_URL.hostname,
                port=DB_URL.port
            )
            self.cursor = self.connection.cursor(cursor_factory=RealDictCursor)
            print('Connected to DB')
        except Exception as e:
            print(e)
            print('Can not connect to DB')

    def get_columns(self, table_name=None):
        if table_name:
            columns = dict()
            query = f"SELECT column_name, data_type FROM information_schema.columns WHERE table_name = '{table_name}'"
            self.cursor.execute(query)

            # Fetch all column information as a list of tuples (column_name, data_type)
            results = self.cursor.fetchall()
            for row in results:
                columns[row['column_name']] = {
                    'type': row['data_type'],
                }
            return columns
        else:
            print('No table name provided')

    def fetch(self, query, params=None):
        self.cursor.execute(query, params)
        return self.cursor.fetchall()

    def fetch_one(self, query, params=None):
        self.cursor.execute(query, params)
        return self.cursor.fetchone()

    def close(self):
        self.cursor.close()
        self.connection.close()

    def execute(self, query, params=None):
        try:
            print(params)
            self.cursor.execute(query, params)
            self.connection.commit()
            return True
        except Exception as e:
            print(e)
            return False

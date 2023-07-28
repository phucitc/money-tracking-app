# DB class
import os

import psycopg2
from psycopg2.extras import RealDictCursor



class DB:
    def __init__(self, **kwargs):
        try:
            self.connection = psycopg2.connect(os.environ['DWH'])
            self.cursor = self.connection.cursor(cursor_factory=RealDictCursor)
            self.table_name = kwargs.get('table_name')
            self.columns = []
            print('Connected to DB')
        except Exception as e:
            print(e)

    def get_columns(self):
        if self.table_name:
            query = f"SELECT column_name FROM information_schema.columns WHERE table_name = '{self.table_name}'"
            self.cursor.execute(query)

            # Fetch all column information as a list of tuples (column_name, data_type)
            results = self.cursor.fetchall()
            for row in results:
                self.columns.append(row['column_name'])
        else:
            print('No table name provided')

    def insert(self, data):
        try:
            # TODO
            # need to check if data is a dict and validate columns in data with self.columns
            columns = data.keys()
            columns = ', '.join(columns)
            values = ', '.join([f"'{value}'" for value in data.values()])
            query = f"INSERT INTO {self.table_name} ({columns}) VALUES ({values})"
            self.execute(query)
        except Exception as e:
            print(e)

    def execute(self, query):
        self.cursor.execute(query)
        self.connection.commit()

    def fetch(self, query):
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def close(self):
        self.cursor.close()
        self.connection.close()
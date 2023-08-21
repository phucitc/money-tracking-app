# Model class
from model.psql import PSQL


class Model:
    COLS_EXE_FCT = []
    COLS_IGNORE = []

    def __init__(self, **kwargs):
        self.table_name = kwargs.get('table_name')
        self.columns = dict()
        self.data = dict()
        self.psql = None

    def insert(self, params):
        try:
            if len(params) == 0 or not isinstance(params, dict):
                raise Exception('No data to insert or data is not a dictionary')

            input_columns = set(params.keys())

            default_columns = self.get_plsql().get_columns(self.table_name)
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

            query = f"INSERT INTO {self.TABLE} ({columns_to_insert}) VALUES ({holder}) RETURNING {return_columns_after_insert}"
            self.psql.execute(query, params=params)
            inserted_row = self.psql.cursor.fetchone()
            self.data = inserted_row
            self.psql.connection.commit()
            return self

        except Exception as e:
            print(e)
            return False

    def get_plsql(self):
        if self.psql is None:
            self.psql = PSQL()
        return self.psql

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
            self.get_plsql().execute(query, params=params)
            updated_row = self.get_plsql().cursor.fetchone()
            self.data = updated_row
            self.get_plsql().connection.commit()
            return updated_row

        except Exception as e:
            print(e)
            return False

    def get_by_field(self, field, value):
        query = 'SELECT * FROM {table_name} WHERE {field} = %(value)s'.format(table_name=self.table_name, field=field)
        params = {
            'value': value
        }
        row = self.get_plsql().fetch_one(query, params=params)
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

    def get_all(self, limit=100, offset=0):
        query = f"SELECT * FROM {self.TABLE} LIMIT {limit} OFFSET {offset}"
        rows = self.get_plsql().fetch(query)
        results = []
        for row in rows:
            original_class = self.__class__
            inst = original_class()
            if 'created_at' in row:
                row['created_at'] = row['created_at'].strftime('%Y-%m-%d %H:%M:%S')
            if 'updated_at' in row:
                row['updated_at'] = row['updated_at'].strftime('%Y-%m-%d %H:%M:%S')
            inst.data = row
            results.append(inst)
        return results
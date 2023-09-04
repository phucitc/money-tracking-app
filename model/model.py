# Model class
from model.psql import PSQL


class Model:
    COLS_EXE_FCT = []
    COLS_IGNORE = []
    CACHE = {}

    def __init__(self, **kwargs):
        self.table_name = kwargs.get('table_name')
        self.columns = dict()
        self.data = dict()
        self.psql = None

    def insert_no_return(self, params):
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

            query = f"INSERT INTO {self.TABLE} ({columns_to_insert}) VALUES ({holder}) ON CONFLICT DO NOTHING"
            return self.psql.execute(query, params=params)

        except Exception as e:
            print(e)
            return False

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

    def get_plsql(self, force=False):
        if force is False and 'psql' in self.CACHE:
            print('Using cached psql')
            self.psql = self.CACHE['psql']
            print('psql 111', self.psql.cursor.closed)
            if self.psql.cursor.closed is True:
                return self.get_plsql(force=True)

        if force is True or self.psql is None:
            print('psql 222', force)
            self.psql = PSQL()
            self.CACHE['psql'] = self.psql
            print('psql 333', self.psql.cursor.closed)

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

    def get_condition_query(self, conditions):
        params = []
        where = 'WHERE 1=1 '
        query = ''
        for condition in conditions:
            if 'column' not in condition:
                raise Exception('Column name is required. Payload should be like: [{"column": "name", "value": "John"}]')

            query += 'AND {column} = %({column})s '.format(column=condition['column'])
            params.append({
                condition['column']: condition['value']
            })
        return where + query, params

    def get_all(self, conditions=None, limit=100, offset=0):
        where, params = self.get_condition_query(conditions)

        # merge params to one dict
        params = {k: v for d in params for k, v in d.items()}

        query = f"SELECT * FROM {self.TABLE} {where} LIMIT {limit} OFFSET {offset}"
        rows = self.get_plsql().fetch(query, params=params)
        results = []
        for row in rows:
            original_class = self.__class__
            inst = original_class()
            if 'created_at' in row and row['created_at'] is not None:
                row['created_at'] = row['created_at'].strftime('%Y-%m-%d %H:%M:%S')
            if 'updated_at' in row and row['updated_at'] is not None:
                row['updated_at'] = row['updated_at'].strftime('%Y-%m-%d %H:%M:%S')
            inst.data = row
            results.append(inst)
        return results

    def get_by_conditions(self, conditions=None):
        where, params = self.get_condition_query(conditions)
        # merge params to one dict
        params = {k: v for d in params for k, v in d.items()}

        query = f"SELECT * FROM {self.TABLE} {where}"
        row = self.get_plsql().fetch_one(query, params=params)
        if row:
            self.data = row
            return self
        return None

    def fetch_one(self, query, params=None):
        return self.get_plsql().fetch_one(query, params=params)
    

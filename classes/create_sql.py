from datetime import datetime, timedelta, date
import itertools as itr
import numpy as np

"""
check_table_variable
check_nonetype --> check_unknown_type
check_strings 
check_max_length --> adjust_character_length
make_file
"""

class Create_SQL():
    def __init__(self, filename, entries, header, filepath=''):
        self.float_tuple = (float, np.float16, np.float32, np.float64)
        self.int_tuple = (int, np.int8, np.int16, np.int32, np.int64)
        self.NoneType = type(None)
        
        if filepath == '':
            filepath = 'sql_files/'
        
        self.filename = filename
        self.filepath = filepath
        self.entries = entries
        self.header = header
        
        self.initiate()

    def initiate(self):
        self.check_table_datatype()

        self.check_nonetype()
        self.check_date()
        self.check_string_length()

        self.make_file()

    def universal_checks(self, variable_type, value):
        if variable_type in self.int_tuple:
            return 'int'
        elif variable_type in self.float_tuple:
            return 'real'
        elif variable_type is date:
            return 'date'
        elif variable_type is str:
            return self.check_if_date(value)
        elif variable_type is bytes:
            return 'bytea'
        elif variable_type is self.NoneType:
            return 'Nonetype'
        else:
            return 'character varying(50)'
    
    def check_if_date(self, entry):
        try:
            datetime.strptime(entry, '%Y-%m-%d')
        except:
            return'character varying(50)'
        else:
            return 'date'
    
    def check_table_datatype(self):
        self.data_types = []
        for idx, i in enumerate(map(type, self.entries[0])):
            type_str = self.universal_checks(i, self.entries[0][idx])
            self.data_types.append(type_str)
    
    def get_type_idx(self, variable):
        idx_list = []
        for idx, i in enumerate(self.data_types):
            if i == variable:
                idx_list.append(idx)       
        
        return idx_list
        
    def check_nonetype(self):
        none_list = self.get_type_idx('Nonetype')
        for idx in none_list:
            for i in self.entries:
                I = i[idx]
                if type(I) != self.NoneType:
                    self.data_types[idx] = self.universal_checks(type(I), I)
                    break
    
    def check_date(self):
        date_idx = self.get_type_idx('date')
        for i, j in itr.product(date_idx, range(len(self.entries))):
            try:
                self.entries[j][i] = self.entries[j][i].strftime('%Y-%m-%d')
            except:
                pass

    def check_string_length(self):
        str_locations = self.get_type_idx('character varying(50)')
        for idx, i in enumerate(str_locations):
            length = 0
            
            for j in self.entries:
                string_length = len(str(j[i]))

                if string_length > length:
                    length = string_length
            
            self.data_types[i] = self.data_types[i].replace('50', str(length))
    
    def make_table_string(self):
        n = len(self.data_types) - 1
        table_str = ''
        
        zipped_list = zip(self.header, self.data_types)
        for idx, (name, variable) in enumerate(zipped_list):
            if idx != n:
                string = f'\t{name} {variable},\n'
            else:
                string = f'\t{name} {variable}\n'
            
            table_str += string
        return table_str
    
    def make_file(self, sql_str=''):
        table_str = self.make_table_string()
        
        sql_str += f'DROP TABLE IF EXISTS {self.filename};\n\n'
        sql_str += f'CREATE TABLE {self.filename} (\n{table_str});\n'
        insert_str = f'\nINSERT INTO {self.filename} VALUES'
        
        for i in self.entries:
            sql_str += f'{insert_str} {tuple(i)};'
        
        sql_str = sql_str.replace('None', 'NULL')
        sql_str = sql_str.replace("b''", "'\\x'")

        with open(self.filepath + self.filename + '.sql', 'w') as sql:
            sql.write(sql_str)

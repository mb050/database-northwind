from datetime import datetime, date
import itertools as itr
import numpy as np

class Create_SQL():
    """
    takes in a nested list and writes a sql file with the elements.
    
    attributes:
        filename: filename to use.
        entries: the nested list to write to the file.
        header: the column names.
        filepath: filepath to write the file to.
    
    methods:
        initiate: initiates necessary methods automatically.
        universal_checks: check what type a given entry in is.
        check_if_date: check if an entry is a valid datetime type.
        check_table_datatype: check what type the elements in a row is.
        get_type_idx: checks the location of a given type in the row.
        check_nonetype: goes through a column noted as Nonetype to check the
                        other entries for what the type is supposed to be.
        check_date: checks if date is formatted correctly.
        check_string_length: checks the max length for the strings
                             in a given column.
        make_table_string: creates the string with which datatype and names
                           the table contains for the sql file.
        make_file: writes the entries to the file.
    """
    def __init__(self, filename, entries, header, filepath=''):
        """
        defines instances and starts the initiate method.
        """
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
        """
        initiates standard procedure.
        """
        self.check_table_datatype()

        self.check_nonetype()
        self.check_date()
        self.check_string_length()

        self.make_file()

    def universal_checks(self, variable_type, value):
        """
        takes in single variable, and check which type it is.
        
        args:
            variable_type: the variable to check the type.
            value (str): entry in a row to check if it is a valid datetype.
        
        return:
            type class. 
        """
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
        """
        check if an entry is a valid datetype.
        
        args:
            entry (str): entry to check.
        
        return:
            string or date.
        """
        try:
            datetime.strptime(entry, '%Y-%m-%d')
        except:
            return'character varying(50)'
        else:
            return 'date'
    
    def check_table_datatype(self):
        """
        takes the first row from the table and check which type each element
        is. It is then stored to data_types.
        """
        self.data_types = []
        for idx, i in enumerate(map(type, self.entries[0])):
            type_str = self.universal_checks(i, self.entries[0][idx])
            self.data_types.append(type_str)
    
    def get_type_idx(self, variable):
        """
        check the location, or column of a given type.
        
        args:
            variable (str): which type to look for.
        
        return:
            idx_list (list): list with the location of the given type.
        """
        idx_list = []
        for idx, i in enumerate(self.data_types):
            if i == variable:
                idx_list.append(idx)       
        
        return idx_list
        
    def check_nonetype(self):
        """
        if a column is defined as Nonetype then it goes through the entries in
        the column to look for entries that can be used to define what type
        the column contains.
        """
        none_list = self.get_type_idx('Nonetype')
        for idx in none_list:
            for i in self.entries:
                I = i[idx]
                if type(I) != self.NoneType:
                    self.data_types[idx] = self.universal_checks(type(I), I)
                    break
    
    def check_date(self):
        """
        check if the dates in a column is the correct format, and corrects
        it along the way.
        """
        date_idx = self.get_type_idx('date')
        for i, j in itr.product(date_idx, range(len(self.entries))):
            try:
                self.entries[j][i] = self.entries[j][i].strftime('%Y-%m-%d')
            except:
                pass

    def check_string_length(self):
        """
        checks the max length for the strings in a given column. The default
        length will be adjusted to the max length.           
        """
        str_locations = self.get_type_idx('character varying(50)')
        for idx, i in enumerate(str_locations):
            length = 0
            
            for j in self.entries:
                string_length = len(str(j[i]))

                if string_length > length:
                    length = string_length
            
            self.data_types[i] = self.data_types[i].replace('50', str(length))
    
    def make_table_string(self):
        """
        creates the first section of the sql file which defines the table name,
        what datatype it contains, and other necessary info along with it.
        """
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
        """
        write the table to the sql file, in the correct format.
        
        args:
            sql_str (str): empty string in case additional info should be
                           written to the file.
        """
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

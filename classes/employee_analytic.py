from classes.create_sql import Create_SQL
from django.db.models import Count
from classes.base import Base
import numpy as np

class Employee_analytic(Base):
    """
    create table related to employee queries and tables.
    
    attributes:
        class_obj: class object from Base for more specific functions or
                   instances.
    
    methods:
        initiate_setup: method to automatically initiate necessary methods
        setup: create dictionary with relevant info for the employees
        get_full_analysis: retrieves relevant information and creates a table
        combine_table: combine lists into a singular list
        make_table: creates table and write result into sql file
    """
    
    
    def __init__(self, class_obj):
        self.orders = class_obj.orders
        self.employees = class_obj.employees
        
        self.detailed_idx = class_obj.detailed_idx
        self.detailed_arr = class_obj.detailed_arr
        
        self.class_obj = class_obj
    
    def initiate_setup(self):
        """
        default setup to use
        """
        self.setup()
        self.get_full_analysis()
        self.combine_tables()
    
    def setup(self, get_table=False):
        """
        more customary setup used when checking the result for debugging.
        
        args:
            get_table (False): prints a table when not False
        """
        var = ['employee_id', 'last_name', 'first_name', 'title', 'hire_date']
        data = list(self.employees.values_list(*var))
        headers = ['employee_id', 'name', 'title', 'hire_date']
        self.employee_dict = {}
        
        for _i_, i in enumerate(data):
            I = list(i)
            I[1], I[4] = f'{I[2]} {I[1]}', str(I[4])
            I.pop(2)
            data[_i_] = I
            self.employee_dict[int(I[0])] = I[1:]
        
        if get_table is not False:
            self.universal_table(data, headers)
    
    def get_full_analysis(self, index_to_sort=1, get_table=False): 
        """
        calculates total orders, quantity, price and items ordered each 
        employees have handled. 
        
        args:
            index_to_sort (int): index, or column to sort
            get_table (False): prints a table when not False
        """
        sales_count = list(self.orders.values_list('employee_id').annotate(
            tot=Count('employee_id')).order_by('-tot'))
        
        for _i_, i in enumerate(sales_count):
            sales_count[_i_] = list(i)

        result = [0] * len(self.order_dict)
        for _i_, i in enumerate(self.order_dict.keys()):
            temp = np.zeros(5)
            temp[:2] = sales_count[_i_]
            
            for j in self.order_dict[i]:
                idx = self.detailed_idx[j]
                detailed_arr = self.detailed_arr[idx] 

                tot_quantity = np.sum(detailed_arr[:, 2])
                cost = np.prod(detailed_arr[:, 1:4], axis=1)
                
                temp[2:] += len(idx), int(tot_quantity), sum(cost)
            
            result[_i_] = np.round(temp, 3)
        
        self.result = result
        headers = ['employee_id', 'orders', 'items_ordered', 'quantity', 
                   'tot_price']
                    
        if get_table is not False:
            sorted_result = self.sort_list(result, index_to_sort)
            self.universal_table(sorted_result, headers)

    def combine_tables(self):
        """
        combines the product statistics and employee table into one.
        """
        result = [0] * len(self.employee_dict)
        
        for _i_, i in enumerate(self.result):
            self.employee_dict[int(i[0])] += list(i[1:])
            result[_i_] = [int(i[0])] + self.employee_dict[int(i[0])]

        self.result = result    
    
    def make_table(self, idx=4, get_table=False, write_to_file=False, 
                   default_header=True, filename='employee_analytic.txt'):
        """
        sorts the result, and stores the result as sql file, txt file and 
        possible to print out the table.
        
        args:
            idx (int): index to sort
            get_table (Bool): prints a table when not False
            write_to_file (Bool): save the result as txt file when not False
            default_header (Bool): use default header, or customary one when
                                   a list is given
            filename (str): name of the txt file
        
        return:
            sorted_result (list): nested list
        """
        idx = self.check_index(idx, len(self.result[0]), 'column', 'column')
        
        if default_header:
            headers = ['employee_id', 'name', 'title', 'hire_date', 'orders', 
                       'items_ordered', 'quantity', 'tot_price']
        
        sorted_result = self.sort_list(self.result, idx)
        table = self.universal_table(sorted_result, headers, True)
        Create_SQL('ansatte', sorted_result, headers)
        
        if get_table is True:
            print(table)
            
        if write_to_file is True:
            file = open('txt_files/' + filename, 'w')
            file.write(table)
            file.close()
            
        return sorted_result
        
        
        
        
        
        
        
        
        
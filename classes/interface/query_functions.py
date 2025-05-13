from classes.interface.utility import Utility

"""
methods for each query that can be used from the interface when main.py is
executed. each method can fall back to default settings, or more customary
ones can be given.
"""

class Query_functions(Utility):
    def storage_query(self, always_default):
        if always_default is True:
            default = True
        else:
            self.use_default_message()
            default = self.request_yes_no(input())
        
        if default is True:
            get_table = False
            product_id = None
        else:
            message = str('\nget entry for a single product.'
                          '\nenter product_id (number):\n>')
            product_id = self.request_number(message)         
            
            self.table_message()
            get_table = self.request_yes_no(input())
    
        return True, (get_table, product_id)
    
    def sale_query_table(self, always_default):
        if always_default is True:
            default = True
        else:
            self.use_default_message()
            default = self.request_yes_no(input())
        
        if default is True:
            get_table = False
            write_to_file = False
        else:
            self.txt_file_message()
            write_to_file = self.request_yes_no(input())
            
            self.table_message()
            get_table = self.request_yes_no(input())
        
        return True, (get_table, write_to_file)
    
    def sale_query_monthly(self, always_default):
        if always_default is True:
            default = True
        else:
            self.use_default_message()
            default = self.request_yes_no(input())
        
        if default is True:
            include_price = False
            separate_years = False
            get_table = False
            make_plot = True
        else:
            print('\ninclude price.\nType "yes" or "no":\n>', end=' ')
            include_price = self.request_yes_no(input())
            
            print('\nseparate the years.\nType "yes" or "no":\n>', end=' ')
            separate_years = self.request_yes_no(input())
            
            self.graph_message()
            make_plot = self.request_yes_no(input())
            
            self.table_message()
            get_table = self.request_yes_no(input())
            
        return True, (include_price, separate_years, get_table, make_plot)
    
    def sale_query_average(self, always_default):
        if always_default is True:
            default = True
        else:
            self.use_default_message()
            default = self.request_yes_no(input())
        
        if default is True:
            get_table = False
        else:
            self.table_message()
            get_table = self.request_yes_no(input())
            
        return True, (get_table)
    
    def sale_query_demand(self, always_default):
        if always_default is True:
            default = True
        else:
            self.use_default_message()
            default = self.request_yes_no(input())
        
        if default is True:
            get_table = False
            interval_size = 3
        else:
            message = str('\nselect interval size in months:\n>')
            interval_size = self.request_number(message, 3)
            
            self.table_message()
            get_table = self.request_yes_no(input())
            
        return True, (interval_size, get_table)
    
    def sale_query_trend(self, always_default):
        if always_default is True:
            default = True
        else:
            self.use_default_message()
            default = self.request_yes_no(input())
        
        if default is True:
            get_table = False
            quarterly = False
        else:
            print('\nget seasonal trend.\nType "yes" or "no":\n>', end=' ')
            quarterly = self.request_yes_no(input())
            
            self.table_message()
            get_table = self.request_yes_no(input())
            
        return True, (get_table, quarterly)
    
    def sale_query_comparison(self, always_default):
        if always_default is True:
            default = True
        else:
            self.use_default_message()
            default = self.request_yes_no(input())
        
        if default is True:
            get_table = False
            make_plot = True
            idx = 2
        else:        
            self.graph_message()
            make_plot = self.request_yes_no(input())
            
            self.table_message()
            get_table = self.request_yes_no(input())
            
            message = self.column_message()
            idx = self.request_number(message, 2)
            
        return True, (get_table, make_plot, idx)
    
    def employees_query(self, always_default):
        if always_default is True:
            default = True
        else:
            self.use_default_message()
            default = self.request_yes_no(input())
        
        if default is True:        
            idx = 4
            write_to_file = False
            get_table = False
        else:
            message = self.column_message()
            idx = self.request_number(message, 4)

            self.txt_file_message()
            write_to_file = self.request_yes_no(input())

            self.table_message()
            get_table = self.request_yes_no(input())
        
        variables = (idx, get_table, write_to_file)                      
        return True, variables
    
    def product_query_storage(self, always_default):
        if always_default is True:
            default = True
        else:
            self.use_default_message()
            default = self.request_yes_no(input())
        
        if default is True:
            get_table = False
            product_id = None
        else:
            message = str('\nget entry for a single product:'
                          '\nenter product_id (number):\n>')
            product_id = self.request_number(message)       
            
            self.table_message()
            get_table = self.request_yes_no(input())
    
        return True, (get_table, product_id)
    
    def product_query_sold(self, always_default):
        if always_default is True:
            default = True
        else:
            self.use_default_message()
            default = self.request_yes_no(input())
        
        if default is True:
            get_table = False
        else:
            self.table_message()
            get_table = self.request_yes_no(input())
        
        return True, (get_table)
    
    def product_query_sales(self, always_default):
        if always_default is True:
            default = True
        else:
            self.use_default_message()
            default = self.request_yes_no(input())
    
        if default is True:
            get_table = False
        else:
            self.table_message()
            get_table = self.request_yes_no(input())
        
        return True, (get_table)
    
    def delivery_query(self, always_default):
        if always_default is True:
            default = True
        else:
            self.use_default_message()
            default = self.request_yes_no(input())
        
        if default is True:        
            filtered = False
            idx = 1
            get_table = False
        else:
            message = '\nfilter out negative times.\nType "yes" or "no":\n>'
            print(message, end=' ')
            filtered = self.request_yes_no(input())
            
            self.table_message()
            get_table = self.request_yes_no(input())
            
            message = self.column_message()
            idx = self.request_number(message, 1)
            
        return True, filtered, (idx, get_table)
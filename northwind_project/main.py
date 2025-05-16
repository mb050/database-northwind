from os.path import exists
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'northwind_project.settings')
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"

def startup():
    import django
    django.setup()

try:
    from application.models import Region
except:
    startup()

from classes.interface.query_functions import Query_functions
from classes.interface.query_functions import Utility

from classes.employee_analytic import Employee_analytic
from classes.product_query import Product_query
from classes.delivery_time import Delivery
from classes.storage_query import Storage
from classes.sales import Sales
from classes.base import Base


class Main(Query_functions, Utility):
    """
    main function which allows the user to choose which queries to use.
    
    methods:
        check_folder: check if certain folder exists.
        setup_class_objects: initiates the querysets.
        menu: method for the main menu in the interface.
        category_storage:method for the main menu in the interface.
        category_sale:method for the sale queries in the interface.
        category_employee: method for the employee queries in the interface.  
        category_product: method for the product queries in the interface.
        category_delivery: method for the delivery queries in the interface.
    """
    def __init__(self):
        self.check_folder()
        super().__init__()
        self.setup_class_objects()
        self.always_default = False
        self.menu()
    
    def check_folder(self):
        """
        check and creates necessary folders if they don't exist.
        """
        if exists('sql_files') is not True:
            os.mkdir('sql_files')
        
        if exists('txt_files') is not True:
            os.mkdir('txt_files')
    
    def setup_class_objects(self):
        """
        prepares and initiates the querysets for later use.
        """
        base_obj = Base()
        base_obj.initiate_default()
        
        self.storage_obj = Storage(base_obj)
        
        self.sale_obj = Sales(base_obj)
        self.sale_obj.get_order()
        
        self.employee_obj = Employee_analytic(base_obj)
        self.employee_obj.get_order('employee_id')
        self.employee_obj.initiate_setup()
        
        self.product_obj = Product_query(base_obj)
        
        self.delivery_obj = Delivery(base_obj)
    
    def menu(self):
        """
        method for the main menu in the interface.
        """
        text, help_str = self.support_text('main menu')
        title, invalid, enter_message = text[:3]
        command_str, overview, option = text[3:]
        
        skip = False
        was_invalid = False
        loop_enabled = True
        while loop_enabled:
            if was_invalid is not True:
                print(enter_message, end=' ')
            else:
                was_invalid = False
            
            input_str = input().lower()
            if input_str in ['storage', 'stor']:
                skip = self.category_storage()
            elif input_str == 'sale':
                skip = self.category_sale()
            elif input_str in ['employee', 'empl']:
                skip = self.category_employee()
            elif input_str in ['product', 'prod']:
                skip = self.category_product()
            elif input_str in ['delivery', 'deli']:
                skip = self.category_delivery()
            
            if skip is True:
                self.make_title('main menu')
                print(overview)
                skip = False
                continue
            
            cases = self.check_command(input_str, help_str, option, 
                                       self.always_default)
            if cases is None:
                continue
            elif cases == 'break':
                break
            elif cases[0] == 'default':
                self.always_default = cases[1]
                print(overview)
            else:
                print(invalid, end=' ')
                was_invalid = True

    def category_storage(self):
        """
        method for the storage queries in the interface.
        
        return:
            True.
        """
        text, help_str = self.support_text('storage')
        title, invalid, enter_message = text[:3]
        command_str, overview, option = text[3:]
        always_default = self.always_default
        
        skip = False
        was_invalid = False
        loop_enabled = True
        while loop_enabled:
            if was_invalid is not True:
                print(enter_message, end=' ')
            else:
                was_invalid = False
            
            input_str = input().lower()
            if input_str in ['product', 'prod']:
                skip, variables = self.storage_query(always_default)
                self.storage_obj.product_storage(*variables)
            
            if skip is True:
                print('\n> Query complete\n', overview)
                skip = False
                continue
            
            cases = self.check_command(input_str, help_str, option, 
                                       always_default, True)
            if cases is None:
                continue
            elif cases == 'break':
                print('\t returning to main menu')
                break
            elif cases[0] == 'default':
                always_default = cases[1]
                print(overview)
            else:
                print(invalid, end=' ')
                was_invalid = True
                
        return True
    
    def category_sale(self):
        """
        method for the sale queries in the interface.
        
        return:
            True.
        """
        text, help_str = self.support_text('sale')
        title, invalid, enter_message = text[:3]
        command_str, overview, option = text[3:]
        always_default = self.always_default
        
        skip = False
        was_invalid = False
        loop_enabled = True
        while loop_enabled:
            if was_invalid is not True:
                print(enter_message, end=' ')
            else:
                was_invalid = False
            
            input_str = input().lower()
            if input_str == 'sale':
                skip, variables = self.sale_query_table(always_default)
                self.sale_obj.sale_table(*variables)
            elif input_str in ['monthly_sale', 'month', 'mont']:
                skip, variables = self.sale_query_monthly(always_default)
                self.sale_obj.monthly_sales(*variables)
            elif input_str in ['average', 'aver']:
                skip, variables = self.sale_query_average(always_default)
                self.sale_obj.average_value(variables)
            elif input_str in ['demand', 'dema']:
                skip, variables = self.sale_query_demand(always_default)
                self.sale_obj.product_request(*variables)
            elif input_str in ['trends', 'tren']:
                skip, variables = self.sale_query_trend(always_default)
                self.sale_obj.seasonal_trend(*variables)
            elif input_str in ['compare', 'comp']:
                skip, variables = self.sale_query_comparison(always_default)
                self.sale_obj.comparison(*variables)
            
            if skip is True:
                print('\n> Query complete\n', overview)
                skip = False
                continue
            
            cases = self.check_command(input_str, help_str, option, 
                                       always_default, True)
            if cases is None:
                continue
            elif cases == 'break':
                print('\t returning to main menu')
                break
            elif cases[0] == 'default':
                always_default = cases[1]
                print(overview)
            else:
                print(invalid, end=' ')
                was_invalid = True
                
        return True
    
    def category_employee(self):
        """
        method for the employees queries in the interface.
        
        return:
            True.
        """
        text, help_str = self.support_text('employee')
        title, invalid, enter_message = text[:3]
        command_str, overview, option = text[3:]
        always_default = self.always_default
        
        skip = False
        was_invalid = False
        loop_enabled = True
        while loop_enabled:
            if was_invalid is not True:
                print(enter_message, end=' ')
            else:
                was_invalid = False
            
            input_str = input().lower()
            if input_str in ['employees', 'empl']:
                skip, variables = self.employees_query(always_default)
                self.employee_obj.make_table(*variables)
                
            if skip is True:
                print('\n> Query complete\n', overview)
                skip = False
                continue
            
            cases = self.check_command(input_str, help_str, option, 
                                       always_default, True)
            if cases is None:
                continue
            elif cases == 'break':
                print('\t returning to main menu')
                break
            elif cases[0] == 'default':
                always_default = cases[1]
                print(overview)
            else:
                print(invalid, end=' ')
                was_invalid = True
                
        return True
    
    def category_product(self):
        """
        method for the product queries in the interface.
        
        return:
            True.
        """
        text, help_str = self.support_text('product')
        title, invalid, enter_message = text[:3]
        command_str, overview, option = text[3:]
        always_default = self.always_default
        
        skip = False
        was_invalid = False
        loop_enabled = True
        while loop_enabled:
            if was_invalid is not True:
                print(enter_message, end=' ')
            else:
                was_invalid = False
    
            input_str = input().lower()
            if input_str in ['products', 'prod']:
                skip, variables = self.product_query_storage(always_default)
                self.product_obj.product_storage(*variables)
            elif input_str in ['inventory', 'inve']:
                skip, variables = self.product_query_sold(always_default)
                self.product_obj.product_sold(variables)
            elif input_str in ['categories', 'cate']:
                skip, variables = self.product_query_sales(always_default)
                self.product_obj.category_sales(variables, 'category_id')
            elif input_str in ['suppliers', 'supp']:
                skip, variables = self.product_query_sales(always_default)
                self.product_obj.category_sales(variables, 'supplier_id')
            
            if skip is True:
                print('\n> Query complete\n', overview)
                skip = False
                continue
            
            cases = self.check_command(input_str, help_str, option, 
                                       always_default, True)
            if cases is None:
                continue
            elif cases == 'break':
                print('\t returning to main menu')
                break
            elif cases[0] == 'default':
                always_default = cases[1]
                print(overview)
            else:
                print(invalid, end=' ')
                was_invalid = True
                
        return True
    
    def category_delivery(self):
        """
        method for the delivery queries in the interface.
        
        return:
            True.
        """
        text, help_str = self.support_text('delivery')
        title, invalid, enter_message = text[:3]
        command_str, overview, option = text[3:]
        always_default = self.always_default
        
        skip = False
        was_invalid = False
        loop_enabled = True
        while loop_enabled:
            if was_invalid is not True:
                print(enter_message, end=' ')
            else:
                was_invalid = False
            
            input_str = input().lower()
            if input_str in ['delivery_time', 'deli']:
                skip, filtered, variables = self.delivery_query(always_default)
                self.delivery_obj.get_delivery_time(filtered)
                self.delivery_obj.make_table(*variables)
                
            if skip is True:
                print('\n> Query complete\n', overview)
                skip = False
                continue
            
            cases = self.check_command(input_str, help_str, option, 
                                       always_default, True)
            if cases is None:
                continue
            elif cases == 'break':
                print('\t returning to main menu')
                break
            elif cases[0] == 'default':
                always_default = cases[1]
                print(overview)
            else:
                print(invalid, end=' ')
                was_invalid = True
                
        return True

if __name__ == '__main__':
    Main()
    pass

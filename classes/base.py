import itertools as itr
import numpy as np
from django.db.models import Count
from tabulate import tabulate
from datetime import datetime
from application.models import (Categories, CustomerCustomerDemo, 
                                CustomerDemographics, Customers,
                                EmployeeTerritories, Employees, 
                                OrderDetails, Orders, Products, 
                                Region, Shippers, Suppliers, 
                                Territories, UsStates)

class Base():
    """
    contains common functions used by other classes, and also contains all the
    django queryset.
    
    methods:
        initiate_less_used: loads in less commonly used querysets.
        initiate_customer_specific: loads in customer demo and demographics.
        initiate_default: default initiation.
        setup_interval_sales: creates date related variables and methods.
        setup_months: creates a list with months.
        sort_dates: sorts dates into months.
        sort_list: sorts nested lists.
        universal_table: create table.
        get_customer_list: creates a list containing customer_id.
        check_index: check if a given index is within range.
        get_order: count amount of orders given a variable.
        get_customer_orders: creates a dict containing customer_id or 
            employee_id and amount of orders.
        get_detailed_orders: create array and dict containing orderdetails.
        get_order_and_date: creates list sorted based on order and date.
        get_interval_idx: creates array used for making custom intervals.
        retrieve_sales: organize orders into an easier format for further use.
        inner_loop: inner loop to retrieve_sales method.
        get_months: get months based on a given interval size.
        merge_months: merge array into given interval size.
        merge_years: merge array into a single year, while containing 
                     the intervals.
        merge_universal: method combining both merge_months and merge_years.
    """
    def __init__(self):
        """
        stores the most commonly used querysets as instances.
        """
        self.categories = Categories.objects.all()
        self.customers = Customers.objects.all()
        self.employees = Employees.objects.all()
        self.orderdetails = OrderDetails.objects.all() 
        self.orders = Orders.objects.all()
        self.products = Products.objects.all()
        self.shippers = Shippers.objects.all()
        self.suppliers = Suppliers.objects.all()
        
        self.n_products = len(self.products)
        self.variable = 'order_id'
        return
    
    def initiate_less_used(self):
        """
        stores less commonly used querysets as instances.
        """
        self.employeeterritories = EmployeeTerritories.objects.all()
        self.region = Region.objects.all()
        self.territories = Territories.objects.all()
        self.usstates = UsStates.objects.all()
    
    def initiate_customer_specific(self):
        """
        stores the least used or unused querysets as instances.
        """
        self.customercustomerdemo = CustomerCustomerDemo.objects.all()
        self.customerdemographics = CustomerDemographics.objects.all()
    
    def initiate_default(self):
        """
        initiation of crucial methods.
        """
        self.get_detailed_orders()
        self.setup_interval_sales()
        
        self.setup_interval_sales()
        self.setup_months()
        return
    
    def setup_interval_sales(self):
        """
        initiation of crucial methods and creation of instances related to
        dates.
        """
        self.get_order_and_date()
        
        self.key_list = list(self.date_to_order.keys())
        
        self.year_0 = min(self.key_list).year
        self.year_1 = max(self.key_list).year
        self.n_years = (self.year_1 - self.year_0) + 1
        
        self.sort_dates()
        self.get_interval_idx()
        self.retrieve_sales()
        
    def setup_months(self):
        """
        create a list with months.
        """
        self.months = [''] * 12
        for i in range(12):
            self.months[i] = datetime(2000, 1 + i, 1).strftime('%B')
    
    def sort_dates(self):
        """
        separates the dates into months as nested lists.
        """
        self.date_list = []
        
        for i in range(12):
            self.date_list.append([])

        for i in self.key_list:
            self.date_list[i.month - 1].append(i)
    
    def sort_list(self, value_list, idx, reverse=True):
        """
        sort nested list.
        
        args:
            value_list (list): nested list.
            idx (int): index.
            reverse (bool): True.
        
        return:
            sorted_list (list): sorted list given index.
        """
        index_to_sort = lambda x: x[idx]
        sorted_list = sorted(value_list, key=index_to_sort)
        
        if reverse is True:
            return list(reversed(sorted_list))
        else:
            return sorted_list
    
    def universal_table(self, content_list, headers, return_table=False,
                        tablefmt='presto'):
        """
        creates a table.
        
        args:
            content_list (list): nested_list.
            headers (list): list containing str.
            return_table (bool): False.
        
        return:
            table (table): if return_table is not False.
        """
        table = tabulate(content_list, headers=headers, tablefmt=tablefmt)
        if return_table is False:
            print(f'\n{table}')
        else:
            return table
    
    def get_customer_list(self):
        """
        create a list with customer_id's
        """
        self.customer = list(sum(list(self.orders.values_list(
            'customer_id').annotate(tot=Count('customer_id')).order_by(
                '-tot')), ())[::2])
        return
    
    def check_index(self, idx, n_elements, message1='', message2='', 
                    start_at_0=True):
        """
        corrects if an index is out of range.
        
        args:
            idx (int): index to check.
            n_elements (int): amount of elements.
            message1 (str): custom text.
            message2 (str): custom text.
            start_at_0 (bool): True.
        
        return:
            idx (int): corrected index.
        """
        text = '\ngiven {} is out of range, defaulting to the {} {}'
        idx -= (start_at_0 is not True)
        n = n_elements - 1
        
        if idx < 0:
            idx = 0
            print(text.format(message1, 'first', message2))
        elif idx > n:
            idx = n
            print(text.format(message1, 'last', message2))
            
        return idx
    
    def get_order(self, variable='customer_id'):
        """
        creates a dict containing customer_id or employee_id with correlating
        orders.
        
        args:
            variable (str): variable to use, will in most cases be either 
                            customer_id or employee_id.
        
        return:
            dict.
        """
        self.count = self.orders.values_list(variable).annotate(
            tot=Count(variable)).order_by('-tot')
        return self.get_customer_orders(variable)
    
    def get_customer_orders(self, variable_filter='customer_id'):
        """
        continuation of get_order, that takes self.count and creates the 
        dictionary itself.
        
        args:
            variable_filter (str): variable to use, will in most cases be 
                                   either customer_id or employee_id.
        
        return:
            self.order_dict (dict): dict containing amount of orders.
        """
        variable = 'order_id'
        self.order_dict = {}        
        for (i, _i_) in self.count:
            if variable_filter == 'customer_id':
                order = list(self.orders.filter(customer_id=i
                                    ).values_list(variable))
            
            elif variable_filter == 'employee_id':
                order = list(self.orders.filter(employee_id=i
                                    ).values_list(variable))
            
            self.order_dict[i] = np.array(sum(order, ()))
        return self.order_dict
    
    def get_detailed_orders(self):
        """
        creates array containing orderdetails and corresponding entries given
        a specific order_id.
        """
        variable = 'order_id'
        individual_order = self.orderdetails.values_list(variable
            ).annotate(tot=Count(variable)).order_by(variable)
        
        n = max(individual_order)[1]
        idx_arr = np.arange(n)
        self.detailed_idx = {}

        for i in individual_order:
            I, J = i     
            self.detailed_idx[I] = idx_arr.copy()[:J]
            idx_arr += J
    
        detailed = np.array(self.orderdetails.values_list())
        detailed[:, -1] = 1 - detailed[:, -1]
        self.detailed_arr = detailed[:, 1:]

        del(detailed)
        del(individual_order)
        return
    
    def get_order_and_date(self):
        """
        creates two dictionaries, one with date as key, and one with the 
        order_id as key.
        """
        var = ['order_id', 'order_date']
        order_date = list(Orders.objects.all().values_list(*var))
        
        for _i_, i in enumerate(order_date):
            order_date[_i_] = list(i)
    
        self.order_to_date = {}
        self.date_to_order = {}
        date = 0
        for i, j in order_date: 
            self.order_to_date[i] = j
            if date == str(j):
                self.date_to_order[j].append(i)
            else:
                self.date_to_order[j] = [i]
                date = str(j)

    def get_interval_idx(self):
        """
        creates an array with indexes for the different years. first two in 
        axis=1 is the index placement of orders for given years in 
        the date_list. it is used for splicing.
        """
        self.interval_idx = np.zeros((12, 4), dtype=int)
        range_year = range(self.year_0, self.year_1 + 1)
        
        for i, months in enumerate(self.date_list):
            temp = []
            for j in months:
                temp.append(j.year)
            
            n = len(temp)
            self.interval_idx[i, 3] = n
            for k, check in enumerate(range_year):
                try:
                    idx = temp.index(check)
                except:
                    if check == self.year_0:
                        idx = 0
                    elif check == self.year_1:
                        idx = n
                
                self.interval_idx[i, k] = idx
    
    def retrieve_sales(self):
        """
        separates ordered product into months, year and total amount sold,
        including the price. 
        """
        self.month_data = []
        self.month_price = np.zeros((3, 12))
        
        Idx = self.interval_idx
        array_shape = (self.n_years, self.n_products)
        pre_calculated = np.prod(self.detailed_arr[:, 1:], axis=1)
        
        for i in range(12):
            self.month_data.append(np.zeros(array_shape, dtype=int))

        for (i, j) in itr.product(range(12), range(3)):
            date_list = self.date_list[i][Idx[i, j]:Idx[i, j + 1]]
            self.inner_loop(date_list, pre_calculated, i, j)
        return 
    
    def inner_loop(self, date_list, price_val, i, j):
        """
        the inner loop from retrieve_sales method.
        
        args:
            date_list (list): nested list of size 12 containing 
                              orders for a given month.
            price_val (np.array): array containing the prices.
            i (int): iteration.
            j (int): iteration.
        """
        for date_key in date_list:
            for order_id in self.date_to_order[date_key]:
                idx = self.detailed_idx[order_id]
                val = np.array(self.detailed_arr[idx], dtype=int)
                self.month_data[i][j, val[:, 0] - 1] += val[:, 2]   
                self.month_price[j][i] += sum(price_val[idx])
         
    def get_months(self, interval_size):
        """
        creates a list containing the intervals and months it start and stops
        at.
        
        args:
            interval_size (int): interval size in months.
            
        return:
            months (list): list of str.
        """
        n = int(12 / interval_size)
        months = self.months.copy()
        
        if not n == 1:
            for i in range(interval_size):
                months[i] = f'{months[i * n]}-{months[(i + 1) * n - 1]}'
        
        del(months[interval_size:])
        return months
    
    def merge_months(self, arr=None, interval_size=3):
        """
        merges the 12 months into defined interval size.
        
        args:
            arr (bool, or np.array): array containing the data, defaults to 
                                     self.month_data if none are provieded
            interval_size (int): interval size.
        
        return:
            merged (list): merged list.
        """
        if arr is None:
            arr = self.month_data
        
        merged = []
        size = int(12 / interval_size)
        idx_arr = np.arange(12).reshape((size, interval_size))
        
        if np.shape(arr) == (3, 12):
            merged = np.zeros((3, size))
            
            for i, idx in enumerate(idx_arr):
                merged[:, i] = np.sum(arr[:, idx], axis=1)
        else:
            for i, idx in enumerate(idx_arr):
                merged.append(sum(arr[idx[0]:idx[-1] + 1]))
                
        return merged

    def merge_years(self, arr=None):
        """
        merges the different years into a single year.
        
        args:
            arr (bool, or np.array): array containing the data, defaults to 
                                     self.month_data if none are provieded.
        return:
            merged (list or np.array): array/list used.
        """
        if arr is None:
            arr = self.month_data
        
        if type(arr) == list:
            for i, j in enumerate(arr):
                arr[i] = np.sum(arr[i], axis=0)
        else:
            arr = np.sum(arr, axis=0)
            
        return arr
    
    def merge_universal(self, arr=None, interval_size=3):
        """
        combines merge_years and combine_months.
        
        args:
            arr (bool, or np.array): array containing the data, defaults to 
                                     self.month_data if none are provieded.
            interval_size (int): interval size.
        
        return:
            merged (list): merged list.
        """
        if arr is None:
            arr = self.month_data

        arr = self.merge_months(arr, interval_size)
        return self.merge_years(arr)








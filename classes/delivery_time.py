from classes.create_sql import Create_SQL
from classes.base import Base

class Delivery(Base):
    """
    create table with the average delivery time from an order is shipped to
    received.
    
    attributes:
        class_obj: class object from Base for more specific functions or
                   instances.
    methods:
        setup: set up necessary instances
        create_lists: creates lists used in the class, and removes already
                      existing ones.
        calculate_delivery_time: calculates average delivery time
        merge: combines lists into a single nested list
        get_delivery_time: initiates to calculate average delivery time
        custom_sort: sort nested list containing nan/None
        make_table: creates table and write result into sql file
        sum_elements: goes through dictionary and calculates the average
    """
    def __init__(self, class_obj):
        self.shippers = class_obj.shippers
        self.orders = class_obj.orders
        self.class_obj = class_obj
        
        self.setup()

    def setup(self):
        """
        creates necessary instances
        """
        var = ['order_date', 'required_date', 'shipped_date', 'ship_via']
        shippers = self.shippers.values_list('shipper_id', 'company_name')
        self._order_ = list(self.orders.values_list(*var))
        self.shipper_dict = {}
        
        for i in shippers:
            self.shipper_dict[i[0]] = i[1]
        
        self.dict_key = self.shipper_dict.keys()
        self.n_shippers = len(shippers)
    
    def create_lists(self):
        """
        creates lists used in the class, and removes already existing ones.
        can cause errors if not used.
        """
        try:
            del(self.no_shipped_date)
            del(self.ordinary)
        except:
            pass

        self.ordinary = {}
        self.no_shipped_date = {}
        
        for i in range(1, self.n_shippers + 1):
            self.no_shipped_date[i] = []
            self.ordinary[i] = []
    
    def calculate_delivery_time(self, filtered=False):
        """
        calculate the average delivery time and stores it into ordinary
        or the no_shipped_date, based on wether the shipped date is missing
        or not.

        args:
            filtered (Bool): will not filter out dates that becomes negative
                             due to errors in the original entry, and instead
                             uses the absolute value.
        """
        normal = True
        for j, i in enumerate(self._order_):
            try:
                difference = (i[1] - i[2]).days
            except:
                difference = (i[1] - i[0]).days
                normal = False
            
            if filtered is False and difference < 0:
                difference = abs(difference)
            elif filtered is True and difference < 0:
                continue
            
            if normal is True:
                self.ordinary[i[3]].append(difference)
            else:
                self.no_shipped_date[i[3]].append(difference)
                normal = True
    
    def merge(self):
        """
        goes through the dictionaries to turn it into lists, and combines them
        into a single nested list in the proper format.
        """
        ordinary = self.sum_elements(self.ordinary)
        no_shipped_date = self.sum_elements(self.no_shipped_date)
        shipper_dict = self.shipper_dict
        
        self.result = [0] * self.n_shippers
        for j, i in enumerate(self.dict_key):
            self.result[j] = [shipper_dict[i], ordinary[i], no_shipped_date[i]]
            
    def get_delivery_time(self, filtered=False):
        """
        initiates necessary method to calculate the average delivery time.
        
        args:
            filtered (Bool): will not filter out dates that becomes negative
                             due to errors in the original entry, and instead
                             uses the absolute value.
        """
        self.create_lists()
        self.calculate_delivery_time(filtered)
        self.merge()
    
    def custom_sort(self, value_list, idx=1):
        """
        sort nested list containing np.NaN/None
        
        args:
            value_list (list): nested list
            idx (int): index to sort
        
        return:
            nested list with the sorted entries.
        """
        contain_no_none = []
        contain_none = []

        for i in value_list:
            found_none = False
            
            for j in i[1:]:
                if j == None:
                    contain_none.append(i)
                    found_none = True
                    break
            
            if found_none is False:
                contain_no_none.append(i)
        
        contain_no_none = self.sort_list(contain_no_none, idx, False)
        return contain_no_none + contain_none
    
    def make_table(self, idx=1, get_table=False):
        """
        sorts the result, and stores the result as sql file.
        
        args:
            idx (int): index to sort
            get_table (Bool): prints a table when not False
        """
        idx = self.check_index(idx, len(self.result[0]), 'column', 'column')
        result = self.custom_sort(self.result, idx)
        headers = ['company_name', 'average_delivery_time', 
                   'average_order_to_required_time']
        
        if get_table is not False:
            self.universal_table(result, headers)
        
        Create_SQL('leveringstid', result, headers)
        
    def sum_elements(self, dictionary):
        """
        calculate the average time.
        
        args:
            dictionary (dict): company name as keys, and list with time as
                               values
        return:
            dictionary with the average values.
        """
        key = list(dictionary.keys())
        
        for j, i in enumerate(dictionary.values()):
            if len(i) <= 0:
                dictionary[key[j]] = None
                continue
            
            dictionary[key[j]] = round(sum(i) / len(i), 1)
        return dictionary

 
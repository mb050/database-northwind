from classes.create_sql import Create_SQL
from django.db.models import Count
from classes.base import Base
import numpy as np

class Product_query(Base):
    """
    class containing related methods to product queries.
    
    attributes:
        class_obj: class object from Base for more specific functions or
                   instances.
    
    methods:
        get_product_order: creates a dict with product_id.
        product_storage: get status of products in storage.
        output_single_product: print the status of a single product.
        product_sold: creates a table based on amount of products sold.
        category_sale: creates a table related to amount of products sold
                       for either category or the supplier.
    """
    def __init__(self, class_obj):
        self.orders = class_obj.orders
        self.products = class_obj.products
        self.orderdetails = class_obj.orderdetails
        
        self.detailed_idx = class_obj.detailed_idx
        self.detailed_arr = class_obj.detailed_arr
        
        self.class_obj = class_obj
        
        self.get_product_order()
        return
 
    def get_product_order(self):
        """
        makes a dict with product_id and the values as arrays.
        
        return:
            self.product_order (dict): product_id as key, and array as values.
        """
        product_id = list(sum(self.products.values_list('product_id'), ()))
        self.product_order = {}
        for i in product_id:
            self.product_order[i] = []
        
        detailed = list(self.orderdetails.values_list())
        for _i_, i in enumerate(detailed):
            i = list(i)
            i[0], i[1] = i[1], i[0]
            self.product_order[i[0]].append(i[1:])
        
        for i in range(1, len(self.product_order) + 1):
            self.product_order[i] = np.array(self.product_order[i])
        return self.product_order
    
    def product_storage(self, get_table=False, product_id=None):
        """
        create a table containing amount of products in stock, and which 
        company supplies a given product. 
        
        args:
            get_table (bool): False, controls if a table is printed out or not.
            product_id (int else bool): product_id to show.
        """
        name = ['product_id', 'product_name', 'unit_price', 'units_in_stock']
        headers = name + ['supplier_company_name']

        product_full = self.products
        products = list(product_full.values_list(*name))
        prod_and_suppliers = product_full.select_related('supplier')

        for i, (j, k) in enumerate(zip(products, prod_and_suppliers)):
            products[i] = list(j) + [k.supplier.company_name]
        
        if product_id is not None:
            self.output_single_product(products, headers, product_id)
        
        if get_table is True:
            self.universal_table(products, headers)

        Create_SQL('varer', products, headers)

    def output_single_product(self, products, headers, product_id):
        """
        prints out a single product and it's status.
        
        args:
            products (list): nested list.
            headers (list): list with header names.
            product_id (int): product_id.
        """
        idx = self.check_index(product_id, len(products), 
                               'product_id', 'prudct', False)        
        self.universal_table([products[idx]], headers)
    
    def product_sold(self, get_table=False):
        """
        makes a list with product_id and amount each product has sold.
        
        args:
            get_table (bool): False, prints out table if not False.
        """
        var = ['product_id', 'units_in_stock']
        product = list(self.products.values_list(*var))
        
        for i, j in enumerate(product):
            product[i] = list(j) + [np.sum(self.product_order[j[0]][:, 2])]

        var += ['units_sold']
        product = self.class_obj.sort_list(product, 2)
        Create_SQL('lagerbeholdning', product, var)
        
        if get_table is True:
            self.universal_table(product, var)
        
    def category_sales(self, get_table=False, variable='category_id'):
        """
        makes a list with product_id and amount each product has sold within
        a given category or supplier.
        
        args:
            get_table (bool): False, prints out table if not False.
            variable (str): category_id or supplier_id.
        """
        if variable == 'supplier_id':
            headers = ['supplier', 'number_of_products', 'units_sold']
            filename = 'leverandor'
        else:
            headers = ['category_id', 'number_of_products', 'units_sold']
            filename = 'kategorier'
        
        product = self.products        
        content = list(product.values_list(variable).annotate(
            tot=Count(variable)).order_by(variable))
        
        container_dict = {}
        for i, j in content:
            container_dict[i] = [i, j, 0]

        for i in product:
            if variable == 'supplier_id':
                cat_id = i.supplier_id
            else:
                cat_id = i.category_id
            
            prod_id = i.product_id
            units_sold = np.sum(self.product_order[prod_id][:, 2])
            container_dict[cat_id][2] += int(units_sold)
        
        container = np.array(list(container_dict.values()))
        container = self.class_obj.sort_list(container, 2)
        
        Create_SQL(filename, container, headers)
        
        if get_table is True:
            self.universal_table(container, headers)
        
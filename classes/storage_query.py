from classes.create_sql import Create_SQL
from classes.base import Base

class Storage(Base):
    """
    retrieve data relevant to the storage/stock of products.
    
    attributes:
        class_obj: class object from Base for more specific functions or
                   instances.
    
    methods:
        product_storage: retrieve and combine tables relevant to the status 
                         of the products.
        output_single_product: get single product.
    """
    def __init__(self, class_obj):
        self.class_obj = class_obj
        self.products = self.class_obj.products
        return
    
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
        idx = self.check_index(product_id, len(products), 'product_id', 
                               'prudct', False)
        
        self.universal_table([products[idx]], headers)


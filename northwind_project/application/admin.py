from django.contrib import admin
from .models import * 

# from .models import Categories, CustomerCustomerDemo, CustomerDemographics
# from .models import Customers, EmployeeTerritories, Employees, OrderDetails
# from .models import Orders, Products, Region, Shippers 
# from .models import Suppliers, Territories, UsStates  

# Register your models here.

admin.site.register(Categories)
admin.site.register(CustomerCustomerDemo)
admin.site.register(CustomerDemographics)
admin.site.register(Customers)
admin.site.register(EmployeeTerritories)
admin.site.register(Employees)
admin.site.register(OrderDetails)
admin.site.register(Orders)
admin.site.register(Products)
admin.site.register(Region)
admin.site.register(Shippers)
admin.site.register(Suppliers)
admin.site.register(Territories)
admin.site.register(UsStates)
from classes.create_sql import Create_SQL
import matplotlib.pyplot as plt
from classes.base import Base
import itertools as itr
import numpy as np



class Sales(Base):
    def __init__(self, class_obj):
        self.products = class_obj.products
        self.orders = class_obj.orders
        
        self.detailed_idx = class_obj.detailed_idx
        self.detailed_arr = class_obj.detailed_arr
        
        self.class_obj = class_obj
        
        self.variable = 'order_id'
        self.variable_list = ['employee_id', 'order_date', 'ship_country']
        
    def test_func(self):
        print(self.result)
    
    def sale_table(self, get_table=False, write_to_file=False):
        val = ['order_id', 'customer_id', 'employee_id', 
               'order_date', 'ship_country']
        
        product = sum(list(self.products.values_list('product_name')), ())
        data = list(self.orders.values_list(*val))

        for _i_, i in enumerate(data):
            data[_i_] = list(i) + [0]

        for _i_, i in enumerate(data):
            idx = self.detailed_idx[i[0]]
            product_id = self.detailed_arr[idx, 0] - 1
            quantity = self.detailed_arr[idx, 2]

            Str = [''] * len(product_id)
            for _j_, j in enumerate(map(int, product_id)):
                Str[_j_] = f'{int(quantity[_j_])} x {product[j]}'
                
            data[_i_][-1] = ', '.join(Str)
            data[_i_][3] = str(data[_i_][3])

        val += ['products']
        Create_SQL('salg', data, val)
        table = self.universal_table(data, val, True)
        
        if get_table is True:
            print(table)
            
        if write_to_file is True:
            file = open('txt_files/sale_table.txt', 'w')
            file.write(table)
            file.close()
    
    def combine_list(self, header_list, value_list, months, y0, 
                     year_split=True):
        years = [f'{y0 + i}' for i in range(self.class_obj.n_years)]
        convert = lambda x: [list(i) for i in x]
        result, headers = [months], ['month']
        
        if year_split is True:
            for i in header_list:
                for j in years:
                    headers.append(f'{i}_{j}')
            
            for i in value_list:
                result += convert(i)
        else:
            headers += header_list
            result += value_list

        result = [list(i) for i in list(zip(*result))]
        return result, headers
    
    def monthly_sales_plot(self, y0, months, data, price=None):
        y_axis_label = ['units', 'price']
        data = data.astype(float)
        data[data==0] = np.nan
        
        if price is None:
            val = [data]
        else:
            price[price==0] = np.nan
            val = [data, price]

        Shape = np.shape(val)

        if Shape[0] == 1:
            fig, ax = plt.subplots(1, 1)
        else:
            fig, ax = plt.subplots(Shape[0], 1, sharex=True)

        if Shape[0] == 1:
            if len(Shape) == 2:
                ax.scatter(months, val[0], marker='.', color='r')
                ax.plot(months, val[0], ls='--', lw=1, color='k', 
                        label='all years')  
            else:
                for i in range(Shape[1]):
                    ax.scatter(months, val[0][i], marker='.', color='r')
                    ax.plot(months, val[0][i], ls='--', lw=1,
                            label=f'year {y0 + i}')
            
            ax.set_ylabel('units sold')
            ax.set_title('units sold each month')
            ax.legend()
        else:
            for i, j in enumerate(('units sold', 'total price')):
                ax[i].set_title(j)
                
                for k in range(Shape[1]):
                    if len(Shape) == 2:
                        ax[i].scatter(months, val[i], marker='.', color='r')
                        ax[i].plot(months, val[i], ls='--', lw=1, color='k', 
                                    label='all years')
                        ax[i].set_ylabel(y_axis_label[i])
                        ax[i].legend()
                        break
                    else:
                        ax[i].scatter(months, val[i][k], marker='.', color='r')
                        ax[i].plot(months, val[i][k], ls='--', lw=1, 
                                      label=f'year {y0 + i}')
                        ax[i].set_ylabel(y_axis_label[i])
                        ax[i].legend()
        
        fig.tight_layout()
        plt.xticks(rotation=27.5)  
        plt.show()
        
    def monthly_sales(self, include_price=False, separate_years=False,
                      get_table=False, make_plot=True):
        month_data = self.class_obj.month_data.copy()
        months = self.class_obj.months.copy()
        date_list = self.class_obj.key_list

        y0 = min(date_list).year
        price = self.class_obj.month_price
        
        if separate_years is False:
            data = np.sum(self.class_obj.merge_years(month_data), axis=1)
            price = sum(price)
        else: 
            data = self.class_obj.merge_months(month_data, 1)
            data = np.rot90(np.sum(data, axis=2), 1)
            data = np.flip(data, axis=0)

        if separate_years is not False and include_price is not False:            
            value, header = [data, price], ['units_sold', 'tot_price']
            
            if make_plot is True:
                self.monthly_sales_plot(y0, months, data, price)
        
        elif separate_years is not False and include_price is False:
            value, header = [data], ['units_sold']
            
            if make_plot is True:
                self.monthly_sales_plot(y0, months, data)
            
        elif separate_years is False and include_price is not False:
            value, header = [data, price], ['units_sold', 'tot_price']
            
            if make_plot is True:
                self.monthly_sales_plot(y0, months, data, price)
            
        elif separate_years is False and include_price is False:
            value, header = [data], ['units_sold']
            
            if make_plot is True:
                self.monthly_sales_plot(y0, months, data)
            
        combined = self.combine_list(header, value, months, y0, separate_years)
        result, headers = combined[0], combined[1]
        Create_SQL('maned_salg', result, headers)
        
        if get_table is True:  
            self.universal_table(result, headers)
        
    def average_value(self, get_table=False):
        key_list = self.order_dict.keys()
        detailed_arr = self.detailed_arr[:, 1:]
        
        result = [0] * len(key_list)        
        for _i_, i in enumerate(key_list):
            order_id_list = self.order_dict[i]
            temp = [0] * len(order_id_list)
            
            for _j_, j in enumerate(order_id_list):
                idx = self.detailed_idx[j]
                value = np.prod(detailed_arr[idx], axis=1)
                temp[_j_] = np.sum(value) / len(value)
            
            average = sum(temp) / len(temp)
            result[_i_] = [i, round(average, 3)]
        
        sorted_result = self.sort_list(result, 1)
        headers = ['customer_id', 'average_value']
        Create_SQL('gj_ordreverdi', sorted_result, headers)
        
        if get_table is True:            
            self.universal_table(sorted_result, headers)
            
        return sorted_result
    
    def product_request_header(self, start_year, interval_size=3):
        n_years = self.class_obj.n_years
        n = int(12 / interval_size)
        
        months = self.class_obj.months.copy()
        year_list = [str(i) for i in range(start_year, start_year + n_years)]
        header = ['product_id']
        month_number = []
        
        for i in range(12):
            s = str(i + 1)
            if len(s) < 2:
                s = '0' + s
            
            month_number.append(s)

        for i in year_list:
            for j in range(n):
                t0 = month_number[j * interval_size]
                t1 = month_number[(j + 1) * interval_size - 1]
                header.append(f'{months[int(t0)-1]}_{i[2:]}_to_'
                              f'{months[int(t1) - 1]}_{i[2:]}')
        return header
    
    def replace_nan(self, value_list):        
        n, m = np.shape(value_list)
        for i, j in itr.product(range(n), range(m)):
            if np.isnan(value_list[i][j]):
                value_list[i][j] = None
        return value_list
    
    def product_request(self, interval_size=3, get_table=False):
        if not(interval_size in [1, 2, 3, 4, 6, 12]):
            print('\ninvalid interval size given, defaulting '
                  'to interval_size = 3.')
            interval_size = 3
        
        month_data = np.array(self.class_obj.month_data.copy())
        date_list = self.class_obj.key_list
        n_years = self.class_obj.n_years
        
        n = int(12 / interval_size)
        size = n_years * n
        Shape = np.shape(month_data)
        
        data = np.zeros((Shape[-1], Shape[1] * 12))
        arr = np.zeros((n_years, 12)) + 1
        
        start_date = min(date_list)
        end_date = max(date_list)
        
        arr[0, :start_date.month - 1] -= 1
        arr[-1, end_date.month:] -= 1

        arr = np.sum(arr.reshape((size, interval_size)), axis=1)
        arr[arr==0] = np.nan
        
        result = [0] * Shape[-1]
        for i in range(Shape[-1]):
            for j in range(Shape[1]):
                data[i, j * 12:(j + 1) * 12] = month_data[:, j, i]
            
            data[i, :-1] = data[i, 1:] - data[i, :-1]
            data[i, -1] = 0
            
            val = np.sum(data[i].reshape((size, interval_size)), axis=1)
            result[i] = [i + 1] + list(val / arr)
            
        headers = self.product_request_header(start_date.year, interval_size)
        
        result = self.replace_nan(result)
        Create_SQL('ettersporsel_trend', result, headers)
        
        if get_table is True:
            self.universal_table(result, headers)
            
        return result
    
    def seasonal_trend(self, get_table=False, quarterly=False):
        month_data = self.class_obj.month_data.copy()
        date_list = self.class_obj.key_list
        name = self.class_obj.months.copy()
        n_years = self.class_obj.n_years
        
        start_date = min(date_list)
        end_date = max(date_list)
        
        arr = np.zeros((n_years, 12)) + 1
        arr[0, :start_date.month - 1] -= 1
        arr[-1, end_date.month:] -= 1
        arr = sum(arr).reshape(12, 1)

        data = self.class_obj.merge_years(month_data) / arr
        
        if quarterly is True:
            data = list(np.roll(data, -2, axis=0))
            data = np.array(self.class_obj.merge_months(data, 3))
            name = ['spring', 'summer', 'atumn', 'winter']
        
        header = ['product_id', 'min_amount', 'time_minimum', 
                  'max_amount', 'time_maximum']
        
        def insert_name(idx_list):
            for i, j in enumerate(idx_list):
                idx_list[i] = name[j]
            return idx_list
        
        res = []
        for i in range(len(data[0])):
            val = data[:, i]
            min_val, max_val = min(val), max(val)

            min_idx = list(np.where(val==min_val)[0])
            max_idx = list(np.where(val==max_val)[0])
            
            min_idx = insert_name(min_idx)
            max_idx = insert_name(max_idx)
            
            min_month = ', '.join(min_idx)
            max_month = ', '.join(max_idx)
            
            res.append([i + 1, min_val, min_month, max_val, max_month])
            
        Create_SQL('sesong_trend', res, header)
        
        if get_table is True:
            self.universal_table(res, header)

    def linear_regression(self, x, y):
        n = len(x)
        
        x_mean = np.mean(x)
        y_mean = np.mean(y)
        
        ss_xy = np.sum(x * y) - n * y_mean * x_mean
        ss_xx = np.sum(x * x) - n * x_mean**2
        
        b1 = ss_xy / ss_xx
        b0 = y_mean - b1 * x_mean
        return b0 + b1 * x

    def comparison(self, get_table=False, make_plot=True, idx=2):
        if not(idx in [0, 1, 2]):
            print('\ninvalid integer for column to sort, ' 
                  'defaulting to idx = 2')
            idx = 2 
            
        price = self.detailed_arr[:, 1]
        amount = self.detailed_arr[:, 2]
        discount = self.detailed_arr[:, 3]

        x = amount
        y = discount * price
        ratio = y / x
        
        result = [list(i) for i in zip(x, y, ratio)]
        result = self.sort_list(result, idx, False)
        
        headers = ['volume', 'price', 'price_volume_ratio']
        
        if get_table is True:
            self.universal_table(result, headers)
        
        Create_SQL('pris_vs_volum', result, headers)
        
        if make_plot is True:
            plt.plot(x, self.linear_regression(x, y), color='k', 
                     label='linear regression')
            plt.scatter(x, y, marker='.', color='r', lw=1)
            plt.xlabel('quantity')
            plt.ylabel('price')
            plt.title('price vs quantity')
            plt.legend()
            plt.show()
        

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
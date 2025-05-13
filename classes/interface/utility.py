from sys import exit
import json as js

class Utility:
    def __init__(self):
        self.read_help_file()
    
    def read_help_file(self):
        file = open('support text/help.json', 'r')
        self.data = js.load(file)
        file.close()
    
    def get_json_text(self, text):
        return ' '.join(text)
    
    def get_json_help(self, key):
        help_str = ''
        json_dict = self.data[key]['help']
        for i, j in zip(json_dict.keys(), json_dict.values()):
            help_str += f'{i} {self.get_json_text(j)}'
        return help_str
    
    def request_string(self, input_str=''):
        break_list = ['', 'quit', 'exit', 'stop', 'cancel', 'none', 'default']
        if input_str in break_list:
            input_str = None
        return input_str

    def request_yes_no(self, input_str):
        input_str = input_str.lower()
        statement = ''
        while statement == '':
            if 'yes' in input_str or '1' in input_str:
                statement = True
            elif 'no' in input_str or '0' in input_str:
                statement = False
            elif input_str in ['', 'quit', 'exit', 'stop', 'cancel']:
                print('defaulting to "yes".\n', end=' ')
                statement = True
            else:
                print('\ninvalid input, type "yes" or "no":\n>', end=' ')
                input_str = input().lower()       
        return statement

    def check_number(self, x, default_number):
        message = '\ninvalid input, enter a new number or type "stop":\n>'
        break_list = ['', 'quit', 'exit', 'stop', 'cancel', 'none', 'default']
        while not(isinstance(x, int)):
            try:
                x = int(x)
            except:
                if x.lower() in break_list:
                    print(f'defaulting to {default_number}.\n', end=' ')
                    x = None
                    break
                
                print(message, end=' ')
                x = input()
        return x

    def request_number(self, message=None, set_default=None, number=''):
        while not(isinstance(number, int)):
            if message is not None:
                print(message, end=' ')
            
            number = self.check_number(input().lower(), set_default)
            if number == '' or number is None:
                number = set_default
                break
        
        return number

    def change_default_setting(self, always_default, setting=''):
        message = str('\nset always_default to True or False.'
                      '\nType "true" or "false":\n>')
        print(message, end=' ')
        while not(setting in (True, False)):
            input_str = input().lower()
            
            if input_str in ('true', '1'):
                return True
            elif input_str in ('false', '0'):
                return False
            elif input_str in ['', 'cancel', 'stop', 'break']:
                return always_default
            else:
                print('\ninvalid input, type "true" or "false":\n>', end=' ')
                continue

    def make_title(self, string, default_space=20):
        length = len(string)
        odd = length % 2
        length = int((length - odd) / 2)
        spacing = '-' * (20 - length) 
        padding = '-'*(1 - odd)
        print('\n' + padding + f'{spacing}{string}{spacing}')
    
    def default_feedback(self, statement, locally=False): 
        print(f'\nalways_default is now set to "{statement}".\nQueries '
              f'{"in this category " * locally}'
              f'will{" not" * statement} ask for more options.')
        return

    def support_text(self, key):
        key_list = ['title', 'invalid', 'input', 'commands', 
                    'overview', 'options']
        help_str = self.get_json_help(key)
        
        text_list = []
        for i in range(6):
            if i < 3:
                text = self.data[key][key_list[i]]
            else:
                text = self.get_json_text(self.data[key][key_list[i]])
            
            text_list.append(text)
    
        self.make_title(text_list[0])
        print(text_list[3])
        print(text_list[4])
        return text_list, help_str

    def check_command(self, input_str, help_str, option, 
                      always_default, locally=False):
        if input_str == 'help':
            print(help_str)
        elif input_str == 'option':
            print(option)
        elif input_str in ['quit', 'exit', 'stop'] and locally is True:
            exit()
        elif input_str in ['', 'quit', 'exit', 'stop', 'back', 'up']:
            return 'break'
        elif input_str in ['default', 'default_setting']:
            always_default = self.change_default_setting(always_default)
            self.default_feedback(always_default)
            return 'default', always_default
        else:
            return 'invalid'

    def table_message(self, default=True):
        text = '\nget table in terminal.\nType "yes" or "no":\n>'
        if default is True:
            print(text, end=' ')
        else:
            return text
    
    def use_default_message(self, default=True):
        text = '\nUse default settings.\nType "yes" or "no":\n>'
        if default is True:
            print(text, end=' ')
        else:
            return text
    
    def column_message(self, default=False):
        text = '\nenter a number for corresponding column to sort:\n>'
        if default is True:
            print(text, end=' ')
        else:
            return text
        
    def graph_message(self, default=True):
        text = '\nget a graph/plot.\nType "yes" or "no":\n>'
        if default is True:
            print(text, end=' ')
        else:
            return text
    
    def txt_file_message(self, default=True):
        text = '\nwrite to txt file.\nType "yes" or "no":\n>'
        if default is True:
            print(text, end=' ')
        else:
            return text
from sys import exit
import json as js

class Utility:
    """
    utility methods mainly used in the main.py. These methods are only used for
    the interface, and providing correct descriptions or variables for the 
    queries.
    
    methods:
       read_help_file: reads the help.json
       get_json_text: turns list with strings into a single string
       get_json_help: get the help description from the json file.
       request_string: method to pass either string or return None.
       request_yes_no: method for getting True or False.
       check_number: check if a given number is an int.
       request_number: method for getting and verifying an input as a number.
       change_default_setting: method which ask to change the default setting.
       make_title: method that creates a title for the interface.
       default_feedback: prints out a message when default setting is changed.
       support_text: retrieves all the support text from the json file.
       check_command: checks which command that are chosen from the interface.
       table_message: standard message for printing a table.
       use_default_message: standard message for default settings in a query.
       column_message: standard message for which column to sort the rows by.
       graph_message: standard message for graphs.
       txt_file_message: standard message for txt_file.
    """
    def __init__(self):
        self.read_help_file()
    
    def read_help_file(self):
        """
        read the help.json and saves it as an instance.
        """
        file = open('support text/help.json', 'r')
        self.data = js.load(file)
        file.close()
    
    def get_json_text(self, text):
        """
        takes in list containing strings and turns it into a single string.
        
        args:
            text (list): list of strings.
        
        return:
            a single string.
        """
        return ' '.join(text)
    
    def get_json_help(self, key):
        """
        gather all the help descriptions from the json file in a given key
        and value pair, and turn it into a single string.
        
        args:
            key (str): key for which json key value pair to use.
        
        return:
            help_str (str): complete help description
        """
        help_str = ''
        json_dict = self.data[key]['help']
        for i, j in zip(json_dict.keys(), json_dict.values()):
            help_str += f'{i} {self.get_json_text(j)}'
        return help_str
    
    def request_string(self, input_str=''):
        """
        when asked for a string this method can be used to return a default
        value, None, if the user chooses to.
        
        args:
            input_str (str): string of own choice.
        
        return:
            either the string or None.
        """
        break_list = ['', 'quit', 'exit', 'stop', 'cancel', 'none', 'default']
        if input_str in break_list:
            input_str = None
        return input_str

    def request_yes_no(self, input_str):
        """
        ask for the user to choose between yes/True or no/False.
        
        args:
            input_str (str): string of own choice.
        
        return:
            statement (bool): True or False.
        """
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
        """
        check if a string can be turned into an int.
        
        args:
            x (str): string of own choice to be turned into int.
            default_number (int): the default number to return if the user
                                  doesn't give anything or cancels the process.
        
        return:
            x (int): valid int.
        """
        
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
        """
        asks for a number.
        
        args:
            message (str): custom message to be used.
            set_default (bool or int): decides if None or a custom input is
                                       returned when the default output is 
                                       chosen.
            number (str): not to be used. just there to define the variable and
                          enable the while loop to start.
        
        return:
            number (int): can return None.
        """
        while not(isinstance(number, int)):
            if message is not None:
                print(message, end=' ')
            
            number = self.check_number(input().lower(), set_default)
            if number == '' or number is None:
                number = set_default
                break
        
        return number

    def change_default_setting(self, always_default, setting=''):
        """
        ask if the user want to change the default setting.
        
        args:
            always_default (bool): the current state of the default setting.
            setting (str): not to be used. just there to define the variable 
                           and enable the while loop to start.
        
        return:
            either True or False.
        """
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
        """
        print out the string in a standardized manner.
        
        args:
            string (str): the title to use.
            default_space (int): the default amount of space to use.
        """
        length = len(string)
        odd = length % 2
        length = int((length - odd) / 2)
        spacing = '-' * (20 - length) 
        padding = '-'*(1 - odd)
        print('\n' + padding + f'{spacing}{string}{spacing}')
    
    def default_feedback(self, statement, locally=False):
        """
        print out message when the always_default setting is used or changed.
        
        args:
            statement (bool): the current state of the setting.
            locally (bool): wether this is called from the main menu, or in
                            one of the categories.
        """
        print(f'\nalways_default is now set to "{statement}".\nQueries '
              f'{"in this category " * locally}'
              f'will{" not" * statement} ask for more options.')
        return

    def support_text(self, key):
        """
        read and returns the different support text and descriptions used in
        the interface from either the main menu, or the categories.
        
        args:
            key (str): which key value pair from the json file to use.
        
        return:
            text_list (list): list containing the different strings.
            help_text (str): the help string used when additional 
                             information is needed.
        """
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
        """
        default check used in main menu, and categories when checking for
        which command a user have chosen.
        
        args:
            input_str (str): user input.
            help_str (str): help description.
            option (str): option description.
            always_default (bool): the state of always_default option.
            locally (bool): wether this is called from the main menu, or in
                            one of the categories.
        
        return:
            will return either nothing, a string or a string and bool.
        """
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
        """
        print out a message to the user when a query has been chosen to print
        out the table to the terminal or not.
        
        args:
            default (bool): print out message when True else return 
                            the message itself.
        """
        text = '\nget table in terminal.\nType "yes" or "no":\n>'
        if default is True:
            print(text, end=' ')
        else:
            return text
    
    def use_default_message(self, default=True):
        """
        print out a message to the user when a query has been chosen to use
        the default settings or not.
        
        args:
            default (bool): print out message when True else return 
                            the message itself.
        """
        text = '\nUse default settings.\nType "yes" or "no":\n>'
        if default is True:
            print(text, end=' ')
        else:
            return text
    
    def column_message(self, default=False):
        """
        print out a message to the user when a query has been chosen for
        which column to use when the rows are sorted. 
        
        args:
            default (bool): print out message when True else return 
                            the message itself.
        """
        text = '\nenter a number for corresponding column to sort:\n>'
        if default is True:
            print(text, end=' ')
        else:
            return text
        
    def graph_message(self, default=True):
        """
        print out a message to the user when a query has been chosen to make
        a graph/plot and show it or not making it.
        
        args:
            default (bool): print out message when True else return 
                            the message itself.
        """
        text = '\nget a graph/plot.\nType "yes" or "no":\n>'
        if default is True:
            print(text, end=' ')
        else:
            return text
    
    def txt_file_message(self, default=True):
        """
        print out a message to the user when a query has been chosen to create
        a txt file with the result or not.
        
        args:
            default (bool): print out message when True else return 
                            the message itself.
        """
        text = '\nwrite to txt file.\nType "yes" or "no":\n>'
        if default is True:
            print(text, end=' ')
        else:
            return text
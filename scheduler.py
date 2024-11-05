import sys
from datetime import datetime
import re
import pickle
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter, Completion


def is_valid_format(s):
    pattern = r'^\d{4}-\d{2}-\d{2}$'
    return re.match(pattern, s) is not None

def save(dict,filename):
    with open(filename,'wb') as f:
        pickle.dump(dict,f)

def load(filename):
    try:
        with open(filename, 'rb') as f:
            return pickle.load(f)
    except (FileNotFoundError, EOFError):
        return {}


# 1.2 -- word completer added
__tasks = []
__schedule_day = load('day.pkl')
__schedule_date = load('date.pkl')
__commands = ['insert','quit','inquire','remove','reset','save']
completer_cmd = WordCompleter(__commands)

while(True):
    __tasks = list(__schedule_date.keys())
    completer_task = WordCompleter(__tasks)
    read_in = prompt("command: ",completer = completer_cmd)
    read_in = read_in.split()
    if(len(read_in)!=1):
        print("The commands can only be [inquire] or [insert]")
        break
    read_in = read_in[0]
    
    def echo(__schedule_date,__schedule_day):     
            print("Tasks"," "*26,"\tDays Left")
            print('-'*60)
            today = datetime.now()
            for key,value in __schedule_date.items():
                date = datetime.strptime(value, '%Y-%m-%d')
                delta = date - today
                days_left = delta.days
                __schedule_day[key] = days_left
            
            __schedule_day = dict(sorted(__schedule_day.items(),key=lambda item:item[1]))  
            
            for key,value in __schedule_day.items():    
                padding = 31 - len(key)
                print(f"{key}"," "*padding,f"\t{value} days left")
            print('-'*60)
            
            
    if(read_in == 'inquire'):
        if(len(__schedule_date) == 0):
            print('No elements in the schedule list')
        else: 
            echo(__schedule_date,__schedule_day)
    
    if(read_in == 'save'):
        save(__schedule_date,'date.pkl')
        save(__schedule_day,'day.pkl')
    
    if(read_in == 'quit'):
        save(__schedule_date,'date.pkl')
        save(__schedule_day,'day.pkl')
        sys.exit()
        
    
    if(read_in == 'insert'):    
        while(True):
            num_of_sch = prompt('How many new tasks you want to add?\n')
            try:
                num_of_sch = int(num_of_sch)
            except ValueError:
                print('You need to enter an integer.')
                continue
            else:
                pass
            print('Please enter new tasks in such format:\n[task name]+[due date](YYYY-MM-DD)')
            
            for i in range(num_of_sch):
                task,date = prompt().split()
                if(not is_valid_format(date)):
                    print("Due date must be in the format YYYY-MM-DD")
                    break
                __schedule_date[task] = date
                __schedule_day[task] = 0    
            break 
    
    if(read_in == 'reset'):
        __schedule_date = {}
        __schedule_day = {}
    
    if(read_in == 'remove'):
        if(len(__schedule_date) == 0):
            print('No elements in the schedule list')
        else:
            echo(__schedule_date,__schedule_day)
            print("Which tasks you want to remove? (Enter task names)")
            names = prompt(">>>",completer = completer_task).split()
            for name in names:
                try:
                    del __schedule_date[name]
                    del __schedule_day[name]
                except KeyError:
                    print('Task you want to remove does not exist.')
                else:
                    pass
                
    
    if (not read_in in __commands):
        print('Commands have to be one of the following:\ninsert, quit, inquire , remove , reset , save')
        
            
        
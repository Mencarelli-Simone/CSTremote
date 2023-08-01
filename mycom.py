#%% imports
from win32com.client import Dispatch

#%% Functions, matlab like notation to connect to a com application

def connect(app :str):
    return Dispatch(app)

# just like Methlab
def invoke(com :object, command :str, *args):
    com._FlagAsMethod(command)
    evstr = 'com.' + command + '('
    for s in args:
        if isinstance(s, str):
            evstr += repr(s) +','
        else:
            evstr += str(s)+','
    if len(args) != 0:
        evstr = evstr[0:-1]
    evstr += ')'
    print(evstr)
    return eval(evstr)
# This file defines the framework and implementation of the configuration objects for the application.  Configuration object classes descend from the DictObj class.  
# A DictObj is a dictionary like object only intended to store data - i.e. they are dictionaries, but access is not via obj['key'], but via obj.key for ease of use.
# The two basic DictObj subclasses are:
#    App - configuration parameters for the application - ex: screen resolution, keyboard configuation, midi configuration
#    State - configuration used to generate a graphical frames - ex: numerical parameters sent to the hardware

import re, os, traceback

from migration import *

from common.log import *
from cmdcenter.script import *
set_log("DictObj")


#  setup root directory for serialization
global root
root = "config/"

def set_root(new_root):
    global root
    root = new_root


def save_obj(obj, type, extension, name=None):
    ''' This method serializes any object into the appropriate directory.  
        If no name is provided, the next available one will be generated '''

    path = root + "/" + type + "/" 

    # hack for state
    if(type == "state"):
        type = obj["app"]

    # set name if necessary
    if(not name):
        # ex: dir contains "state_0.est, state_1.est, ..., state_n.est], this returns n + 1
        i = max([-1] + [int(file[(len(type) + 1):(-1 - len(extension))]) for file in os.listdir(path) if re.compile(type + '_(\d+)').match(file)]) + 1
        name = "%s_%d" % (type, i)
       
    try:
        obj["name"] = name
    except:
        debug("couldn't set object name")

    # open file & dump repr(obj)
    loc = path + "%s.%s" % (name, extension)
    file = open(loc, "w")
    file.write(repr(obj).replace(",", ",\n"))
    file.close()

    info("saved %s.%s" % (name, extension))

    return name



def load_obj(type, name, extension):
    ''' This method loads a serialized object from the filesystem. '''

    # open file 
    try:
        global root
        file = root + "/" + type + "/" + name + "." + extension
        file = open(file)
        contents = file.read().replace("\n", "")
        file.close()
    except:
         critical("couldn't open %s.%s" % (name, extension))
         return None  

    # creat object
    try:
        obj = eval(contents)
        return obj
    except:
         critical("couldn't read %s.%s" % (name, extension))
         return None  


class ObserverList(list):
    ''' This is an extension of the list class where observers can be registered to be notified of changes. '''

    def __init__(self, vals):
        list.__init__(self, vals)
        self.observers = []

    def add_observer(self, observer):
        ''' NOTE: An observer here is simply a function that is called when an element of the list is modified.
            It must take args (list, key, val). '''
        self.observers.append(observer)

    # maintain copy of origonal setter
    old_set = list.__setitem__

    def __setitem__(self, key, val):
        # set value
        self.old_set(key, val)

        # notify observers
        for observer in self.observers:
            observer(self, key, val)


class DictObj(object):
    ''' A Dictionary Object is simply an object used solely as a
        dictionary for ease of use '''

    def __init__(self, type, name="default"):
        self.type, self.name = type, name

        if(not self.__dict__.has_key("extension")):
            self.extension = "obj" 

        global root
        self.path = root + "/" + self.type + "/"

            
        # load default object & then update with actual object
        try:
            data = load_obj(self.type, "default", self.extension)
        except:
            critical("Couldn't initialize object: " + name)
            sys.exit(0)
        if(self.name and self.name != "default"):
            data.update(load_obj(self.type, self.name, self.extension))

        self.__dict__.update(data)


    def __setattr__(self, key, val):        
        if(key == 'name' and self.__dict__.has_key('name') and self.name != val):
            self.__dict__ = eval(self.type.capitalize())(val).__dict__
        else:
            object.__setattr__(self, key, val)                          
                 

    def save(self, name=None):
        ''' Dumps a dict to a file.  Adds newlines after commas for legibility. 
            NOTE:  A new object is created by default.'''

        # copy object
        obj = copy.copy(self.__dict__)

        # hack for state
        if(self.type == "state"):
            obj['par'] = list(reduce(lambda s,t: s + t, zip(obj['par_names'], obj['par']), ()))
            del(obj['par_names'])

        # save object
        name = save_obj(obj, self.type, self.extension, name)
        object.__setattr__(self, 'name', name)

        return name


    def update_record(self, key, val):
        ''' Updates the current hard disk record of a particular attribute of this object '''

        # load & update self
        old_self = load_obj(self.type, self.name, self.extension)
        old_self[key] = val

        # update file
        loc = self.path + "%s.%s" % (self.name, self.extension)
        file = open(loc, "w")
        file.write(repr(old_self).replace(",", ",\n"))
        file.close()        


    def rm(self):
        ''' Deletes an object from disk '''

        loc = self.path + "%s.%s" % (self.name, self.extension)

        os.remove(loc)
            
        info("Deleted " + loc)
        

    def merge(self, dict_obj):
        self.__dict__.update(dict_obj.__dict__)


class App(DictObj):
    ''' Configuration settings for the application. '''

    def __init__(self, name="default"):
        self.extension = "app"
        DictObj.__init__(self, 'app', name)


class State(DictObj):
    ''' Configuration parameters for generating Frames. '''

    def __init__(self, name="default"):
        self.extension = "est"
        DictObj.__init__(self, 'state', name)

        # process pars & names
        self.par_names = self.par[::2]
        self.par = self.par[1::2]

        # perform migration
        self.__dict__ = migrate(self.__dict__)

        # make observer lists
        self.zn  = ObserverList(self.zn)
        self.par = ObserverList(self.par)

        # set path phases
        for path in self.paths:
            path.phase = self.time

    def get_par(self, name):
        return self.par[self.par_idx(name)]

    def par_idx(self, name):
        return self.par_names.index(name)

    def set_par(self, name, val):
        self.par[self.par_idx(name)] = val

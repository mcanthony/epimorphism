# This file defines the framework and implementation of the configuration objects for the application.  Configuration object classes descend from the DictObj class.  
# A DictObj is a dictionary like object only intended to store data - i.e. they are dictionaries, but access is not via obj['key'], but via obj.key for ease of use.
# The two basic DictObj subclasses are:
#    App - configuration parameters for the application - ex: screen resolution, keyboard configuation, midi configuration
#    State - configuration used to generate a graphical frames - ex: numerical parameters sent to the hardware

import re, os, copy

import config


#  setup root directory for serialization
global root
root = "config/"

def set_root(new_root):
    global root
    root = new_root


def save_obj(obj, type, extension, app=None, name=None):
    ''' This method serializes any object into the appropriate directory.  
        If no name is provided, the next available one will be generated '''

    path = root + "/" + type + "/" 

    # set name if necessary
    if(not name):
        type = app or type
        # ex: dir contains "state_0.est, state_1.est, ..., state_n.est], this returns n + 1
        idx = max([-1] + [int(file[(len(type) + 1):(-1 - len(extension))]) for file in os.listdir(path) if re.compile(type + '_(\d+)').match(file)]) + 1
        name = "%s_%d" % (type, idx)
       
    try:
        obj["name"] = (app and idx or name)
    except:
        debug("couldn't set object name for saving")

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
        critical("couldn't parse %s.%s" % (name, extension))
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


class ObserverDict(dict):
    ''' This is an extension of the list class where observers can be registered to be notified of changes. '''

    def __init__(self, vals):
        dict.__init__(self, vals)
        self.observers = []

    def add_observer(self, observer):
        ''' NOTE: An observer here is simply a function that is called when an element of the dict is modified.
            It must take args (dict, key, val). '''
        self.observers.append(observer)

    # maintain copy of origonal setter
    old_set = dict.__setitem__

    def __setitem__(self, key, val):
        # set value
        self.old_set(key, val)

        # notify observers
        for observer in self.observers:
            observer(self, key, val)


class DictObj(object):
    ''' A Dictionary Object is simply an object used solely as a
        dictionary for ease of use '''

    def __init__(self, type, app, name):
        self.type, self.app, self.name = type, app, name

        if(not self.__dict__.has_key("extension")):
            self.extension = "obj" 
            
        global root
        self.path = root + "/" + self.type + "/"
            
        # load default objects & then update with actual object
        try:
            data = load_obj(self.type, "default", self.extension)
            data.update(load_obj(self.type, self.app + "_default", self.extension))
        except:
            critical("Couldn't load defaults: " + name)
            sys.exit(0)

        if(self.name != None and self.name != "default"):
            data.update(load_obj(self.type, self.app + '_' + str(self.name), self.extension))

        self.__dict__.update(data)


    def save(self, name=None):
        ''' Dumps a dict to a file.  Adds newlines after commas for legibility. 
            NOTE:  A new object is created by default.'''

        # copy object
        obj = copy.copy(self.__dict__)

        # save object
        name = save_obj(obj, self.type, self.extension, self.app, name)
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
    ''' Configuration settings for an application. '''

    def __init__(self, app, name="default"):
        info("loading app: %s %s" % (app, name))
        self.extension = "app"        
        config.app = self
        self.migrations = {}
        DictObj.__init__(self, 'app', app, name)

    def get_state_name(self):
        return self.state.name

    def set_state(self, name):
        self.state = State(self.app, name)

    def get_substitutions(self):
        return {'POST_PROCESS': self.state.post_process and "#define POST_PROCESS" or ""}
    
    state_name = property(get_state_name, set_state)


class State(DictObj):
    ''' Configuration parameters for generating Frames. '''

    VERSION = 1.0

    def __init__(self, app, name="default"):
        info("loading state: %s %s" % (app, name))
        self.app, self.name = app, name
        self.extension = "est"
        DictObj.__init__(self, 'state', app, name)

        migrations = config.app.migrations

        # perform migrations
        if(self.VERSION < getattr(self.__class__, "VERSION")):
            
            # get necessary migrations
            versions = [version for version in migrations.keys() if version > old_version]
            versions.sort()

            # run migrations
            for version in versions:
                migrations[version]()

            # update VERSION
            self.VERSION = getattr(self.__class__, "VERSION")

        # make observed objects
        self.zn  = ObserverList(self.zn)
        self.par = ObserverDict(self.par)
        self.components = ObserverDict(self.components)

        # set path phases
        for path in self.paths:
            path.phase = self.time


    def __repr__(self):
        return "%s('%s', '%s')" % (self.__class__.__name__, self.app, self.name)
    

# TODO: increment through all states, migrate & save
def migrate_all_states():
    pass

# due to nonsense with dependancy ordering this has to go after the definition of load_obj
from cmdcenter.script import* 

from common.log import *
set_log("DictObj", logging.DEBUG)

from config.migration import *
from phenom.path import *
from phenom.program import *

import re
import os
import traceback

from common.log import *
set_log("DictObj")

global root
root = "config/"

def set_root(new_root):
    global root
    root = new_root


class MidiList(list):
    ''' This is an internal class to add midi synchronization to
        changes in parameters. '''

    def __init__(self, vals):
        self.midi_echo = True
        list.__init__(self, vals)

    # maintain copy of origonal setter
    old_set = list.__setitem__

    def __setitem__(self, key, val):
        # set value
        self.old_set(key, val)

        if(self.midi_echo and hasattr(self, "midi")):
            self.midi.mirror(self, key)




def save_obj(obj, type, extension, name=None):

    path = root + "/".join(type) + "/" 
    
    top_type = type[-1]

    # set name
    if(not name):
        # ex: dir contains "state_0.est, state_1.est, ..., state_n.est], this returns n + 1
        i = max([-1] + [int(file[(len(top_type) + 1):(-1 - len(extension))]) for file in os.listdir(path) if re.compile(top_type + '_').match(file)]) + 1
        name = "%s_%d" % (top_type, i)
        
    obj["name"] = name

    # open file & dump repr(obj)
    loc = path + "%s.%s" % (name, extension)
    file = open(loc, "w")
    file.write(repr(obj).replace(",", ",\n"))
    file.close()

    info("saved %s.%s" % (name, extension))

    return name



def load_obj(type, name, extension):
    # open file & extract contents
#   try:
    global root
    file = root + "/".join(type) + "/" + name + "." + extension
    file = open(file)

    results = file.read().replace("\n", "")
    file.close()

    results = eval(results)

    # evaluate nested fields
    if(results.__class__.__name__ == 'dict'):
        for k in results:
            if(k[0] == "_"):
                results[k] = eval(k[1:].capitalize())(results[k])
                
            
    return results
 #   except:
 #       critical("couldn't read %s" % name)
 #       traceback.print_stack()
 #       return None  


class DictObj(object):
    ''' A Dictionary Object is simply an object used solely as a
        dictionary for ease of use '''

    def __init__(self, type, name="default"):
        self.type, self.name = type, name

        if(not self.__dict__.has_key("extension")):
            self.extension = "obj" 

        global root
        self.path = root + "/".join(self.type) + "/"

        self.top_type = self.type[-1]
            
        data = load_obj(self.type, "default", self.extension)

        if(self.name and self.name != "default"):
            data.update(load_obj(self.type, self.name, self.extension))

        self.__dict__.update(data)


    def children(self):
        return [k for k in self.__dict__ if k[0] == '_']


    def has_key(self, key):
        return self.__dict__.has_key(key) or any([self.__dict__[child].__dict__.has_key(key) for child in self.children()])


    def __setattr__(self, key, val):        
        if(key == 'name' and self.__dict__.has_key('name') and self.name != val):
            self.__dict__ = eval(self.top_type.capitalize())(val).__dict__
        else:
            if(key == "__dict__"):
                object.__setattr__(self, key, val)                          
            for child in self.children():
                if(self.__dict__[child].has_key(key)):
                    object.__setattr__(self.__dict__[child], key, val)
                    return
            object.__setattr__(self, key, val)


    def __dir__(self):
        return ["children", "has_key", "merge", "save", "rm", "__class__", "update_record"]

  
    def __getattribute__(self, key):
        if(key == "__dict__"  or key in dir(self) or self.__dict__.has_key(key)):
            return object.__getattribute__(self, key)
        else:
            for child in self.children():
                val = getattr(self.__dict__[child], key)
                if(val):
                    return val 

        return None
                 

    def save(self, name=None):
        ''' Dumps an object to a file.  Adds newlines after commas for legibility '''

        # copy object
        obj = copy.copy(self.__dict__)

        # save children
        for child in self.children():
            new_name = self.__dict__[child].save(name)
            obj[child] = new_name

        # hack for state
        if(self.top_type == "state"):
            obj['par'] = list(reduce(lambda s,t: s + t, zip(obj['par_names'], obj['par']), ()))
            del(obj['par_names'])

        # save object
        name = save_obj(obj, self.type, self.extension, name)
        object.__setattr__(self, 'name', name)

        return name


    def update_record(self, key, val):
        # load & update self
        old_self = load_obj(self.type, self.name, self.extension)
        old_self[key] = val

        # update file
        loc = self.path + "%s.%s" % (self.name, self.extension)
        file = open(loc, "w")
        file.write(repr(old_self).replace(",", ",\n"))
        file.close()        


    def rm(self):
        ''' Deletes an object and all of its children from disk '''

        # delete children
        for child in self.children():
            self.__dict__[child].rm()

        loc = self.path + "%s.%s" % (self.name, self.extension)

        os.system("rm " + loc)
            
        debug("Deleted " + loc)
        

    def merge(self, dict_obj):
        self.__dict__.update(dict_obj.__dict__)


class App(DictObj):
    ''' Configuration settings for the application. '''

    def __init__(self, name="default"):
        self.extension = "app"
        DictObj.__init__(self, ['app'], name)


class Profile(DictObj):
    ''' Configuration settings for the Engine. '''

    def __init__(self, name="default"):
        self.extension = "prf"
        DictObj.__init__(self, ['app', 'profile'], name)


class Context(DictObj):
    ''' Configuration settings for the Interface. '''

    def __init__(self, name="default"):
        self.extension = "ctx"
        DictObj.__init__(self, ['app', 'context'], name)


class State(DictObj):
    ''' Configuration parameters for generating Frames. '''

    def __init__(self, name="default"):
        self.extension = "est"
        DictObj.__init__(self, ['app', 'state'], name)

        # process pars & names
        self.par_names = self.par[::2]
        self.par = self.par[1::2]

        # perform migration
        self.__dict__ = migrate(self.__dict__)

        # make midi lists
        self.zn  = MidiList(self.zn)
        self.par = MidiList(self.par)

        # set path phases
        for path in self.paths:
            path.phase = self.time


from phenom.script import *

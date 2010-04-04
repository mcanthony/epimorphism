from config.migration import *

import re

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

def load_obj(name):
    # open file & extract contents
        try:
            file = open(name)
            results = file.read()
            file.close()
            return eval(results)
        except:
            critical("couldn't read %s" % name)
            return None  


class DictObj(object):
    ''' A Dictionary Object is simply an object used solely as a
        dictionary for ease of use '''

    def __init__(self, type, name="default"):
        self.type, self.name = type, name
        if(not self.__dict__.has_key("extension")):
            self.extension = "obj" 
        self.path = "config/" + "/".join(self.type) + "/"
        self.top_type = self.type[-1]
        print self.path, self.top_type
            
        data = load_obj(self.path + "default." + self.extension)

        if(self.name != "default"):
            data.update(load_obj(self.path + self.name + "." + self.extension))

        # hack for states
        if(self.top_type == "state"):
            data['par_names'] = data['par'][::2]
            data['par'] = data['par'][1::2]
            data = migrate(data)
            data['zn']  = MidiList(data['zn'])
            data['par'] = MidiList(data['par'])

        self.__dict__.update(data)    
    

    def save(self, name):
        ''' Dumps an object to a file.  Adds newlines after commas for legibility '''

        if(not name):
            # ex: dir contains "state_0.est, state_1.est, ..., state_n.est], this returns n + 1
            i = max([-1] + [int(file[(len(self.top_type) + 1):(-1 - len(self.extension))] for file in os.listdir(self.path) if re.compile(self.top_type + '_').match(file))]) + 1
            name = "%s_%d" % (self.top_type, i)

        debug("with name %s" % name)
        print name
        self.name = name
    
        loc = path + "%s.%s" % (name, self.extension)

        # copy object
        obj = copy.copy(self.__dict__)

        # hack for state
        if(self.top_type == "state"):
            obj['par'] = list(reduce(lambda s,t: s + t, zip(obj['par_names'], obj['par']), ()))
            del(obj['par_names'])

        # open file & dump repr(obj)
        file = open(loc, "w")
        file.write(repr(obj).replace(",", ",\n"))
        file.close()

        info("saved state as: %s" % name)
        return name


    def merge(self, dict_obj):
        self.__dict__.update(dict_obj.__dict__)


class App(DictObj):
    ''' Encapsulates one of each other structs. '''

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


class Environment(DictObj):
    ''' Configuration settings for the application. '''

    def __init__(self, name="default"):
        self.extension = "env"
        DictObj.__init__(self, ['app', 'environment'], name)


class State(DictObj):
    ''' Configuration parameters for generating Frames. '''

    def __init__(self, name="default"):
        self.extension = "est"
        DictObj.__init__(self, ['app', 'state'], name)

        # create midi_lists - for echoing changes back to midi devices
        
        # set path phases
        #for path in self.paths:
        #    path.phase = self.time

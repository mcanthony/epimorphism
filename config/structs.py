from config.migration import *


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


class DictObj(object):
    ''' A Dictionary Object is simply an object used solely as a
        dictionary for ease of use '''

    def __init__(self, **vars):
        # init
        self.__dict__.update(vars)

    def merge(self, dict_obj):
        self.__dict__.update(dict_obj.__dict__)


class State(DictObj):
    ''' Configuration parameters for generating Frames. '''

    def __init__(self, **vars):
        # update dict with migrated vars
        self.__dict__.update(migrate(vars))

        # create midi_lists - for echoing changes back to midi devices
        self.zn  = MidiList(self.zn)
        self.par = MidiList(self.par)
        
        # set path phases
        for path in self.paths:
            path.phase = self.time

        self.time = 0
        


class Profile(DictObj):
    ''' Configuration settings for the Engine. '''


class Context(DictObj):
    ''' Configuration settings for the Interface. '''


class Environment(DictObj):
    ''' Configuration settings for the application. '''


class App(DictObj):
    ''' Encapsulates one of each other structs. '''


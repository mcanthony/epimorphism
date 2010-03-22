from globals import *

import config

import sys
import os.path
import time

from common.log import *
set_log("SCRIPT")

from common.runner import *



class Script(object):
    ''' Contains a timestamped sequence of commands which are executed in the Cmd environment '''


    def __init__(self, name = None):
        debug("Creating script")
        Globals().load(self)

        self.name = name

        self.events = (self.name and config.configmanager.load_obj("script", name)) or []
        self.current_idx = 0


    def _execute(self):
        ''' Internal execution loop '''

        # main execution loop
        while(self.current_idx < len(self.events) and not self.cmdcenter.env.exit):            
            while(self.current_idx < len(self.events) and self.cmdcenter.time() >= self.events[self.current_idx]["time"] and not self.cmdcenter.env.exit):
                if("inc" in self.events[self.current_idx]["cmd"]):
                    async(lambda :self.cmdcenter.cmd(self.events[self.current_idx]["cmd"]))
                else:
                    self.cmdcenter.cmd(self.events[self.current_idx]["cmd"])
                self.current_idx += 1
            if(self.current_idx < len(self.events)):
                t = self.events[self.current_idx]["time"] - self.cmdcenter.time()
                if(t > 0):
                    time.sleep(t)

        debug("Finished executing script")


    def start(self):
        ''' Starts the script '''
        debug("Start script")

        async(self._execute)


    def add_event(self, time, cmd):
        ''' Add an event to the collection of events '''
        debug("Adding event at %f" % time)

        # compute insertion index
        lst = [(i == 0 or time >= self.events[i-1]["time"])
               and (i >= len(self.events) or time <= self.events[i]["time"])
               for i in xrange(len(self.events) + 1)]
        idx = lst.index(True)

        # insert event
        self.events.insert(idx, {"time":time, "cmd":cmd})

        # increment index if necessary
        if(idx < self.current_idx): self.current_idx += 1

    def last_event_time(self):
        ''' Returns the time of the last event '''

        return self.events[-1]["time"]


    def push(self, time, cmd):
        ''' Push an event to the top of the stack '''

        self.events.append({"time":time, "cmd":cmd})


    def save(self, name = None):
        ''' Saves the script '''

        # output events
        self.name = config.configmanager.outp_obj("script", self.events, self.name)

from common.globals import *
from common.structs import *
from common.runner import *

from common.log import *
set_log("SCRIPT")

import time

class Script():
    ''' Contains a timestamped sequence of commands which are executed in the Cmd environment '''

    def __init__(self, name = "default"):
        debug("Creating script")
        self.__dict__ = load_obj("script", name, "scr")


    def save(self, name = None):
        self.name = save_obj({'name':name, 'events':self.events, 'phase':self.phase}, "script", "scr", name)
        return self.name


    def __repr__(self):
        return "Script('%s')" % self.name


    def _execute(self):
        ''' Internal execution loop '''

        if(not self.__dict__.has_key('cmdcenter')):
            Globals().load(self)

        while(len(self.events) > 0 and not self.app.exit and not self.exit):
            next_event = self.events[0]

            t = next_event["time"] + self.phase - self.cmdcenter.time()
            if(t > 0):
                time.sleep(t)

            cmd = next_event["cmd"]

            self.cmdcenter.cmd(cmd)

            self.events.pop(0)

        debug("Finished executing script")


    def start(self):
        ''' Starts the script '''
        debug("Start script")
        Globals().load(self)

        self.exit = False
        async(self._execute)


    def stop(self):
        ''' Stops the script '''
        debug("Stop script")

        self.exit = True


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



#    def __repr__(self):
#        return "Script('%s')" % self.name

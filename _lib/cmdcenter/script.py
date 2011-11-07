from common.globals import *
from program import Program
from common.structs import * 
from common.runner import *

from common.log import *
set_log("SCRIPT")

import time

class Script(Program):
    ''' Contains a timestamped sequence of commands which are executed in the Cmd environment '''

    def __init__(self, name = "default"):
        info("Creating script")
        self.data = load_obj("script", name, "scr")

        Program.__init__(self, self.data)


    def __repr__(self):
        return "Script('%s')" % self.data["name"]


    def _execute(self):
        ''' Internal execution loop '''
        if(len(self.data["events"]) == 0):
            self.exit = True
            return

        self.next_event_t = self.data["events"][0]["time"] + self.data["phase"] - self.cmdcenter.time()

        if(self.next_event_t > 0):
            return

        self.cmdcenter.cmd(self.data["events"].pop(0)["cmd"])


    def save(self, name = None):
        self.data["name"] = save_obj(self.data, "script", "scr", self.app.app, name)
        return self.data["name"]


    def add_event(self, time, cmd):
        ''' Add an event to the collection of events '''
        info("Adding event at %f" % time)

        # compute insertion index
        lst = [(i == 0 or time >= self.data["events"][i-1]["time"])
               and (i >= len(self.data["events"]) or time <= self.data["events"][i]["time"])
               for i in xrange(len(self.data["events"]) + 1)]
        idx = lst.index(True)

        # insert event
        self.data["events"].insert(idx, {"time": time, "cmd": cmd})


    def last_event_time(self):
        ''' Returns the time of the last event '''

        return self.data["events"][-1]["time"]


    def push(self, time, cmd):
        ''' Push an event to the top of the stack '''

        self.data["events"].append({"time":time, "cmd":cmd})

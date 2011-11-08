import config

from common.globals import *
from program import Program
from common.structs import * 
from common.runner import *

from common.log import *
set_log("SCRIPT")

import time

class Script(DictObj, Program):
    ''' Contains a timestamped sequence of commands which are executed in the Cmd environment '''

    def __init__(self, app=None, name = "default"):
        info("Creating script")
        self.extension = "scr"
        Program.__init__(self, None)
        DictObj.__init__(self, "script", app, name)
        self.repr_blacklist += ["exit", "sleep_event", "freeze_event", "next_event_in"]


    def _execute(self):
        ''' Internal execution loop '''

        if(len(self.data["events"]) == 0):
            self.state.programs.remove(self)
            self.exit = True
            return

        self.next_event_in = self.data["events"][0]["time"] + self.data["phase"] - self.cmdcenter.time()

        if(self.next_event_in > 0):
            return

        self.cmdcenter.cmd(self.data["events"].pop(0)["cmd"], False)


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

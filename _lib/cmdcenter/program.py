from common.globals import *

import time, threading

from common.runner import *

from common.log import *
set_log("Program")

class Program(threading.Thread):

    def __init__(self, data):

        self.data = data
        info("Starting program: %s", str(self))

        self.exit = False
        self.freeze_event = threading.Event()
        self.freeze_event.set()
        self.sleep_event = threading.Event()

        self.next_event_t = None

        # init thread
        threading.Thread.__init__(self)


    def freeze(do_freeze):
        if(do_freeze):
            self.freeze_event.set()
        else:
            self.freeze_event.clear()

    def stop(self):
        self.exit = True
        self.sleep_event.set()
        self.state.programs.remove(self)


    def run(self):
        if(not hasattr(self, 'app')):
            Globals.load(self)
        
        while(not self.app.exit and not self.exit):  
            self._execute()
            self.freeze_event.wait()
            self.sleep_event.wait(self.next_event_t)

    def _execute(self):
        pass


    def __repr__(self):
        return "%s(%s)" % (self.__class__.__name__, str(self.data))

from common.globals import *

import random, time, threading

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
        
        time.sleep(5)
        print self.app.exit, self.exit
        while(not self.app.exit and not self.exit):  
            self._execute()
            self.freeze_event.wait()


    def _execute(self):
        pass


    def __repr__(self):
        return "%s(%s)" % (self.__class__.__name__, str(self.data))



class RandomComponents(Program):
    def _execute(self):
        debug("Executing Random Components")
        i = random.randint(0, self.data["scope"])            
        if(i == 0):
            async(lambda :self.cmdcenter.cmd("inc_data('T', 0)"))
        elif(i == 1):
            async(lambda :self.cmdcenter.cmd("inc_data('T_SEED', 0)"))
        elif(i == 2):
            async(lambda :self.cmdcenter.cmd("inc_data('SEED_W', 0)"))
        elif(i == 3):
            async(lambda :self.cmdcenter.cmd("inc_data('SEED_WT', 0)"))
        elif(i == 4):
            async(lambda :self.cmdcenter.cmd("inc_data('SEED_A', 0)"))
        elif(i == 5):
            async(lambda :self.cmdcenter.cmd("inc_data('SEED', 0)"))            

        self.sleep_event.wait(self.data["interval"] * (0.5 + random.random()))

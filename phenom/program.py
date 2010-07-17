from common.globals import *

import random
import time

from common.runner import *

class Program(object):

    def __init__(self, data):
        self.data = data
        self.phase = 0
        self.exit = False
        self.running = False


    def stop(self):
        self.exit = True
        self.running = False

    
    def start(self):
        Globals().load(self)
        self.running = True
        async(self._execute)


    def _execute(self):
        pass


    def __repr__(self):
        return "%s(%s)" % (self.__class__.__name__, str(self.data))



class RandomComponents1(Program):
    def _execute(self):
        while(not self.exit and not self.app.exit):

            i = random.randint(0,2)
            if(i == 0):
                async(lambda :self.cmdcenter.cmd("inc_data('T', 0)"))
            elif(i == 1):
                async(lambda :self.cmdcenter.cmd("inc_data('T_SEED', 0)"))
            elif(i == 2):
                async(lambda :self.cmdcenter.cmd("inc_data('SEED_W', 0)"))
                        
            time.sleep(self.data["interval"] * 0.5 + rand.randint(0, self.data["interval"]))


class RandomComponents2(Program):
    def _execute(self):
        while(not self.exit and not self.app.exit):
            
            i = random.randint(0,4)
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

            # make this better
            t = self.data["interval"] * 0.5 + random.randint(0, self.data["interval"]) + self.cmdcenter.time()
            while(self.cmdcenter.time() < t and not self.app.exit):
                time.sleep(0.1)
            #time.sleep()

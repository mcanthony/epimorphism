from cmdcenter.program import Program

import random

from common.runner import *

from common.log import *
set_log("Program")


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

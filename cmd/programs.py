from cmdcenter.program import Program

import random

from common.runner import *

from common.log import *
set_log("Program")


class RandomComponents(Program):
    def _execute(self):
        debug("Executing Random Components")

        self.next_event_in = self.data["interval"] * (0.5 + random.random())

        # update all components if necessary
        if(not hasattr(self, "initialized")):
            self.initialized = True
            update = {}
            for component_name in ['T', 'T_SEED', 'SEED_W', 'SEED_WT', 'SEED_A'][0:self.data["scope"]]:
                update[component_name] = config.cmdcenter.componentmanager.inc_data(component_name, random.randint(0,100000), True)
        
            print "UPDATE", update
            config.cmdcenter.componentmanager.switch_components(update)
            return

        i = random.randint(0, self.data["scope"])            
        if(i == 0):
            async(lambda :self.cmdcenter.cmd("inc_data('T', 0)", False))
        elif(i == 1):
            async(lambda :self.cmdcenter.cmd("inc_data('T_SEED', 0)", False))
        elif(i == 2):
            async(lambda :self.cmdcenter.cmd("inc_data('SEED_W', 0)", False))
        elif(i == 3):
            async(lambda :self.cmdcenter.cmd("inc_data('SEED_WT', 0)", False))
        elif(i == 4):
            async(lambda :self.cmdcenter.cmd("inc_data('SEED_A', 0)", False))
        elif(i == 5):
            async(lambda :self.cmdcenter.cmd("inc_data('SEED', 0)", False))            


class RandomAllComponents(Program):
    def _execute(self):
        debug("Execute random All Components")

        self.next_event_in = self.data["interval"] * (0.5 + random.random())

        update = {}
        for component_name in ['T', 'T_SEED', 'SEED_W', 'SEED_WT', 'SEED_A'][0:self.data["scope"]]:
            update[component_name] = config.cmdcenter.componentmanager.inc_data(component_name, random.randint(0,100000), True)
        
        config.cmdcenter.componentmanager.switch_components(update)

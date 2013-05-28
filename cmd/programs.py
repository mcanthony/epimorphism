from cmdcenter.program import Program
from cmd.paths import *

import random, os, math

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
            for component_name in ['T', 'T_SEED', 'SEED_W', 'SEED_WT', 'SEED_A', 'SEED'][0:self.data["scope"]]:
                update[component_name] = config.cmdcenter.componentmanager.inc_data(component_name, random.randint(0,100000), True)
        
            # print "UPDATE", update
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
        for component_name in ['T', 'T_SEED', 'SEED_W', 'SEED_WT', 'SEED_A', 'SEED'][0:self.data["scope"]]:
            update[component_name] = config.cmdcenter.componentmanager.inc_data(component_name, 0, True)
        
        config.cmdcenter.componentmanager.switch_components(update)

        
class RandomVideoComponents(Program):
    def _execute(self):
        debug("Execute random All Components")

        self.next_event_in = self.data["interval"] * (0.5 + random.random())

        update = {}
        for component_name in ['T', 'T_SEED0', 'SEED_W0', 'SEED_WT0', 'SEED_A0', 'SEED_C0', 'T_SEED1', 'SEED_W1', 'SEED_WT1', 'SEED_A1', 'SEED_C1', 'T_SEED2', 'SEED_W2', 'SEED_WT2', 'SEED_A2', 'SEED_C2'][0:self.data["scope"]]:
            update[component_name] = config.cmdcenter.componentmanager.inc_data(component_name, 0, True)
        
        config.cmdcenter.componentmanager.switch_components(update)        


class RandomGridAux(Program):
    def _execute(self):
        debug("Executing Random Grid Aux")

        self.next_event_in = self.data["interval"] * (0.5 + random.random())        

        textures = [ f for f in os.listdir("media/textures") ]

        i = random.randint(0, len(textures) - 1)

#        config.cmdcenter.load_image(textures[i])


class SwitchAux(Program):
    def _execute(self):
        debug("Switching aux %d to %s" % (self.data["idx"], self.data["tex"]))

        # see if we're already switching.  done a bit ghettoly.  not even sure if it works
        cur = config.cmdcenter.state.par["_SEED_TEX_IDX"][self.data["idx"]]
        if math.fabs(cur - round(cur)) > 0.1:
            debug("Already switching aux %d" % self.data["idx"])
            return

        ofs = (round(cur) == 0 and 1 or 0)

        # load image
        config.cmdcenter.load_image(self.data["tex"], self.data["idx"] + ofs)

        # add path
        config.cmdcenter.state.paths.append(Linear1D("par['_SEED_TEX_IDX']", self.data["idx"], config.cmdcenter.app.state_intrp_time, {'s':1.0 - ofs, 'e':ofs, 'loop':False}))

        
        

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
        for component_name in ['T', 'T_SEED0', 'SEED_W0', 'SEED_WT0', 'SEED_A0', 'SEED'][0:self.data["scope"]]:
            update[component_name] = config.cmdcenter.componentmanager.inc_data(component_name, 0, True)
        
        config.cmdcenter.componentmanager.switch_components(update)

        
class RandomMain(Program):
    def _execute(self):
        debug("Execute random All Components")
        self.next_event_in = self.data["interval"] * (0.5 + random.random())

        update = {}

        programs = []
        # seed 0                
        for component_name in ['T', 'T_SEED0', 'SEED_W0', 'SEED_WT0', 'SEED_A0']:
            update[component_name] = config.cmdcenter.componentmanager.inc_data(component_name, 0, True)
        update["SEED_C0"] = 'tex_color(idx, fb, aux, z, seed, par, time)'

        programs.append(RandomAux({'idx': 0, 'folder': 'simplegeom'}))

        # seed 1
        if random.random() > 0.4:
            for component_name in ['T_SEED1', 'SEED_W1', 'SEED_WT1', 'SEED_A1']:
                update[component_name] = config.cmdcenter.componentmanager.inc_data(component_name, 0, True)
            update["SEED1"] = "seed_multi_wca(idx, frame, z, fb, aux, par, internal, zn, time)"
            update["SEED_C1"] = 'tex_color(idx, fb, aux, z, seed, par, time)'
            rnd = random.random()
            if rnd < 0.33:
                programs.append(RandomAux({'idx': 1, 'folder': 'Vasarely'}))
            elif rnd < 0.66:
                programs.append(RandomAux({'idx': 1, 'folder': 'misc'}))
            else:
                programs.append(RandomAux({'idx': 1, 'folder': 'simplegeom'}))
        else:
            update["SEED1"] = "seed_id(idx, frame, z, fb, aux, par, internal, zn, time)"            

        # seed 2
        if random.random() > 0.2:
            for component_name in ['T_SEED2', 'SEED_W2', 'SEED_WT2', 'SEED_A2']:
                update[component_name] = config.cmdcenter.componentmanager.inc_data(component_name, 0, True)
            update["SEED_C2"] = 'tex_color(idx, fb, aux, z, seed, par, time)'
            update["SEED2"] = "seed_multi_wca(idx, frame, z, fb, aux, par, internal, zn, time)"
            rnd = random.random()
            if rnd < 0.33:            
                programs.append(RandomAux({'idx': 2, 'folder': 'flowers'}))
            elif rnd < 0.66:
                programs.append(RandomAux({'idx': 2, 'folder': 'misc'}))
            else:
                programs.append(RandomAux({'idx': 2, 'folder': 'nontile'}))
        else:
            update["SEED2"] = "seed_id(idx, frame, z, fb, aux, par, internal, zn, time)"            

        if random.random() > 0.6:
            update["COLOR"] = "rotate_hsls(v, z_z, par, time)"
            update["POST"] = "post_colors3(v, par, time)"
        else:
            update["COLOR"] = "bgr_id(v, z_z, par, time)"
            update["POST"] = "post_gamma(v, par, time)"                


        def start_programs():
            for program in programs:
                print "program"
                config.cmdcenter.state.programs.append(program)
                program.run()

        #start_programs()
        config.cmdcenter.componentmanager.switch_components(update, start_programs)        


class RandomAux(Program):
    def _execute(self):
        debug("Executing Random Aux")

        if not self.data.has_key("folder"):
            self.data["folder"] = ""
        path = "media/textures/" + self.data["folder"] + '/'
        textures = [f for f in os.listdir(path) if os.path.isfile(path + f)]

        i = random.randint(0, len(textures) - 1)
        prg = SwitchAux({'idx': self.data['idx'], 'tex': self.data["folder"] + '/' + textures[i]})
        config.cmdcenter.state.programs.append(prg)
        prg.run()

        # remove self.  should ideally happen after execution terminates
        self.stop()


class SwitchAux(Program):
    def _execute(self):
        debug("Switching aux %d to %s" % (self.data["idx"], self.data["tex"]))

        # see if we're already switching.  done a bit ghettoly.  not even sure if it works
        cur = config.cmdcenter.state.par["_SEED_TEX_IDX"][self.data["idx"]]
#        if math.fabs(cur - round(cur)) > 0.1:
#            debug("Already switching aux %d" % self.data["idx"])
#            return

        ofs = (round(cur) == 0 and 1 or 0)

        # load image
        config.cmdcenter.load_image(self.data["tex"], self.data["idx"] + ofs)

        # add path
        config.cmdcenter.state.paths.append(Linear1D("par['_SEED_TEX_IDX']", self.data["idx"], config.cmdcenter.app.state_intrp_time * config.cmdcenter.state.t_speed, {'s':1.0 - ofs, 'e':ofs, 'loop':False}))

        # remove self.  should ideally happen after execution terminates
        self.stop()
        
        
class RandomInterference(Program):
    def _execute(self):
        debug("Execute random Interference")
    
        self.next_event_in = self.data["interval"] * (0.5 + random.random())

        config.cmdcenter.state.par['_N'][0] = random.randint(1, 8)
        config.cmdcenter.state.par['_SLICES'][0] = random.randint(1, 5)
        config.cmdcenter.cmd("inc_data('T', 0)")
            


from cmdcenter.program import Program
from cmdcenter.script import *
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
        if self.data["interval"]:
            self.next_event_in = self.data["interval"] * (0.5 + random.random())

        update = {}

        programs = []
        # seed 0
        for component_name in ['T', 'T_SEED0', 'SEED_W0', 'SEED_WT0', 'SEED_A0']:
            update[component_name] = config.cmdcenter.componentmanager.inc_data(component_name, 0, True)
        update["SEED_C0"] = 'tex_color(idx, fb, aux, z, seed, par, time)'
        
        no_more = False
        if(not "no_aux" in self.data or not self.data["no_aux"]):
            if random.random() <= 0.50:
                programs.append(RandomAux({'idx': 0, 'folder': 'simplegeom'}))
            else:
                programs.append(RandomAux({'idx': 0, 'folder': 'psych'}))

        # seed 1
        if random.random() > 0.3 and not no_more:
            for component_name in ['T_SEED1', 'SEED_W1', 'SEED_WT1', 'SEED_A1']:
                update[component_name] = config.cmdcenter.componentmanager.inc_data(component_name, 0, True)
            update["SEED1"] = "seed_multi_wca(idx, frame, z, fb, aux, par, internal, zn, time)"
            update["SEED_C1"] = 'tex_color(idx, fb, aux, z, seed, par, time)'
            rnd = random.random()

            if rnd < 0.25:
                programs.append(RandomAux({'idx': 1, 'folder': 'Vasarely'}))
            elif rnd < 0.50:
                programs.append(RandomAux({'idx': 1, 'folder': 'misc'}))
            elif rnd < 0.75:
                programs.append(RandomAux({'idx': 1, 'folder': 'psych'}))
            else:
                programs.append(RandomAux({'idx': 1, 'folder': 'simplegeom'}))
        else:
            update["SEED_W1"] = "nothing(idx, z, par)"

        # seed 2
        if random.random() > 0.2 and not no_more:
            for component_name in ['T_SEED2', 'SEED_W2', 'SEED_WT2', 'SEED_A2']:
                update[component_name] = config.cmdcenter.componentmanager.inc_data(component_name, 0, True)
            update["SEED_C2"] = 'tex_color(idx, fb, aux, z, seed, par, time)'
            update["SEED2"] = "seed_multi_wca(idx, frame, z, fb, aux, par, internal, zn, time)"

            rnd = random.random()
            if rnd < 0.29:
                programs.append(RandomAux({'idx': 2, 'folder': 'flowers'}))
            elif rnd < 0.58:
                programs.append(RandomAux({'idx': 2, 'folder': 'misc'}))
            elif rnd < 0.85:
                programs.append(RandomAux({'idx': 2, 'folder': 'nontile'}))
            else:
                programs.append(RandomAux({'idx': 2, 'folder': 'stoopid'}))
        else:
            update["SEED_W1"] = "nothing(idx, z, par)"



        if random.random() > 0.3:
            update["COLOR"] = "rotate_hsls(v, z_z, par, time)"
            update["POST"] = "post_colors3(v, par, time)"
        else:
            update["COLOR"] = "bgr_id(v, z_z, par, time)"
            update["POST"] = "post_gamma(v, par, time)"


        def start_programs():
            for program in programs:
                config.cmdcenter.state.programs.append(program)
                program.run()

        #start_programs()
        config.cmdcenter.componentmanager.switch_components(update, start_programs)

class RandomPonies(Program):
    def _execute(self):
        programs = []
        programs.append(RandomAux({'idx': 0, 'folder': 'ponies'}))
        programs.append(RandomAux({'idx': 1, 'folder': 'ponies'}))
        programs.append(RandomAux({'idx': 2, 'folder': 'ponies'}))

        for program in programs:
            config.cmdcenter.state.programs.append(program)
            program.run()
    

class RandomMain2(Program):
    def _execute(self):
        debug("Execute random All Main2")
        self.next_event_in = self.data["interval"] * (0.5 + random.random())

        update = {}
        programs = []

        def random_image(idx):
            rnd = random.random()
            if rnd < 0.5:
                programs.append(RandomAux({'idx': idx, 'folder': '4'}))
            elif rnd < 0.75:
                programs.append(RandomAux({'idx': idx, 'folder': '3'}))
            elif rnd < 0.92:
                programs.append(RandomAux({'idx': idx, 'folder': '2'}))
            elif rnd < 0.98:
                programs.append(RandomAux({'idx': idx, 'folder': '12'}))
            elif rnd < 1.0:
                programs.append(RandomAux({'idx': idx, 'folder': '11'}))


        # first seed
        for component_name in ['T', 'T_SEED0', 'SEED_W0', 'SEED_WT0', 'SEED_A0']:
            update[component_name] = config.cmdcenter.componentmanager.inc_data(component_name, 0, True)

        update["SEED0"] = "seed_multi_wca(idx, frame, z, fb, aux, par, internal, zn, time)"
        update["SEED_C0"] = 'tex_color(idx, fb, aux, z, seed, par, time)'
        random_image(0)

        # second seed
        if random.random() > 0.7:
            debug("Adding 2nd seed")
            for component_name in ['T_SEED1', 'SEED_W1', 'SEED_WT1', 'SEED_A1']:
                update[component_name] = config.cmdcenter.componentmanager.inc_data(component_name, 0, True)

            update["SEED1"] = "seed_multi_wca(idx, frame, z, fb, aux, par, internal, zn, time)"
            update["SEED_C1"] = 'tex_color(idx, fb, aux, z, seed, par, time)'
            random_image(1)

            # third seed
            if random.random() > 0.5:
                debug("Adding 3nd seed")
                for component_name in ['T_SEED2', 'SEED_W2', 'SEED_WT2']:
                    update[component_name] = config.cmdcenter.componentmanager.inc_data(component_name, 0, True)
                update["SEED_A2"] = 'solid_alpha(idx, w, res, par)'
                update["SEED2"] = "seed_multi_wca(idx, frame, z, fb, aux, par, internal, zn, time)"
                update["SEED_C2"] = 'tex_color(idx, fb, aux, z, seed, par, time)'
                random_image(2)
            else:
                update["SEED_W2"] = "nothing(idx, z, par)"
        else:
            update["SEED_W2"] = "nothing(idx, z, par)"
            update["SEED_W1"] = "nothing(idx, z, par)"

        # colorization
        if random.random() > 0.6:
            update["COLOR"] = "rotate_hsls(v, z_z, par, time)"
            update["POST"] = "post_colors3(v, par, time)"
        else:
            update["COLOR"] = "bgr_id(v, z_z, par, time)"
            update["POST"] = "post_gamma(v, par, time)"


        def start_programs():
            for program in programs:
                config.cmdcenter.state.programs.append(program)
                program.run()

        #start_programs()
        config.cmdcenter.componentmanager.switch_components(update, start_programs)


class RandomAux(Program):
    def _execute(self):
        debug("Executing Random Aux")

        self.data["folder"] = 'ponies'
        
        if not self.data.has_key("folder"):
            self.data["folder"] = ""
        path = "media/textures/" + self.data["folder"] + '/'
        textures = [f for f in os.listdir(path) if os.path.isfile(path + f)]

        i = random.randint(0, len(textures) - 1)
        config.cmdcenter.switch_aux(self.data['idx'], self.data["folder"] + '/' + textures[i])

        # remove self.  should ideally happen after execution terminates
        self.stop()


class SwitchAux(Program):
    def _execute(self):
        debug("Switching aux %d to %s" % (self.data["idx"], self.data["tex"]))
        print "Switching aux %d to %s" % (self.data["idx"], self.data["tex"])

        # see if we're already switching.  done a bit ghettoly.  not even sure if it works
        cur = config.cmdcenter.state.par["_SEED_TEX_IDX"][self.data["idx"]]
#        if math.fabs(cur - round(cur)) > 0.1:
#            debug("Already switching aux %d" % self.data["idx"])
#            return
        ofs = (round(cur) == 0 and 1 or 0)

        #print "cur, ofs", cur, ofs

        # load image
        config.cmdcenter.load_image(self.data["tex"], 2 * self.data["idx"] + ofs)

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


class FOG(Program):
    def _execute(self):
        debug("Execute Face of God program")
        config.cmdcenter.state.t_phase -= config.cmdcenter.state.time
        t = 16 * 4 * 60.0 / config.cmdcenter.state.bpm * config.cmdcenter.state.audio_block
        config.cmdcenter.play_mp3("face_of_god", 44100, t)
        config.cmdcenter.run_program(BeatScript("epimorphism", "fog"))

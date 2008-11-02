from ctypes import *
import pickle
import os.path

from noumena.logger import *



class State:
    def __init__(self, **vars):
        self.__dict__.update(vars)


class Profile:
    def __init__(self, **vars):
        self.__dict__.update(vars)


class StateManager:
    def load_state(self, state_name, **vars):
        log("st: load state - " + state_name)
        log("st: with vars - " + str(vars))

        state = State(manual_iter=False, FRACT=4, T="zn[0] * i(S(z))", SEED="fade_frame", COLORIFY="rg_swizzle", par=(c_float * 40)(), zn=[complex(0,0) for i in range(5)], short_damping = 10)
        state.zn[0] = complex(2.0, 0)
        #self.save_state(state, "default")
        return state

        #file = open("phenom/state/" + state_name + ".epi", "r")
        #return pickle.load(file)


    def load_profile(self, profile_name, **vars):
        log("st: load profile - " + profile_name)
        log("st: with vars - " + str(vars))

        file = open("noumena/profile/" + profile_name + ".prf", "r")
        #return pickle.load(file)

        # temporary
        profile = Profile(name=profile_name, viewport_width=900, viewport_height=900, full_screen=False, viewport_refresh=60, vp_scale=1.0, vp_center_x=0.0, 
                          vp_center_y=0.0, kernel_dim=1024, debug_freq=125.0)
        self.save_profile(profile, "box1")
        return profile


    def save_state(self, state, name=''):
        log("st: save state")

        if(name == ''):
            i = 0
            while(os.path.exists("phenom/state/state_" + i + ".epi")):
                i += 1
            name = "state_" + i

        log("st:   as " + name)

        file = open("phenom/state/" + name + ".epi", "w")
        pickle.dump(state, file)


    def save_profile(self, profile, name):
        log("st: save profile")
        log("st:   as " + name)

        file = open("noumena/profile/" + name + ".prf", "w")
        pickle.dump(profile, file)

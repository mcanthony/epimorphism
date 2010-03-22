from common.complex import *
from common.runner import *
import random

def linear_1d(self, t, data):
    ''' 1 dimensional linear path '''

    if(t > 1):
        t = data['loop'] and fmod(t, 1.0) or 1

    return (data['s'] * (1 - t) + data['e'] * t, t != 1 or data['loop'])


def linear_2d(self, t, data):
    ''' 2 dimensional linear path '''

    if(t > 1):
        t = data['loop'] and fmod(t, 1.0) or 1

    return (complex(data['s'].real * (1 - t) + data['e'].real * t,
                    data['s'].imag * (1 - t) + data['e'].imag * t), t != 1 or data['loop'])


def radial_2d(self, t, data):
    ''' 2 dimensional radial path '''

    if(t > 1):
        t = data['loop'] and fmod(t, 1.0) or 1

    z = [data['s'][0] * (1 - t) + data['e'][0] * t, data['s'][1] * (1 - t) + data['e'][1] * t]

    return (p_to_r(z), t != 1 or data['loop'])


def radial_2d_step(self, t, data):
    ''' 2 dimensional radial path '''

    if(t > 1):
        t = data['loop'] and fmod(t, 1.0) or 1

    z = [data['s'][0] * (1 - t) + data['e'][0] * t, data['s'][1] * (1 - t) + data['e'][1] * t]

    return (p_to_r(z), t != 1 or data['loop'])


def wave_1d(self, t, data):
    ''' 1 dimensional sinousoidal path '''

    return (data['a'] * sin(2.0 * pi * t + data['th']) + data['b'], True)


def rose(self, t, data):
    ''' a rose curve '''

    return (p_to_r([data['c'] + data['a'] * cos(data['b'] * t), t]), True)


def random_components1(self, t, data):
    if(not self.__dict__.has_key('last_event_time1')):
        self.last_event_time1 = 0.0
        random.seed()

    if(t - self.last_event_time1 > data["interval"]):
        self.last_event_time1 = t

        i = random.randint(0,2)
        if(i == 0):
            async(lambda :self.cmdcenter.cmd("inc_data('T', 1)"))
        elif(i == 1):
            async(lambda :self.cmdcenter.cmd("inc_data('T_SEED', 1)"))
        elif(i == 2):
            async(lambda :self.cmdcenter.cmd("inc_data('SEED_W', 1)"))


    return (None, True)


def random_components2(self, t, data):
    if(not self.__dict__.has_key('last_event_time1')):
        self.last_event_time1 = 0.0
        random.seed()

    if(t - self.last_event_time2 > data["interval"]):
        self.last_event_time2 = t

        i = random.randint(0,4)
        if(i == 0):
            async(lambda :self.cmdcenter.cmd("inc_data('T', 1)"))
        elif(i == 1):
            async(lambda :self.cmdcenter.cmd("inc_data('T_SEED', 1)"))
        elif(i == 2):
            async(lambda :self.cmdcenter.cmd("inc_data('SEED_W', 1)"))
        elif(i == 3):
            async(lambda :self.cmdcenter.cmd("inc_data('SEED_WT', 1)"))
        elif(i == 4):
            async(lambda :self.cmdcenter.cmd("inc_data('SEED_A', 1)"))

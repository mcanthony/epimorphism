from common.complex import *
from common.runner import *
import random

def linear_1d(self, t):
    ''' 1 dimensional linear path '''

    if(t > 1):
        t = self.loop and fmod(t, 1.0) or 1

    return (self.s * (1 - t) + self.e * t, t != 1 or self.loop)


def linear_2d(self, t):
    ''' 2 dimensional linear path '''

    if(t > 1):
        t = self.loop and fmod(t, 1.0) or 1

    return (complex(self.s.real * (1 - t) + self.e.real * t,
                    self.s.imag * (1 - t) + self.e.imag * t), t != 1 or self.loop)


def radial_2d(self, t):
    ''' 2 dimensional radial path '''

    if(t > 1):
        t = self.loop and fmod(t, 1.0) or 1

    z = [self.s[0] * (1 - t) + self.e[0] * t, self.s[1] * (1 - t) + self.e[1] * t]

    return (p_to_r(z), t != 1 or self.loop)


def radial_2d_step(self, t):
    ''' 2 dimensional radial path '''

    if(t > 1):
        t = self.loop and fmod(t, 1.0) or 1

    z = [self.s[0] * (1 - t) + self.e[0] * t, self.s[1] * (1 - t) + self.e[1] * t]

    return (p_to_r(z), t != 1 or self.loop)


def wave_1d(self, t):
    ''' 1 dimensional sinousoidal path '''

    return (self.a * sin(2.0 * pi * t + self.th) + self.b, True)


def wave_zr(self, t):
    ''' complex sinousoidal radius path '''       

    return (p_to_r([self.a * sin(2.0 * pi * t + self.th) + self.b, 0]), True)


def rose(self, t):
    ''' a rose curve '''

    return (p_to_r([self.a * cos(self.b * t) + self.c, t]), True)

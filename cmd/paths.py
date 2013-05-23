from cmdcenter.path import Path

from common.complex import *
from common.runner import *
import random

import math

class Linear1D(Path):
    ''' 1 dimensional linear path '''
    def do(self, t):
        if(t > 1):
            t = self.loop and fmod(t, 1.0) or 1

        return (self.s * (1 - t) + self.e * t, t != 1 or self.loop)


class Linear2D(Path):
    ''' 2 dimensional linear path '''
    def do(self, t):
        if(t > 1):
            t = self.loop and fmod(t, 1.0) or 1

        return (complex(self.s.real * (1 - t) + self.e.real * t,
                        self.s.imag * (1 - t) + self.e.imag * t), t != 1 or self.loop)


class Radial2D(Path):
    ''' 2 dimensional radial path '''
    def do(self, t):
        if(t > 1):
            t = self.loop and fmod(t, 1.0) or 1

        z = [self.s[0] * (1 - t) + self.e[0] * t, self.s[1] * (1 - t) + self.e[1] * t]

        return (p_to_r(z), t != 1 or self.loop)


class Radial2DStep(Path):
    ''' 2 dimensional radial path, moving by steps '''
    def do(self, t):
        if(t > 1):
            t = self.loop and fmod(t, 1.0) or 1

        z = [self.s[0] * (1 - t) + self.e[0] * t, self.s[1] * (1 - t) + self.e[1] * t]

        return (p_to_r(z), t != 1 or self.loop)


class Wave1D(Path):
    ''' 1 dimensional sinousoidal path '''
    def do(self, t):
        return (self.a * sin(2.0 * pi * (t + self.th)) + self.b, True)


class WaveZR(Path):
    ''' complex sinousoidal radius path '''       
    def do(self, t):
        return (p_to_r([self.a * sin(2.0 * pi * (t + self.th)) + self.b, 0]), True)


class Rose(Path):
    ''' a rose curve '''
    def do(self, t):
        return (p_to_r([self.a * cos(self.b * t) + self.c, t]), True)

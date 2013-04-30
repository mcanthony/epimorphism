import config

from common.globals import *

from common.complex import *

from common.runner import *

import random

class EventManager(object):


    def __init__(self):
        Globals().load(self)


    def handle_event(f):
        def inner(self, element, multiplier=0):
            old_time = self.app.state_intrp_time
            time = 60.0 / self.state.bpm * (2 ** multiplier)
            self.cmdcenter.cmd("app.state_intrp_time = %f" % time)
            #self.app.state_intrp_time = 2.0#time

            f(self, element, time)

            self.cmdcenter.cmd("app.state_intrp_time = %f" % old_time)
            # self.app.state_intrp_time = old_time

        return inner

    def setT(self, val):
        self.cmdcenter.cmd("switch_component('T', '%s')" % val)

#    @handle_event
#    def switch_component(self, component, multiplier=0):
#        ''' Switches a component '''

#        self.cmdcenter.cmd("inc_data('%s', 1)" % component)


    @handle_event
    def rotate360(self, component, time=1):
        ''' Rotates a zn by 360 deg '''

        z0 = r_to_p(self.state.zn[component])
        z1 = [z0[0], z0[1]]
        z1[1] += 2.0 * pi
        self.cmdcenter.cmd('radial_2d("zn", %d, %f, %s, %s)' % (component, time, str(z0), str(z1)))


    @handle_event
    def rotate180(self, component, time=1):
        ''' Rotates a zn by 180 deg '''

        z0 = r_to_p(self.state.zn[component])
        z1 = [z0[0], z0[1]]
        z1[1] += 2.0 * pi / 2
        self.cmdcenter.cmd('radial_2d("zn", %d, %f, %s, %s)' % (component, time, str(z0), str(z1)))


    @handle_event
    def rotate90(self, component, time=1):
        ''' Rotates a zn by 90 deg '''

        z0 = r_to_p(self.state.zn[component])
        z1 = [z0[0], z0[1]]
        z1[1] += 2.0 * pi / 4
        self.cmdcenter.cmd('radial_2d(zn, %d, %f, %s, %s)' % (component, time, str(z0), str(z1)))


    @handle_event
    def rotate45(self, component, time=1):
        ''' Rotates a zn by 45 deg '''

        z0 = r_to_p(self.state.zn[component])
        z1 = [z0[0], z0[1]]
        z1[1] += 2.0 * pi / 8
        self.cmdcenter.cmd('radial_2d(zn, %d, %f, %s, %s)' % (component, time, str(z0), str(z1)))


    @handle_event
    def rotateLoop(self, component, time=1):
        ''' Rotates a zn continuously '''

        z0 = r_to_p(self.state.zn[component])
        z1 = [z0[0], z0[1]]
        z1[1] += 2.0 * pi
        self.cmdcenter.cmd("Radial2D('zn', %d, %s, {'s' : %s, 'e' : %s, 'loop' : True})" % (component, 32.0 * time, str(z0), str(z1)))


    @handle_event
    def transLoop(self, component, time=1):
        ''' Translates a zn continuously '''

        z0 = r_to_p(self.state.zn[component])
        z1 = [z0[0], z0[1]]
        z1[0] += 2.0
        self.cmdcenter.cmd("Radial2D('zn', %d, %s, {'s' : %s, 'e' : %s, 'loop' : True})" % (component, 8.0 * time, str(z0), str(z1)))


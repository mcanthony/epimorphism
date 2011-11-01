from common.globals import *

from interface.oschandler import *

import interface.OSC

from common.log import *
set_log("OSCHandler")

class DefaultOSCHandler(OSCHandler):
    def mirror_all(self):
        OSCHandler.mirror_all(self)

class DefaultInterferenceOSC(DefaultOSCHandler):    

    # OSC address handers
    def adr_num_waves(self, addr, tags, data, source):
        num = self.state.get_par('_SLICES') + data[0]        
        if(num > 0):
            self.cmdcenter.cmd("state.set_par('_SLICES', %d)" % num)


    def adr_wave_n(self, addr, tags, data, source):
        self.cmdcenter.cmd("state.set_par('_N', %f)" % data[0])

        
    def adr_speed(self, addr, tags, data, source):
        v_new = 0.05 * data[0] + 0.00001
        v_old = self.state.t_speed
        
        # set val
        self.cmdcenter.cmd("state.t_speed = %f" % v_new)
        
        # adjust phase
        self.cmdcenter.cmd("state.t_phase = %f" % (v_old * (self.state.time + self.state.t_phase) / v_new - self.state.time))


    # OSC device feedback
    def mirror(self, obj, key, val):
        if(obj == self.state.par):
            if(key == self.state.par_idx('_SLICES')):
                self._send("/val_num_waves", [str(val)])
            elif(key == self.state.par_idx('_N')):
                 self._send("/val_wave_n", [str("%0.2f" % val)])
                 self._send("/wave_n", [val])


    def mirror_all(self):
        DefaultOSCHandler.mirror_all(self)
        self._send("/speed", [(self.state.t_speed - 0.00001) / 0.05])
        

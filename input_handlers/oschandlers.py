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


    def adr_zn0(self, addr, tags, data, source):
        self.cmdcenter.cmd("state.zn[0] = %f + %fj" % (data[1], data[0]))


    def adr_zn1(self, addr, tags, data, source):
        self.cmdcenter.cmd("state.zn[1] = %f + %fj" % (data[1], data[0]))


    def adr_zn2(self, addr, tags, data, source):
        self.cmdcenter.cmd("state.zn[2] = %f + %fj" % (data[1], data[0]))


    def adr_zn3(self, addr, tags, data, source):
        self.cmdcenter.cmd("state.zn[3] = %f + %fj" % (data[1], data[0]))

        
    def adr_T(self, addr, tags, data, source):
        if data[0] == 0:
            return
        elif data[0] == 100:
            v = 0
        else:
            v = data[0]

        self.cmdcenter.cmd("inc_data('T', %d)" % v)


    # OSC device feedback
    def mirror(self, obj, key, val):
        if(obj == self.state.par):
            if(key == self.state.par_idx('_SLICES')):
                self._send("/val_num_waves", [str(val)])
            elif(key == self.state.par_idx('_N')):
                 self._send("/val_wave_n", [str("%0.2f" % val)])
                 self._send("/wave_n", [val])
        elif(obj == self.state.zn):
            self._send("/zn%d" % key, [val.imag, val.real])
            self._send("/val_zn%d" % key, ["%f+%fi" % (val.imag, val.real)])


    def mirror_all(self):
        DefaultOSCHandler.mirror_all(self)
        self._send("/speed", [(self.state.t_speed - 0.00001) / 0.05])
        

from common.globals import *

from common.complex import *

from interface.oschandler import *

import OSC, re

from common.log import *
set_log("OSCHandler")

class DefaultOSCHandler(OSCHandler):
    def __init__(self):
        self.regex_callbacks = {"/val_zn(\d+)": self.val_zn,
                                "/val_r_zn(\d+)": self.val_r_zn,
                                "/val_th_zn(\d+)": self.val_th_zn,
                                "/val_par_(\w+)": self.val_par,
                                "/inc_par_(\w+)": self.inc_par,
                                "/inc_cmp_(\w+)": self.inc_cmp,
                                "/cmd_(\w+)": self.cmd}
                                
        OSCHandler.__init__(self)


    def val_zn(self, addr, tags, data, source):
        idx = int(re.search("(\d+)$", addr).groups()[0])
        #self.cmdcenter.cmd("state.zn[%d] = %f + %fj" % (idx, data[1], data[0]))        

        old = self.state.zn[idx]
        val = complex(data[1], data[0])
        self.cmdcenter.radial_2d('state.zn', idx, self.app.midi_speed, r_to_p(old), r_to_p(val))


    def val_r_zn(self, addr, tags, data, source):
        idx = int(re.search("(\d+)$", addr).groups()[0])
        old = self.state.zn[idx]        
        val = p_to_r([data[0], r_to_p(old)[1]])
        self.cmdcenter.cmd("state.zn[%d] = %f + %fj" % (idx, val.real, val.imag))        
#        val = (data[0], r_to_p(old)[1])
#        self.cmdcenter.radial_2d('state.zn', idx, self.app.midi_speed / 8, r_to_p(old), val)


    def val_th_zn(self, addr, tags, data, source):
        idx = int(re.search("(\d+)$", addr).groups()[0])
        old = self.state.zn[idx]
        val = p_to_r([r_to_p(old)[0], data[0]])
        self.cmdcenter.cmd("state.zn[%d] = %f + %fj" % (idx, val.real, val.imag))        
#        val = (r_to_p(old)[0], data[0])
#        self.cmdcenter.radial_2d('state.zn', idx, self.app.midi_speed / 8, r_to_p(old), val)


    def val_par(self, addr, tags, data, source):
        name=addr[9:]
        self.cmdcenter.cmd("state.set_par('%s', %f)" % ('_' + name, data[0]))


    def inc_par(self, addr, tags, data, source):
        name=addr[9:]
        self.cmdcenter.cmd("state.set_par('%s', %f)" % ('_' + name, self.state.get_par('_' + name) + data[0]))

        
    def inc_cmp(self, addr, tags, data, source):
        name=addr[9:]
        if(data[0] in {-1, 0, 1}):
            self.cmdcenter.cmd("inc_data('%s', %d)" % (name, data[0]))        


    def cmd(self, addr, tags, data, source):
        cmd=addr[5:]
        print cmd
        self.cmdcenter.cmd("%s()" % cmd)        


    # OSC address handers        
    def hnd_var_speed(self, addr, tags, data, source):
        v_new = 0.05 * data[0] + 0.00001
        v_old = self.state.t_speed
        
        # set val
        self.cmdcenter.cmd("state.t_speed = %f" % v_new)
        
        # adjust phase
        self.cmdcenter.cmd("state.t_phase = %f" % (v_old * (self.cmdcenter.abs_time() + self.state.t_phase) / v_new - self.cmdcenter.abs_time()))


    # OSC device feedback
    def mirror(self, obj, key, val):
        if(obj == self.state.par):
            self._send("/val_par_%s" % self.state.par_names[key][1:], [str(val)])
            self._send("/txt_par_%s" % self.state.par_names[key][1:], ["%0.2f" % val])
        elif(obj == self.state.zn):
            self._send("/val_zn%d" % key, [val.imag, val.real])
            self._send("/txt_zn%d" % key, ["%f+%fi" % (val.imag, val.real)])
            val = r_to_p(val)
            self._send("/val_r_zn%d" % key, [val[0]])
            self._send("/txt_r_zn%d" % key, ["%0.2f" % val[0]])
            self._send("/val_th_zn%d" % key, [val[1]])
            self._send("/txt_th_zn%d" % key, ["%0.2f" % val[1]])
        elif(obj == self.state.components):
            if(re.match("intrp", val)):
                val = "SWITCHING"
            self._send("/txt_cmp_%s" % key, [val])


    def mirror_all(self):
        self._send("/val_speed", [(self.state.t_speed - 0.00001) / 0.05])
        self._send("/txt_speed", [str((self.state.t_speed - 0.00001) / 0.05)])

        OSCHandler.mirror_all(self)


class DefaultInterferenceOSC(DefaultOSCHandler):    

    def __init__(self):
        DefaultOSCHandler.__init__(self)


class DefaultEpimorphismOSC(DefaultOSCHandler):    

    def __init__(self):
        DefaultOSCHandler.__init__(self)

        

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
                                "/set_r_zn(\d+)": self.val_r_zn,
                                "/set_th_zn(\d+)": self.val_th_zn,
                                "/qnt_th_zn(\d+)": self.qnt_th_zn,
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
        self.cmdcenter.radial_2d('zn', idx, self.app.midi_speed, r_to_p(old), r_to_p(val))


    def val_r_zn(self, addr, tags, data, source):
        if(data[0] == -1000):
            return
        idx = int(re.search("(\d+)$", addr).groups()[0])
        old = self.state.zn[idx]        
        val = (data[0], r_to_p(old)[1])
        self.cmdcenter.radial_2d('zn', idx, self.app.midi_speed / 8, r_to_p(old), val)


    def val_th_zn(self, addr, tags, data, source):
        if(data[0] == -1000):
            return
        idx = int(re.search("(\d+)$", addr).groups()[0])
        old = self.state.zn[idx]
        val = (r_to_p(old)[0], data[0] / 360.0 * 2 * 3.14159)
        self.cmdcenter.radial_2d('zn', idx, self.app.midi_speed / 8, r_to_p(old), val)


    def qnt_th_zn(self, addr, tags, data, source):
        if(data[0] == -1000):
            return
        idx = int(re.search("(\d+)$", addr).groups()[0])
        old = self.state.zn[idx]
        pi4 = 3.14159 / 4
        th = pi4 * ((int)(r_to_p(old)[1] / pi4 + 0.0001))
        th += data[0] * pi4;
        val = (r_to_p(old)[0], th)
        self.cmdcenter.radial_2d('zn', idx, self.app.midi_speed / 8, r_to_p(old), val)


    def val_par(self, addr, tags, data, source):
        name=addr[9:]
        self.cmdcenter.cmd("state.par['%s'] = %f" % ('_' + name, data[0]))


    def inc_par(self, addr, tags, data, source):
        name=addr[9:]
        self.cmdcenter.cmd("state.par['%s'] = %f" % ('_' + name, self.state.par['_' + name] + data[0]))

        
    def inc_cmp(self, addr, tags, data, source):
        name=addr[9:]
        if(data[0] in {-1, 0, 1}):
            self.cmdcenter.cmd("inc_data('%s', %d)" % (name, data[0]))        


    def cmd(self, addr, tags, data, source):
        if(data[0] != 1):
            return
        cmd=addr[5:]
        self.cmdcenter.cmd("%s()" % cmd)        


    # OSC address handers        
    def hnd_val_speed(self, addr, tags, data, source):
        v_new = data[0] + 0.00001
        v_old = self.state.t_speed
        
        # set val
        self.cmdcenter.cmd("state.t_speed = %f" % v_new)
        
        # adjust phase
        self.cmdcenter.cmd("state.t_phase = %f" % (v_old * (self.cmdcenter.abs_time() + self.state.t_phase) / v_new - self.cmdcenter.abs_time()))


    # OSC device feedback
    def mirror(self, obj, key, val, bundle=False):
        if(obj == self.state.par):
            self._send("/val_par%s" % key, [str(val)], True)
            self._send("/txt_par%s" % key, ["%0.2f" % val], bundle)
        elif(obj == self.state.zn):
            self._send("/val_zn%d" % key, [val.imag, val.real], True)
            self._send("/txt_zn%d" % key, ["%f+%fi" % (val.imag, val.real)], bundle)
            val = r_to_p(val)
            self._send("/val_r_zn%d" % key, [val[0]], True)
            self._send("/txt_r_zn%d" % key, ["%0.2f" % val[0]], True)
            th = (val[1] + 0.0001) / (2 * 3.14159) * 360
            self._send("/val_th_zn%d" % key, [str(th)], True)
            self._send("/txt_th_zn%d" % key, [str(int(th))], bundle)
        elif(obj == self.state.components):
            if(re.match("intrp", val)):
                val = "SWITCHING"
            self._send("/txt_cmp_%s" % key, [val], bundle)
        elif(obj == self.state):
            if(key == "t_speed"):
                print self.state.t_speed
                self._send("/val_speed", [str(self.state.t_speed)], True)
                self._send("/txt_speed", ["%0.2f" % self.state.t_speed], bundle)


    def mirror_all(self):
        for k,v in self.state.par.items():
            self.mirror(self.state.par, k, v, True)
        for i in xrange(len(self.state.zn)):
            self.mirror(self.state.zn, i, self.state.zn[i], True)
        for k,v in self.state.components.items():
            self.mirror(self.state.components, k, v, True)
        self._send("/val_speed", [self.state.t_speed], True)
        self._send("/txt_speed", ["%0.2f" % self.state.t_speed])


class DefaultInterferenceOSC(DefaultOSCHandler):    

    def __init__(self):
        DefaultOSCHandler.__init__(self)


class DefaultEpimorphismOSC(DefaultOSCHandler):    

    def __init__(self):
        DefaultOSCHandler.__init__(self)

# define helpers
def get_val(x):       return x
def set_val(x, y):    return y
def get_radius(z):    return r_to_p(z)[0]
def set_radius(z, r): return p_to_r([r, r_to_p(z)[1]])
def get_th(z):        return r_to_p(z)[1]
def set_th(z, th):    return p_to_r([r_to_p(z)[0], th])
        
class EpimorphismRD1OSC(OSCHandler):
    def __init__(self):
        self.regex_callbacks = {"/midinote": self.midinote, "/midictrl": self.midictrl}
                                
        OSCHandler.__init__(self)


    def midinote(self, addr, tags, data, source):
        note = data[0]
        if(note == 0):
            pass
        elif(note == 1):
            pass        
        print "note", note

        
    def midictrl(self, addr, tags, data, source):
        param = data[1]
        val = data[0]
        
#        print "ctrl", param, val

        bindings = {1: ["state.zn",  '0',  "radius", (1.0, 1.0)],
                    2: ["state.zn",  '2',  "radius", (1.0, 1.0)],
                    3: ["state.zn",  '8',  "radius", (1.0, 1.0)],
                    4: ["state.zn",  '9',  "radius", (1.0, 0.0)],
                    5: ["state.zn",  '10', "radius", (1.0, 1.0)],
                    6: ["state.zn",  '11', "radius", (1.0, 0.0)]
                    }

        # catch error
        if(not bindings.has_key(int(param))):
            print "no osc binding for channel ", param
        binding = bindings[int(param)]

        f = val / 128.0
        if(val == 127.0) : f = 1.0

        f = binding[3][0] * f + binding[3][1]

        old = self.cmdcenter.get_val(binding[0], eval(binding[1]))
        val = eval("set_" + binding[2])(old, f)
        #print old, val, str(binding[1])
        # HACK to smoothen values
        
        if(binding[2] == "radius" or binding[2] == "th"):
            self.cmdcenter.radial_2d('zn', eval(binding[1]), self.cmdcenter.interface.app.midi_speed, r_to_p(old), r_to_p(val))
        else:
            self.cmdcenter.linear_1d('par', eval(binding[1]), self.cmdcenter.interface.app.midi_speed, old, val)


        

from common.globals import *

from common.complex import *

from interface.oschandler import *

import OSC, re, time, os, copy

import random

from common.log import *
set_log("OSCHandler")

SPD = 0.54

class DefaultOSCHandler(OSCHandler):
    def __init__(self):
        self.regex_callbacks = {"/val_zn(\d+)$": self.val_zn,
                                "/val_r_zn(\d+)$": self.val_r_zn,
                                "/val_th_zn(\d+)$": self.val_th_zn,
                                "/qnt_th_zn(\d+)$": self.qnt_th_zn,
                                "/qnt_th_d_zn(\d+)$": self.qnt_th_d_zn,
                                "/set_r_zn(\d+)$": self.val_r_zn,
                                "/set_th_zn(\d+)$": self.val_th_zn,
                                "/set_re_zn(\d+)$": self.val_re_zn,
                                "/set_im_zn(\d+)$": self.val_im_zn,
                                "/tex_send": self.tex_send,
                                "/change_state": self.change_state,
                                "/inc_tex_folder_(\d+)$": self.inc_tex_folder,
                                "/inc_tex_name_(\d+)$": self.inc_tex_name,
                                "/val_par_(\w+)_(\d+)$": self.val_par,
                                "/inc_par_(\w+)_(\d+)$": self.inc_par,
                                "/inc_cmp_([a-zA-Z_]+)": self.inc_cmp,
                                "/cmp_send": self.cmp_send,
                                "/cmd_(\w+)": self.cmd}


        self.idx = -1

        OSCHandler.__init__(self)

    def val_zn(self, addr, tags, data, source):
        self.log_event()
        idx = int(re.search("(\d+)$", addr).groups()[0])
        #self.cmdcenter.cmd("state.zn[%d] = %f + %fj" % (idx, data[1], data[0]))

        old = self.state.zn[idx]
        val = complex(data[1], data[0])
        self.cmdcenter.radial_2d('zn', idx, self.app.midi_speed, r_to_p(old), r_to_p(val))
        #self.cmdcenter.state.zn[idx] = val

    def val_re_zn(self, addr, tags, data, source):
        self.log_event()
        if(data[0] == -1000):
            return
        idx = int(re.search("(\d+)$", addr).groups()[0])
        #self.cmdcenter.cmd("state.zn[%d] = %f + %fj" % (idx, data[1], data[0]))

        old = self.state.zn[idx]
        val = complex(data[0], old.imag)
        self.cmdcenter.radial_2d('zn', idx, self.app.midi_speed, r_to_p(old), r_to_p(val))
        #self.cmdcenter.state.zn[idx] = val

    def val_im_zn(self, addr, tags, data, source):
        self.log_event()
        if(data[0] == -1000):
            return
        idx = int(re.search("(\d+)$", addr).groups()[0])
        #self.cmdcenter.cmd("state.zn[%d] = %f + %fj" % (idx, data[1], data[0]))

        old = self.state.zn[idx]
        val = complex(old.real, data[0])
        self.cmdcenter.radial_2d('zn', idx, self.app.midi_speed, r_to_p(old), r_to_p(val))
        #self.cmdcenter.state.zn[idx] = val

    def val_r_zn(self, addr, tags, data, source):
        self.log_event()
        if(data[0] == -1000):
            return
        idx = int(re.search("(\d+)$", addr).groups()[0])
        old = self.state.zn[idx]
        val = (data[0], r_to_p(old)[1])
        self.cmdcenter.radial_2d('zn', idx, self.app.midi_speed / 8, r_to_p(old), val)
#        self.cmdcenter.cmd("set_state_val('zn', %d, %s)" % (idx, str(p_to_r(val))))
        #self.cmdcenter.state.zn[idx] = p_to_r(val)


    def val_th_zn(self, addr, tags, data, source):
        self.log_event()
        if(data[0] == -1000):
            return
        idx = int(re.search("(\d+)$", addr).groups()[0])
        old = self.state.zn[idx]
        val = (r_to_p(old)[0], data[0] / 360.0 * 2 * 3.14159)
        self.cmdcenter.radial_2d('zn', idx, self.app.midi_speed / 8, r_to_p(old), val)
        #self.cmdcenter.state.zn[idx] = p_to_r(val)


    def qnt_th_zn(self, addr, tags, data, source):
        self.log_event()
        if(data[0] == -1000):
            return
        idx = int(re.search("(\d+)$", addr).groups()[0])
        old = self.state.zn[idx]
        pi4 = 3.14159 / 2
        th = pi4 * ((int)(r_to_p(old)[1] / pi4 + 0.0001))
        th += data[0] * pi4
        val = (r_to_p(old)[0], th)
        spd = SPD
        self.cmdcenter.cmd("radial_2d('zn', %s, %s, %s, %s)" % (idx, spd, r_to_p(old), val))
        #self.cmdcenter.state.zn[idx] = p_to_r(val)


    def qnt_th_d_zn(self, addr, tags, data, source):
        self.log_event()
        if(data[0] == -1000):
            return
        idx = int(re.search("(\d+)$", addr).groups()[0])
        old = self.state.zn[idx]
        pi4 = 3.14159 / 2
        th = pi4 * ((int)(r_to_p(old)[1] / pi4 + 0.0001))
        th += data[0] * pi4;
        val = (r_to_p(old)[0], th)
        spd = SPD * 2
        self.cmdcenter.cmd("radial_2d('zn', %s, %s, %s, %s)" % (idx, spd, r_to_p(old), val))
        #self.cmdcenter.state.zn[idx] = p_to_r(val)


    def inc_tex_folder(self, addr, tags, data, source):
        self.log_event()
        if(data[0] == -1000):
            return
        idx = int(re.search("(\d+)$", addr).groups()[0])
        cur = self.current_texture_folders[idx]
        cur_idx = [t['folder'] for t in self.texture_names].index(cur)
        cur_idx = (cur_idx + int(data[0])) % len(self.texture_names)
        new = self.texture_names[cur_idx]['folder']
        self.current_texture_folders[idx] = new
        self._send("/txt_tex_folder_%d" % idx, [new])

        new = self.texture_names[cur_idx]['textures'][0]
        self.current_texture_names[idx] = new
        self._send("/txt_tex_name_%d" % idx, [new])

    def inc_tex_name(self, addr, tags, data, source):
        self.log_event()
        if(data[0] == -1000):
            return
        idx = int(re.search("(\d+)$", addr).groups()[0])
        cur_folder = self.current_texture_folders[idx]
        cur_texture = self.current_texture_names[idx]
        textures = [t['textures'] for t in self.texture_names if t['folder'] == cur_folder][0]
        cur_idx = (textures.index(cur_texture) + int(data[0])) % len(textures)

        new = textures[cur_idx]
        self.current_texture_names[idx] = new
        self._send("/txt_tex_name_%d" % idx, [new])


    def tex_send(self, addr, tags, data, source):
        self.log_event()
        if(data[0] == -1000):
            return
        for i in xrange(self.state.par_dim):
            name = self.current_texture_folders[i] + '/' + self.current_texture_names[i] + ".png"
            self.cmdcenter.switch_aux(i, name, self.app.state_intrp_time / 2.0)


    def val_par(self, addr, tags, data, source):
        self.log_event()
        idx = re.search("(\d+)$", addr).groups()[0]
        idx_idx = addr.index(idx)
        name=addr[9:idx_idx-1]
#        self.cmdcenter.cmd("state.par['_%s'][%s] = %f" % (name, idx, data[0]))
        new_par = self.cmdcenter.state.par['_' + name]
        new_par[int(idx)] = data[0]
        self.cmdcenter.state.par['_' + name] = new_par


    def inc_par(self, addr, tags, data, source):
        self.log_event()
        idx = re.search("(\d+)$", addr).groups()[0]
        idx_idx = addr.index(idx)
        name=addr[9:idx_idx-1]
        #self.cmdcenter.cmd("state.par['_%s'][%s] = %f" % (name, idx, self.state.par['_' + name] + data[0]))
        new_par = self.cmdcenter.state.par['_' + name]
        new_par[int(idx)] = data[0]
        self.cmdcenter.state.par['_' + name] = new_par


    def inc_cmp(self, addr, tags, data, source):
        self.log_event()
        if(data[0] == -1000):
            return
        name=addr[9:]
#        if(data[0] in {-1, 0, 1}):
#            self.cmdcenter.cmd("inc_data('%s', %d)" % (name, data[0]))
        cur = self.current_components[name]
        parent_name = re.sub("(\d)+$", "", name)

        components = self.cmdcenter.componentmanager.datamanager.components[parent_name]
        cur_idx = [c[0] for c in components].index(cur)
        cur_idx = (cur_idx + int(data[0])) % len(components)
        new_component = components[cur_idx][0]

        self.updated_components[name] = new_component
        self.current_components[name] = new_component
        if parent_name in self.cmdcenter.componentmanager.datamanager.component_suffixes:
            suffix = self.cmdcenter.componentmanager.datamanager.component_suffixes[parent_name]
        else:
            suffix = ""
        self._send("/txt_cmp_%s" % name, [new_component.replace(suffix, '')])


    def cmp_send(self, addr, tags, data, source):
        self.log_event()
        self.cmdcenter.componentmanager.switch_components(self.updated_components)
        self.updated_components = {}


    def change_state(self, addr, tags, data, source):
        if(data[0] == -1000):
            return
        #i = random.randint(0, 4)
        self.idx = (self.idx + 1) % 5
        i = self.idx
        #print i
        par = {}
        if(i == 0):
            updated_components = {
                'SEED': 'seed_multi(0, frame, z, fb, aux, par, internal, zn, time)',
                'SEED0': 'seed_multi_wca(idx, frame, z, fb, aux, par, internal, zn, time)',
                'SEED_W0': 'lines_box(idx, z, par)',
                'SEED_WT0': 'wt_id(idx, w)',
                'SEED_C0': 'tex_color(idx, fb, aux, z, seed, par, time)',
                'SEED_A0': 'solid_alpha(idx, w, res, par)',
                'SEED1': 'seed_multi_wca(idx, frame, z, fb, aux, par, internal, zn, time)',
                'SEED_W1': 'nothing(idx, z, par)',
                'SEED_WT1': 'wt_id(idx, w)',
                'SEED_C1': 'tex_color(idx, fb, aux, z, seed, par, time)',
                'SEED_A1': 'solid_alpha(idx, w, res, par)',
                'SEED2': 'seed_multi_wca(idx, frame, z, fb, aux, par, internal, zn, time)',
                'SEED_W2': 'nothing(idx, z, par)',
                'SEED_WT2': 'wt_id(idx, w)',
                'SEED_C2': 'tex_color(idx, fb, aux, z, seed, par, time)',
                'SEED_A2': 'solid_alpha(idx, w, res, par)',
                'T': 'sinhz(z)',
                'T_SEED': 'sinhz(z)',
                'T_SEED0': 'z',
                'T_SEED1': 'z',
                'T_SEED2': 'z',
                'COLOR': 'rotate_hsls(v, z_z, par, time)',
                'REDUCE': 'torus_reduce(z)',
                'RESET': 'reset_hsls(x, y, par)',
                'POST': 'post_gamma(v, par, time)'
            }

            aux = ['simplegeom/tile_rainbow1.png', 'simplegeom/tile_rainbow1.png', 'simplegeom/tile_rainbow1.png']

        elif(i == 1):
            aux = ['psych/psych_7.png', 'simplegeom/tile_grid3.png', 'simplegeom/tile_grid1.png']
            updated_components = {
                'T': '0.5f * (z + sinhz(z))',
                'T_SEED': 'cosz(z) - sinhz(z)',
                'SEED_C0': 'tex_color(idx, fb, aux, z, seed, par, time)',
                'SEED_C1': 'tex_color(idx, fb, aux, z, seed, par, time)',
                'SEED_C2': 'tex_color(idx, fb, aux, z, seed, par, time)',
                'POST': 'post_gamma(v, par, time)',
                'COLOR': 'rotate_hsls(v, z_z, par, time)',
                'T_SEED2': 'z',
                'T_SEED1': 'cosz(z)',
                'T_SEED0': 'expz(z)',
                'SEED_W0': 'lines_box(idx, z,par)',
                'SEED_W1': 'lines_lr(idx,z, par)',
                'SEED_W2': 'nothing(idx, z, par)'
            }

        elif(i == 2):
            aux = ['simplegeom/tile_rainbow1.png','misc/tile_vector1.png','simplegeom/tile_grid1.png']
            updated_components = {
                'T_SEED': 'cosz(z) - sinhz(z)',
                'SEED_C0': 'tex_color(idx, fb, aux, z, seed, par, time)',
                'SEED_C1': 'tex_color(idx, fb, aux, z, seed, par, time)',
                'SEED_C2': 'tex_color(idx, fb, aux, z, seed, par, time)',
                'T': 'sinhz(z)',
                'POST': 'post_gamma(v, par, time)',
                'COLOR': 'rotate_hsls(v, z_z, par, time)',
                'T_SEED2': 'z',
                'T_SEED1': 'cosz(z)',
                'T_SEED0': 'expz(z)',
                'SEED_W0': 'lines_box(idx, z, par)',
                'SEED_W1': 'lines_lr(idx, z, par)',
                'SEED_W2': 'nothing(idx, z, par)'
            }
        elif(i == 3):
            aux = ['simplegeom/tile_grid3.png', 'misc/tile_vector2.png', 'flowers/flowers7.png']
            updated_components = {
                'T_SEED': '0.5f * (z + sqz(z))',
                'SEED_C0': 'tex_color(idx, fb, aux, z, seed, par, time)',
                'SEED_C1': 'tex_color(idx, fb, aux, z, seed, par, time)',
                'SEED_C2': 'tex_color(idx, fb, aux, z, seed, par, time)',
                'T': '0.5f * (sinz(z) + tanz(z))',
                'POST': 'post_gamma(v, par, time)',
                'COLOR': 'rotate_hsv(v, z_z, par, time)',
                'T_SEED2': 'z',
                'T_SEED1': 'sinh(z)',
                'T_SEED0': 'z',
                'SEED_W0': 'lines_box(idx, z, par)',
                'SEED_W1': 'lines_inner(idx, z, par)',
                'SEED_W2': 'lines_box_stag(idx, z, par)'
            }
        elif(i == 4):
            aux = ['simplegeom/tile_rainbow2.png', 'simplegeom/tile_grid2.png', 'psych/psych_7.png']
            updated_components = {
                'T': '0.5f * (z + expz(z))',
                'T_SEED': '0.5f * (sinz(z) + cosz(z) )',
                'SEED_C0': 'tex_color(idx, fb, aux, z, seed, par, time)',
                'SEED_C1': 'tex_color(idx, fb, aux, z, seed, par, time)',
                'SEED_C2': 'tex_color(idx, fb, aux, z, seed, par, time)',
                'POST': 'post_gamma(v, par, time)',
                'COLOR': 'bgr_id(v, z_z, par, time)',
                'T_SEED2': 'cosz(z)',
                'T_SEED1': 'sinh(z)',
                'T_SEED0': 'sinh(z)',
                'SEED_W0': 'lines_box(idx, z, par)',
                'SEED_W1': 'lines_inner(idx, z, par)',
                'SEED_W2': 'lines_box_stag(idx, z, par)'
            }

        elif(i == 5):
            aux = []
            updated_components = {

            }

        time = SPD

        self.cmdcenter.cmd("app.state_intrp_time = %s" % time)
        self.cmdcenter.cmd("switch_components_all(%s, %s, '%s', '%s', '%s')" % (updated_components, par, aux[0], aux[1], aux[2]))

    def cmd(self, addr, tags, data, source):
        self.log_event()
        if(data[0] != 1):
            return
        cmd=addr[5:]
        self.cmdcenter.cmd("%s()" % cmd)


    def log_event(self):
        self.cmdcenter.programInterrupt()


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
            for i in range(len(val)):
                self._send("/val_par%s_%d" % (key, i), [str(val[i])], bundle)
                self._send("/txt_par%s_%d" % (key, i), ["%0.2f" % val[i]], bundle)
        elif(obj == self.state.zn):
            self._send("/val_zn%d" % key, [val.imag, val.real], bundle)
            self._send("/txt_zn%d" % key, ["%0.2f + %0.2fi" % (val.imag, val.real)], bundle)
            val = r_to_p(val)
            self._send("/val_r_zn%d" % key, [val[0]], bundle)
            self._send("/txt_r_zn%d" % key, ["%0.2f" % val[0]], bundle)
            th = (val[1] + 0.0001) / (2 * 3.14159) * 360
            self._send("/val_th_zn%d" % key, [str(th)], bundle)
            self._send("/txt_th_zn%d" % key, [str(int(th))], bundle)
        elif(obj == self.state.components):
            if(re.match("intrp", val)):
                val = "SWITCHING"
                suffix = ""
            else:
                parent_key = re.sub("(\d)+", "", key)
                if parent_key in self.cmdcenter.componentmanager.datamanager.component_suffixes:
                    suffix = self.cmdcenter.componentmanager.datamanager.component_suffixes[parent_key]
                else:
                    suffix = ""
            self._send("/txt_cmp_%s" % key, [val.replace(suffix, '')], bundle)
        elif(obj == self.state.aux):
            key /= 2
            name = self.cmdcenter.get_aux_name(key)
            if not name or name != val:
                return
            self._send("/txt_tex_folder_%d" % key, [name.split('/')[0]], bundle)
            self._send("/txt_tex_name_%d" % key, [name.split('/')[1].replace('.png', '')], bundle)
        elif(obj == self.state):
            if(key == "t_speed"):
                self._send("/val_speed", [str(self.state.t_speed)], bundle)
                self._send("/txt_speed", ["%0.2f" % self.state.t_speed], bundle)\
#        elif(obj == self.state):


    def mirror_all(self):
        for i in xrange(len(self.state.zn)):
            time.sleep(0.01)
            self.mirror(self.state.zn, i, self.state.zn[i], False)
        for k,v in self.state.par.items():
            time.sleep(0.01)
            self.mirror(self.state.par, k, v, False)
        for k,v in self.state.components.items():
            time.sleep(0.01)
            self.mirror(self.state.components, k, v, False)
        for i in xrange(self.state.par_dim):
            time.sleep(0.01)
            self.mirror(self.state.aux, i, self.state.aux[i], False)
        time.sleep(0.01)
        self._send("/val_speed", [self.state.t_speed], False)
        time.sleep(0.01)
        self._send("/txt_speed", ["%0.2f" % self.state.t_speed], False)


class DefaultInterferenceOSC(DefaultOSCHandler):

    def __init__(self):
        DefaultOSCHandler.__init__(self)


class DefaultEpimorphismOSC(DefaultOSCHandler):

    def __init__(self):
        DefaultOSCHandler.__init__(self)
        self.updated_components = {}
        path = "media/textures/"
        folders = [f for f in os.listdir(path) if not os.path.isfile(path + f)]
        for i in xrange(len(folders)):
            textures = [f.replace('.png','') for f in os.listdir(path + folders[i]) if os.path.isfile(path + folders[i] + "/" + f)]
            textures.sort()
            folders[i] = {'folder': folders[i], 'textures': textures}
        self.texture_names = folders

        self.current_texture_folders = []
        self.current_texture_names = []
        for i in xrange(self.state.par_dim):
            name = self.cmdcenter.get_aux_name(i)
            self.current_texture_folders.append(name.split('/')[0])
            self.current_texture_names.append(name.split('/')[1].replace('.png', ''))

        self.current_components = copy.copy(self.state.components)



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

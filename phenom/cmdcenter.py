from phenom.animator import *
from phenom.console import *
from phenom.keyboard import *
from phenom.mouse import *
from phenom.server import *
from phenom.midi import *
from phenom.video import *
from phenom.setter import *
from phenom.interpolator import *

from phenom.BM2009 import *

from phenom.datamanager import *

from common.default import *
from common.complex import *
from noumena.compiler import *

from config.configmanager import *

import StringIO
import sys

import Image


class CmdEnv(dict):
    ''' The CmdEnv object is a subclass of dict used as the execution
        environment for the CmdCenter.cmd method '''

    def __init__(self, data, funcs):

        self.data, self.funcs = data, funcs


    def __getitem__(self, key):

        # first check data
        for d in self.data:
            if d.has_key(key):
                return d[key]

        # if not found, return func
        return self.funcs[key]


    def __setitem__(self, key, value):

        # set data
        for d in self.data:
            if d.has_key(key):
                d[key] = value


class CmdCenter(Setter, Animator):
    ''' The CmdCenter is the central control center for the engine and
        renderer.  All systems generating signals live here, and the object
        provides an interface for executing code int the appropriate environment. '''


    def __init__(self, state, renderer, engine, context):

        self.state, self.renderer, self.engine, self.context = state, renderer, engine, context

        # start datamanager
        self.datamanager = DataManager()

        # start BM2009 code
        self.bm2009 = BM2009(self)

        # init interpolator
        self.interpolator = Interpolator(self, self.state, self.renderer, self.engine, self.context)

        # init animator
        Animator.__init__(self)

        # create video_renderer
        self.video_renderer = VideoRenderer(self)

        # create input handlers
        mouse_handler = MouseHandler(self, renderer.profile)
        keyboard_handler = KeyboardHandler(self)

        # create_console
        console = Console(self)

        # register callbacks with Renderer
        self.renderer.register_callbacks(keyboard_handler.keyboard, mouse_handler.mouse, mouse_handler.motion,
                                         console.render_console, console.console_keyboard)

        # start server
        if(self.context.server):

            self.server = Server(self)
            self.server.start()

        else:

            self.server = None

        # start midi
        if(self.context.midi):

            self.midi = MidiHandler(self)

            if(self.context.midi):

                self.state.zn.midi = self.midi
                self.state.par.midi = self.midi
                self.midi.start()

        else:

            self.midi = None

        # start video_renderer
        if(self.context.render_video):

            self.video_renderer.video_start()

        # create cmd_env function blacklist
        func_blacklist = ['do', '__del__', '__init__', 'kernel', 'print_timings', 'record_event', 'start', 'switch_kernel',
                          'keyboard', 'console_keyboard', 'register_callbacks', 'render_console', 'capture', 'render_fps',
                          'video_time', 'set_inner_loop', 'time', 'cmd', 'execute_paths', 'echo', 'reshape',
                          'set_component_indices'] + dir(object) + dir(Setter)

        # extract non-blacklist functions from an object
        def get_funcs(obj):
            return dict([(attr, getattr(obj, attr)) for attr in dir(obj) if callable(getattr(obj, attr)) and attr not in func_blacklist])

        # get functions from objects
        funcs = get_funcs(self)
        funcs.update(get_funcs(self.renderer))
        funcs.update(get_funcs(self.video_renderer))
        funcs.update(get_funcs(self.engine))
        funcs.update(default_funcs)

        # generate cmd exec environment
        self.env = CmdEnv([self.state.__dict__, self.context.__dict__], funcs)

        # init indices for components
        self.set_component_indices()

        self.frame_cnt = 0


        self.last_update_time = time.clock()


    def __del__(self):
        pass

        # kill server
        #if(self.server):
        #    self.server.__del___()


    def cmd(self, code, capture=False):

        # hijack stdout, if requested
        out = StringIO.StringIO()
        sys.stdout = capture and out or sys.stdout

        err = ""

        # execute code
        if(capture):
            try:
                exec(code) in self.env
            except:
                err = traceback.format_exc().split("\n")[-2]
        else:
            exec(code) in self.env


        # restore stdout
        sys.stdout = sys.__stdout__

        # get result
        res = [out.getvalue(), err]

        # close StringIO
        out.close()

        # return result
        return res


    def do(self):

#        if(self.frame_cnt == 10):
#            self.test_bm2009()


        # bm2009 manual automation
        if(time.clock() - self.last_update_time > 5):
            self.last_update_time = time.clock()
            print "manual bm2009 command"
            self.moduleCmd('bm2009', 'impulse', {'intensity':1.0, 'freq':0.2})

        # execute animation paths
        self.execute_paths()

        # capture video frames
        if(self.context.render_video):
            self.video_renderer.capture()


        self.frame_cnt += 1

    def set_component_indices(self):
        self.state.component_idx = [0 for i in xrange(20)]

        component_vals = [[items[0] for items in getattr(self.datamanager, component)] for component in self.datamanager.components]

        for component_name in self.datamanager.components:
            idx = self.datamanager.components.index(component_name)
            val =  getattr(self.state, component_name.upper())

            if(component_name == "T"):
                val = val.replace("(zn[2] * z + zn[3])", "(z)").replace("zn[0] * ", "").replace(" + zn[1]", "")
            elif(component_name == "T_SEED"):
                val = val.replace("(zn[10] * z + zn[11])", "(z)").replace("zn[8] * ", "").replace(" + zn[9]", "")

            print component_name, ":", val

            self.state.component_idx[2 * idx] = component_vals[idx].index(val)


    def inc_data(self, component_name, idx):

        # get components
        components = getattr(self.datamanager, component_name)

        # get and update index
        idx_idx = self.datamanager.components.index(component_name)

        val_idx = self.state.component_idx[2 * idx_idx]
        val_idx += idx
        val_idx %= len(components)

        # switch to component
        if(not self.context.splice_components):

            self.state.component_idx[2 * idx_idx] = val_idx

            # get component
            component = components[self.state.component_idx[2 * idx_idx]]

            # initialize component
            for line in component[1]:
                exec(line) in self.env

            self.blend_to_component(component_name, component[0])
        else:
            self.interpolator.interpolate_splice(idx_idx, val_idx, self.set_component_indices)


    def test_bm2009(self):
        self.moduleCmd('bm2009', 'set_var', {'var':'volume', 'val':1.0})
        self.moduleCmd('bm2009', 'set_var', {'var':'tempo', 'val':100})
        self.moduleCmd('bm2009', 'impulse', {'intensity':1.0, 'freq':0.2})
        #self.bm2009.impulse(1.0, 0.2)


    def moduleCmd(self, module, cmd, vars):
        cmd = "self.%s.%s(**%s)" % (module, cmd, vars)
        print "cmd string", cmd
        exec(cmd)


    def t(self, val):
        self.blend_to_component("T", val)


    def blend_to_component(self, data, val):

        idx_idx = self.datamanager.components.index(data)

        # cheat if t or t_seed
        if(data == "T"):
            val = "zn[0] * (%s) + zn[1]" % val.replace("(z)", "(zn[2] * z + zn[3])")
        elif(data == "T_SEED"):
            val = "zn[8] * (%s) + zn[9]" % val.replace("(z)", "(zn[10] * z + zn[11])")

        self.interpolator.interpolate(data, idx_idx, eval("self.state." + data), val, self.set_component_indices)


    def load_image(self, name, buffer_name):
        ''' Loads and image into the host memory
            and uploads it to a buffer.
              buffer_name can be either fb or aux '''

        data = Image.open("image/input/" + name).convert("RGBA").tostring("raw", "RGBA", 0, -1)

        if(buffer_name == "fb"):
            self.engine.set_fb(data, True, False)
        else:
            self.engine.set_aux(data, True, False)


    def grab_image(self):
        ''' Gets the framebuffer and binds it to an Image. '''


        self.load_state(90)

        #img = Image.frombuffer("RGBA", (self.engine.profile.kernel_dim, self.engine.profile.kernel_dim), self.engine.get_fb(), "raw", "RGBA", 0, -1).convert("RGB")

        #img.show()

        #return img


    def pars(self):
        ''' Prints a list of paramaters, their bindings, and their values. '''

        for i in xrange(len(self.state.par_names)):
            print self.state.par_names[i], ":", i


    def funcs(self):
        ''' Prints a list of all functions available in the command environment. '''

        # sort keys
        keys = self.env.funcs.keys()
        keys.sort()

        for key in keys : print key


    def components(self):
        ''' Prints a list of all components, their bindings, and their values. '''

        keys = self.datamanager.components

        for i in xrange(len(keys)) :
            component = getattr(self.state, keys[i])
            print i+1, ":", keys[i], "-", component, "-", self.datamanager.comment(keys[i], component)


    def save(self, name=None):
        ''' Saves the current state. '''

        name = ConfigManager().save_state(self.state, name)
        self.grab_image().save("image/image_%s.png" % name)

        print "saved state as", name

        self.renderer.flash_message("saved state as %s" % name)


    def load(self, name):
        ''' Loads and blends to the given state. '''

        new_state = ConfigManager().load_dict(name + ".est")

        # blend to zns
        for i in xrange(len(new_state.zn)):

            self.radial_2d(self.state.zn, i, self.context.component_switch_time + COMPILE_TIME, r_to_p(self.state.zn[i]), r_to_p(new_state.zn[i]))

        # blend to pars
        for i in xrange(len(new_state.par)):
            self.linear_1d(self.state.par, i, self.context.component_switch_time + COMPILE_TIME, self.state.par[i], new_state.par[i])

        # remove zn & par from dict
        del new_state.zn
        del new_state.par

        updates = {}

        # update components
        for name in self.datamanager.components:

            if(getattr(self.state, name) != getattr(new_state, name)):

                updates[name] = getattr(new_state, name)

            delattr(new_state, name)

        # blend to components
        for data in updates:

            async(lambda : self.blend_to_component(data, updates[data]))

            time.sleep(0.2)

        # update state
        print self.state.__dict__.update(new_state.__dict__)

        # set indices
        self.set_component_indices()


    def load_state(self, idx):
        ''' Loads and blends to the state with the given id. '''

        self.load("state_%d" % idx)


    def manual(self):
        ''' Toggles manual iteration. '''

        if(self.context.manual_iter):
            self.context.next_frame = True
        self.context.manual_iter = not self.context.manual_iter


    def next(self):
        ''' If manual iteration toggles, andvances frame. '''

        self.context.next_frame = True




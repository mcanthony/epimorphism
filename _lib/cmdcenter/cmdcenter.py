from common.globals import *

from common.runner import *

from video import *
from animator import *
from archiver import *
from componentmanager import *
from script import *
from common.default import *
from common.complex import *
from common.structs import *

from cmd.events import *
from cmd.programs import *

import StringIO, sys, traceback, random
from PIL import Image

from common.log import *
set_log("CMDCENTER")

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


class CmdCenter(Animator, Archiver):
    ''' The CmdCenter is the central control center for the engine and
        renderer.  All systems generating signals route through here, and the object
        provides an interface for executing code int the appropriate environment. '''
    

    def init(self):
        info("Initializing CmdCenter")
        Globals().load(self)

        # init animator
        Animator.__init__(self)

        # init archiver
        Archiver.__init__(self)

        # init componentmanager
        self.componentmanager = ComponentManager()

        # init eventmanager
        self.eventmanager = EventManager()

        # for cycling through existing states
        self.current_state_idx = -1

        # setup application
        self.interface.renderer.set_inner_loop(self.do)
        self.frame = []
        self.engine.frame = self.frame
        self.t_start = None
        self.recorded_events = None

        # create video_renderer
        self.video_renderer = VideoRenderer()

#            self.app.max_video_frames = int(self.initial_script.last_event_time() * 1000 / self.app.video_frame_rate)
#            info("Setting max_video_frames to %d" % self.app.max_video_frames)

        if(self.app.render_video):
            self.video_renderer.start_video()


        # create cmd_env function blacklist
        func_blacklist = ['do', '__del__', '__init__', 'kernel', 'print_timings', 'record_event', 'start', 'switch_kernel',
                          'keyboard', 'console_keyboard', 'register_callbacks', 'render_console', 'capture', 'render_fps',
                          'video_time', 'set_inner_loop', 'time', 'cmd', 'execute_paths', 'echo', 'reshape',
                          'init_component_indices'] + dir(object)

        # extract non-blacklist functions & data from an object
        def get_funcs(obj):
            return dict([(attr, getattr(obj, attr)) for attr in dir(obj) if callable(getattr(obj, attr)) and attr not in func_blacklist])

        # get functions from objects
        funcs = get_funcs(self)
        funcs.update(get_funcs(self.interface.renderer))
        funcs.update(get_funcs(self.video_renderer))
        funcs.update(get_funcs(self.engine))
        funcs.update(get_funcs(self.componentmanager))
        funcs.update(default_funcs)

        # generate cmd exec environment
        self.cmd_env = CmdEnv([{"cmd":self.__dict__, "state":self.state, "app":self.app}, self.state.__dict__, self.interface.app.__dict__, self.app.__dict__], funcs)

        # tap tempo info
        self.tempo_events = []
        self.last_tempo_event_time = 0

        # misc
        self.last_frame_time = 0
        self.programs_initialized = False
        
        return True


    def __del__(self):
        ''' Exit handler '''
        info("Deleting Cmdcenter")

        # stop programs
        for program in self.state.programs:
            program.stop()

        # stop video
        if(self.app.render_video):
            self.video_renderer.stop_video()


    def start(self):
        ''' Start main loop '''
        info("Start main loop")

        self.state.t_phase += self.state.time
        self.state.time = 0
        self.t_start = time.time()
        self.state.frame_cnt = 0

        # seed random
        random.seed(self.state.time + self.state.t_phase)

        # start modules - DOESN'T RETURN
        self.engine.start()
        self.interface.start()
        

    def do(self):
        ''' Main application loop '''

        # execute engine
        if((not (self.app.manual_iter and not self.app.next_frame)) and not self.app.freeze and not self.componentmanager.compiling):
            self.app.next_frame = False

            # get time
            self.state.time = self.abs_time()

            if(self.app.manual_iter):
                d = self.abs_time() - self.last_frame_time
                self.state.t_phase += 1.0 / 30.0 - d

            self.last_frame_time = self.abs_time()


            # execute animation paths
            self.execute_paths()
            
            # render frame
            self.send_frame()
            self.engine.do()

            self.state.frame_cnt += 1
        

        # execute interface
        self.interface.do()

        # capture video frames
        if(self.app.render_video):
            self.video_renderer.capture()

        # cleanup
        if(self.app.exit):
            self.interface.renderer.stop()

        # start programs
        if not self.programs_initialized:
            self.programs_initialized = True        
            for program in self.state.programs:
                program.start()

            for script in self.state.scripts:
                script.data["phase"] = self.time()
                script.start()


    def send_frame(self):
        ''' Generates and sends the current frame to the Engine '''

        del self.frame[:]
        keys = self.state.par.keys()
        keys.sort()
        self.frame.append({"name": "par",         "type": "float_array",   "val": [self.state.par[key] for key in keys]})
        self.frame.append({"name": "internal",    "type": "float_array",   "val": self.state.internal})        
        self.frame.append({"name": "zn",          "type": "complex_array", "val": self.state.zn})    
        self.frame.append({"name": "time",        "type": "float",         "val": self.time()})      


    def cmd(self, code, record = True, capture=False):
        ''' Execute code in the CmdEnv environment '''

        if(self.app.record_events):
            self.recorded_events.push(self.time() - self.app.record_events, code)

#        debug("Executing cmd: %s", code)

        # hijack stdout, if requested
        out = StringIO.StringIO()
        sys.stdout = capture and out or sys.stdout

        err = ""

        # execute code
        if(capture):
            try:
                exec(code) in self.cmd_env
            except:
                err = traceback.format_exc().split("\n")[-2]
        else:
            exec(code) in self.cmd_env

        # restore stdout
        sys.stdout = sys.__stdout__

        # get result
        res = [out.getvalue(), err]

        # close StringIO
        out.close()

        # return result
        return res


    # UTILITY FUNCTIONS
    def abs_time(self):
        ''' Returns the current absolute time '''

        if(self.app.fps_sync):
            return self.state.frame_cnt / float(self.app.fps_sync)
        else:
            return time.time() - self.t_start


    def time(self):
        ''' Returns the current relative time '''

        return self.state.t_speed * (self.abs_time() + self.state.t_phase)


    def get_val(self, var, idx):
        return eval("self.%s[%s]" % (var, (((type(idx) == int) and "%s" or "'%s'") % idx)))


    def update_current_state_idx(self, idx=1):
        self.current_state_idx += idx
        self.load(self.current_state_idx)


    def load_image(self, name):
        ''' Loads and image into the host memory
            and uploads it to a buffer.
              buffer_name can be either fb or aux '''
        info("Load image: %s", name)

        self.engine.load_aux(Image.open("media/image/" + name).convert("RGBA"))


    def grab_image(self):
        ''' Gets the framebuffer and binds it to an Image. '''
        info("Grab image")

        try:
            self.app.next_frame = True
            pixels = self.interface.renderer.grab_pixels()
            img = Image.frombuffer('RGBA', (self.app.kernel_dim, self.app.kernel_dim), pixels, 'raw', 'BGRA', 0, 1).transpose(Image.FLIP_TOP_BOTTOM)
        except Exception, err:
            info(str(err))
            sys.exit(0)

        info("Done grab image")

        # img.show()
        return img


    def pars(self):
        ''' Prints a list of paramaters, their bindings, and their values. '''
        print str(self.state.pars)


    def funcs(self):
        ''' Prints a list of all functions available in the command environment. '''

        # sort keys
        keys = self.app.funcs.keys()
        keys.sort()

        for key in keys : print key


    def components(self):
        ''' Prints a list of all components, their bindings, and their values. '''

        self.componentmanager.print_components()


    def save(self, name=None):
        ''' Grabs a screenshot and saves the current state. '''

        name = self.state.save(name)

        self.grab_image().save("media/image/%s.png" % name)
        self.interface.renderer.flash_message("saved state as %s" % name)

        return name        


    # needs some work - right now it only loads components, zn & par
    def load(self, name, immediate=False):
        ''' Loads and blends to the given state. '''

        info("Loading state: %s" % name)

        new_state = State(self.app.app, str(name))
        if(not new_state):
            return False
        
        updates = {}

        # if immediate, change switch time
        if(immediate):
            old_intrp_time = self.app.state_intrp_time
            self.app.state_intrp_time = 0.000001            

        # get update components
        for name in self.componentmanager.component_list():
            if(self.state.components[name] != new_state.components[name]):
                updates[name] = new_state.components[name]

            del(new_state.components[name])

        if(not self.componentmanager.can_switch_to_components(updates)):
            error("Failed to load state")
            return False

        info("Loading state, updating components: %s" % str(updates))

        # stop paths, scripts & programs
        self.state.paths = []

        for script in self.state._script:
            script.stop()

        for program in self.state.programs:
            program.stop()

        # blend to zns
        for i in xrange(len(new_state.zn)):
            self.radial_2d('state.zn', i, self.app.state_intrp_time, r_to_p(self.state.zn[i]), r_to_p(new_state.zn[i]))

        # blend to pars
        for i in xrange(len(new_state.par)):
            self.linear_1d('state.par', i, self.app.state_intrp_time, self.state.par[i], new_state.par[i])

        # load evolution
        def load_paths():
            time.sleep(self.app.state_intrp_time)
            self.state.paths = []
            for path in new_state.paths:
                path.phase = new_state.time - self.time()
                self.state.paths.append(path)

            for program in new_state.programs:
                program.start()
                self.state.programs.append(program)

            for script in new_state._script:
                script.phase += self.time()
                script.start()
                self.state._script.append(script)

        async(load_paths)

        self.componentmanager.switch_components(updates)

        # if immediate, revert switch time
        if(immediate):
            self.app.state_intrp_time = old_intrp_time


    def toggle_record(self):
        ''' Toggles event recording '''
        
        if(not self.app.record_events):
            info("Recording script")
            self.app.record_events = self.time()
            self.recorded_events = Script()

            self.record_state = State(self.state.app_name, self.state.save(self.state.name + "_record"))

            self.interface.renderer.flash_message("Recording script")
        else:            
            info("Saving recorded script")
            self.app.record_events = False

            self.recorded_events.save()   
            self.record_state.scripts.append(self.recorded_events)
            self.record_state.save(self.record_state.name)
            
            self.interface.renderer.flash_message("Saved state as %s" % (self.state.name))
            info("Saved state as %s" % (self.record_state.name))
            self.recorded_events = None


    def toggle_manual(self):
        ''' Toggles manual iteration. '''

        if(self.app.manual_iter):
            self.app.next_frame = True

        self.app.manual_iter = not self.app.manual_iter


    def next(self):
        ''' If manual iteration toggles, andvances frame. '''

        self.app.next_frame = True


    def tap_tempo(self):
        ''' Uses tap tempo to set bmp '''

        t = self.time()

        # reset if necessary
        if(t - self.last_tempo_event_time > 2):
            self.tempo_events = []

        # set & append
        self.last_tempo_event_time = t
        self.tempo_events.append(t)

        # max 20 events
        if(len(self.tempo_events) > 20):
            self.tempo_events.pop(0)

        # compute tempo
        if(len(self.tempo_events) > 1):
            lst = [self.tempo_events[i + 1] - self.tempo_events[i] for i in xrange(len(self.tempo_events) - 1)]
            self.state.bmp = 1.0 / (sum(lst) / (len(self.tempo_events) - 1)) * 60
            info("Tempo: %s bmp" % self.state.bmp)

               
    def reset_zn(self):
        default = State(self.app.app)
        for i in xrange(len(default.zn)):
            self.cmdcenter.radial_2d('state.zn', i, 0.4, r_to_p(self.state.zn[i]), r_to_p(default.zn[i]))


    def reset_par(self):
        default = State(self.app.app)
        for i in xrange(len(default.par)):
            self.cmdcenter.linear_1d('state.par', i, 0.4, self.state.par[i], default.par[i])

    
    def quit(self):
        self.app.exit = True
        sys.exit(0)


import config

from common.globals import *

from common.runner import *
from math import *

from video import *
from animator import *
from path import *
from archiver import *
from componentmanager import *
from script import *
from common.default import *
from common.complex import *
from common.structs import *

from cmd.events import *
from cmd.programs import *

import StringIO, sys, traceback, random, copy

if config.PIL_available:
    from PIL import Image

if config.app.camera_enabled:
    import cv

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
                

class CmdCenter(Archiver):
    ''' The CmdCenter is the central control center for the engine and
        renderer.  All systems generating signals route through here, and the object
        provides an interface for executing code int the appropriate environment. '''
    

    def init(self):
        info("Initializing CmdCenter")
        Globals().load(self)

        # init animator
        self.animator = Animator()
        self.linear_1d = self.animator.linear_1d
        self.radial_2d = self.animator.radial_2d

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
                          'video_time', 'set_inner_loop', 'time', 'cmd', 'echo', 'reshape',
                          'init_component_indices', 'handle_event'] + dir(object)

        # extract non-blacklist functions & data from an object
        def get_funcs(obj):
            return dict([(attr, getattr(obj, attr)) for attr in dir(obj) if callable(getattr(obj, attr)) and attr not in func_blacklist])

        # get functions from objects
        funcs = get_funcs(self)
        funcs.update(get_funcs(self.interface.renderer))
        funcs.update(get_funcs(self.video_renderer))
        funcs.update(get_funcs(self.engine))
        funcs.update(get_funcs(self.componentmanager))
        funcs.update(get_funcs(self.eventmanager))
        funcs.update(default_funcs)
        funcs.update(dict([(cls.__name__, cls) for cls in vars()['Program'].__subclasses__()]))

        # generate cmd exec environment
        paths = dict([(sub.__name__, sub) for sub in Path.__subclasses__()])
        self.cmd_env = CmdEnv([{"cmd":self.__dict__, "state":self.state, "app":self.app}, self.state.__dict__, self.app.__dict__, paths], funcs)

        # tap tempo info
        self.tempo_events = []
        self.last_tempo_event_time = 0

        # misc
        self.last_frame_time = 0
        self.programs_initialized = False

        # camera
        if config.app.camera_enabled and config.state.camera_id:
            self.camera = cv.CreateCameraCapture(0)#config.state.camera_id)
        
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

        config.last_frame_time = self.time()

        # seed random
        if(self.state.randomize_seed):
            random.seed(time.time())
        else:
            random.seed(self.state.time + self.state.t_phase)

        # start modules - DOESN'T RETURN
        self.engine.start()
        self.interface.start()
        

    def do(self):
        ''' Main application loop '''

        #print self.state.par['_SEED_TEX_IDX']
        #print self.state.aux
        
        # execute engine
        if((not (self.app.manual_iter and not self.app.next_frame)) and not self.app.freeze and not self.componentmanager.compiling):
            self.app.next_frame = False

            # get time
            self.state.time = self.abs_time()
#            print "T", self.time()

            if(self.app.manual_iter):
                d = self.abs_time() - self.last_frame_time
                self.state.t_phase += 1.0 / 30.0 - d


            self.last_frame_time = self.abs_time()


            # execute animation paths
            self.animator.execute_paths()
            
            # render frame
            self.send_frame()
            self.engine.do()

            self.state.frame_cnt += 1
            #print "t elapsed:", self.abs_time() - self.last_frame_time
        

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
                if isinstance(program, Script):
                    program.data["phase"] = self.time()
                program.start()
        
        # upload frame
        if config.app.camera_enabled and config.state.camera_id:
            self.upload_webcam_frame()


    def send_frame(self):
        ''' Generates and sends the current frame to the Engine '''

        del self.frame[:]
        keys = self.state.par.keys()
        keys.sort()
        pars = [self.state.par[key] for key in keys]
        pars = [item for sublist in pars for item in sublist]
        self.frame.append({"name": "par",         "type": "float_array",   "val": pars})
        self.frame.append({"name": "internal",    "type": "float_array",   "val": self.state.internal})        
        self.frame.append({"name": "zn",          "type": "complex_array", "val": self.state.zn})    
        self.frame.append({"name": "time",        "type": "float",         "val": self.time()})      

        config.last_frame_time = self.time()


    def cmd(self, code, record = True, capture=False):
        ''' Execute code in the CmdEnv environment '''

        print code
        
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
                err = traceback.format_exc() #.split("\n")[-2]
        else:
            exec(code) in self.cmd_env

        # restore stdout
        sys.stdout = sys.__stdout__

        # get result
        res = [out.getvalue(), err]

        if(res != ["", ""]):
            debug("console res: %s", str(res))

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


    def load_image(self, name, idx):
        ''' Loads and image into the aux buffer
            and uploads it to a buffer.
            '''
        if not config.PIL_available:
            warning("PIL not available")
            return None

        info("Load image: %s, %d", name, idx)

        self.state.aux[idx] = name

        img = Image.open("media/textures/" + name).convert("RGBA")
        self.engine.load_aux(img.resize((self.app.kernel_dim, self.app.kernel_dim)), idx)
        info("Done load image: %s", name)


    def upload_webcam_frame(self):
        #if config.PIL_available: self.engine.load_aux(cv.adaptors.Ipl2PIL(cv.cvQueryFrame(self.camera)).convert("RGBA"))
        if config.PIL_available:            
            cv_im = cv.QueryFrame(self.camera)
            pi = Image.fromstring("RGB", cv.GetSize(cv_im), cv_im.tostring())
            self.engine.load_aux(pi.convert("RGBA"))
        


    def pars(self):
        ''' Prints a list of paramaters, their bindings, and their values. '''
        print str(self.state.par)


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

        if not config.PIL_available:
            warning("PIL not available")
            return name

        self.app.next_frame = True
        img = self.interface.renderer.grab_image()
        #img.save("media/image/%s_%s.jpg" % (self.app.app, name))
        img.convert("RGB").save("media/image/%s_%s.png" % (self.app.app, name))
        #self.interface.renderer.grab_image().save("media/image/%s_%s.jpg" % (self.app.app, name))

        self.interface.renderer.flash_message("saved state as %s_%s" % (self.app.app, name))

        return name        


    # needs some work - right now it only loads components, zn & par
    def load(self, name, immediate=False):
        ''' Loads and blends to the given state. '''

        info("Loading state: %s" % name)

        new_state = State(self.app.app, str(name))
        if(not new_state):
            return False    

        # if immediate, change switch time
        if(immediate):
            old_intrp_time = self.app.state_intrp_time
            self.app.state_intrp_time = 0.000001            

        # stop paths, scripts & programs
        [path.stop() for path in self.state.paths]

        [program.stop() for program in self.state.programs]

        # blend to zns
        for i in xrange(len(new_state.zn)):
            self.radial_2d('zn', i, self.app.state_intrp_time, r_to_p(self.state.zn[i]), r_to_p(new_state.zn[i]))

        # blend to pars
        for k in new_state.par.keys():
            self.linear_1d('par', k, self.app.state_intrp_time, self.state.par[k], new_state.par[k])

        self.componentmanager.switch_components(new_state.components)

        # fix time
        #self.state.t_phase = new_state.t_speed * (new_state.time + new_state.t_phase) / self.state.t_speed - self.state.time
        #print "setting phase", self.state.t_phase
        #self.state.t_speed = new_state.t_speed

        # load evolution
        for path in new_state.paths:
            path.phase -= self.state.t_speed * (new_state.time + new_state.t_phase) / self.state.t_speed - self.state.time
            self.state.paths.append(path)
            
        for program in new_state.programs:
            program.start()
            self.state.programs.append(program)
            if isinstance(program, Script):
                program.data["phase"] = self.time()

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
            self.record_state.programs.append(self.recorded_events)
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
            self.radial_2d('zn', i, 0.4, r_to_p(self.state.zn[i]), r_to_p(default.zn[i]))


    def reset_par(self):
        default = State(self.app.app)
        for i in xrange(len(default.par)):
            self.linear_1d('par', i, 0.4, self.state.par[i], default.par[i])

    def runProgram(self, prg):
        self.state.programs.append(prg)
        prg.run()        

    # convert rect to polar - GHETTO - shouldn't be here
    def r_to_p(self, z):
        arg = atan2(z.imag, z.real)
        if(arg < 0) : arg += 2.0 * 3.14159
        return [abs(z), arg]
                
    def quit(self):
        self.app.exit = True
        sys.exit(0)




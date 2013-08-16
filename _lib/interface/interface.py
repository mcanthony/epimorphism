# The interface controls the applications input from & output to the external world.  Information comes in via any of the possible 
# interfaces - keyboard, mouse, midi, server, and is then fed to the CmdCenter.  The CmdCenter takes all of this information, as well
# as the State configuration object and creates a Frame.  The Frame is sent to the Engine, which is then uploaded to the hardware.  
# The Engine is synchronized with the Renderer via a pbo, which is then rendered and then displayed.

# The program is controlled by two types of variables - continuous and discrete. The continuous variables are numerical parameters, 
# corresponding normally either to real numbers, or components(r, th, x, y) of complex numbers.  The discrete variables simply 
# choose one value from a collection of possibilities.

import config

from common.globals import *

from renderer import Renderer

from console import Console

import urllib

from server import *
from input_handlers.mousehandlers import *
from input_handlers.keyboardhandlers import *
from input_handlers.oschandlers import *
from midihandler import *

from common.log import *
set_log("INTERFACE")


class Interface(object):

    def init(self):
        info("Initializing interface")
        Globals().load(self)

        self.renderer = Renderer()
        return True


    def __del__(self):
        info("Deleting Interface")

        self.renderer.__del__()

        if(self.server):
           self.server.__del___()


    def start(self):
        info("Starting interface")

        # create input handlers
#        self.mouse_handler = eval(self.app.mouse_handler + "()")
        self.keyboard_handler = eval(self.app.keyboard_handler + "()")

        # create_console
        if config.PIL_available:
            console = Console()
            self.renderer.register_console_callbacks(console.render_console, console.console_keyboard)

        # register callbacks & console with Renderer
        self.renderer.register_callbacks(self.keyboard_handler.do_key, None, None)#self.mouse_handler.do_button, self.mouse_handler.do_motion)

        # register cmdcenter with renderer
        self.renderer.cmdcenter = self.cmdcenter

        # start server
        if(self.app.server):
            self.server = Server()
            self.server.start()
        else:
            self.server = None

        # start midi
        if(self.app.midi_enabled):
            self.app.last_midi_event = self.cmdcenter.time()
            self.midi = MidiHandler()

            # sync par & zn lists to controller
            if(self.app.midi_echo):
                self.cmdcenter.state.par.add_observer(midi.mirror)
                self.cmdcenter.state.zn.add_observer(midi.mirror)

            # start midi
            self.midi.start()
        else:
            self.midi = None

        # start osc
        if(self.app.OSC_enabled):
            self.osc = eval(self.app.OSC_handler + "()")
            self.osc.start()
            
            # sync par & zn lists to controller
            
            if(self.app.OSC_echo):
                self.cmdcenter.state.par.add_observer(self.osc.mirror)
                self.cmdcenter.state.zn.add_observer(self.osc.mirror)            
                self.cmdcenter.state.components.add_observer(self.osc.mirror)            
                self.cmdcenter.state.add_observer(self.osc.mirror)

        self.renderer.start()


    def do(self):
        # execute renderer
        self.renderer.do()

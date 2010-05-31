# The program is controlled by two types of variables - continuous and discrete. The continuous variables are numerical parameters, 
# corresponding normally either to real numbers, or components(r, th, x, y) of complex numbers.  The discrete variables simply 
# choose one value from a collection of possibilities.

# KEYBOARD:
# There are a number of mappings from keys on the keyboard to these variables and other actions.  See noumena/keyboard.txt for details.  
# For the main keyboard body, all generally tend to follow a similar scheme where the key underneath(below & to the right) is 
# opposite to the key above.  For instance the '1' key may cycle through the possibilities for a discrete variable, while the 'q' key 
# would cycle in the opposite direction.  Similarly for continuous variables.  'a' may increase a variable by 0.1, but 'z' would decrease it by 0.1

# MIDI:
# The


from common.globals import *

from noumena.renderer import *

from noumena.console import *
from noumena.keyboard import *
from noumena.mouse import *
from noumena.server import *
from noumena.midi import *

from common.log import *
set_log("INTERFACE")

import sys

class Interface(object):

    def init(self):
        debug("Initializing interface")
        Globals().load(self)

        self.renderer = Renderer()

        return True


    def __del__(self):
        debug("Deleting Interface")
        # self.renderer.__del__()
        # kill server
        # if(self.server):
        #   self.server.__del___()
        pass


    def start(self):
        debug("Starting interface")

        # create input handlers
        self.mouse_handler = MouseHandler()
        self.keyboard_handler = KeyboardHandler()

        # create_console
        console = Console()

        # register callbacks & console with Renderer
        self.renderer.register_callbacks(self.keyboard_handler.keyboard, self.mouse_handler.mouse, self.mouse_handler.motion)
        self.renderer.register_console_callbacks(console.render_console, console.console_keyboard)

        # register cmdcenter with renderer
        self.renderer.cmdcenter = self.cmdcenter

        # start server
        if(self.context.server):
            self.server = Server()
            self.server.start()

        else:
            self.server = None

        # start midi
        if(self.app.midi_enabled):
            self.midi = MidiHandler()

            if(self.app.midi_enabled):
                # sync midi lists to controller
                self.cmdcenter.state.zn.midi = self.midi
                self.cmdcenter.state.par.midi = self.midi
                self.midi.start()

        else:
            self.midi = None

        self.renderer.start()


    def do(self):
        self.renderer.do()

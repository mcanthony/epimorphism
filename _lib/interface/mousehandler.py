from common.globals import *

from common.runner import *

from common.log import *
set_log("Mouse")

class MouseHandler(object):
    ''' The MouseHandler is the GLUT callback that handles keyboard events
        in the Renderer object during normal operation '''


    def __init__(self):
        Globals().load(self)

        # init coords
        self.vp_start_x = 0
        self.vp_start_y = 0
        self.mouse_start_x = 0
        self.mouse_start_y = 0


    def do_button(self, button, state, x, y):
        async(lambda: self.button(button, state, x, y))


    def do_motion(self, x, y):
        async(lambda: self.motion(x, y))


    def button(self, button, state, x, y):
        pass
    

    def motion(self, x, y):
        pass

     




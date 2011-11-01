from common.globals import *

from OpenGL.GLUT import *

from common.runner import *

from common.log import *
set_log("KEYBOARD")

class KeyboardHandler(object):
    ''' The KeyboardHandler is the GLUT callback that handles keyboard events
        in the Renderer object during normal opperation '''

    def __init__(self):
        Globals().load(self)

        # initialize component list
        self.components = self.cmdcenter.componentmanager.component_list()

    def do_key(self, key, x, y):
        modifiers = glutGetModifiers()                
        #import gc
        #gc.collect()
        
        #async(lambda : self.key_pressed(key, modifiers))
        self.key_pressed(key, modifiers)

    def key_pressed(self, key, modifiers):
        pass

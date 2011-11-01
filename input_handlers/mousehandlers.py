from OpenGL.GLUT import *

from interface.mousehandler import MouseHandler

class DefaultMouse(MouseHandler):
    def button(self, button, state, x, y):
        if(state == GLUT_DOWN):
            # set start center drag coords
            if(button == 0):
                self.vp_start_x = self.app.viewport[0]
                self.vp_start_y = self.app.viewport[1]

                self.mouse_start_x = x
                self.mouse_start_y = y

        elif(state == GLUT_UP):
            # on right click, reset scale/center
            if(button == 2):
                self.app.viewport[2] = 1.0
                self.app.viewport[0] = 0.0
                self.app.viewport[1] = 0.0

            # mousewheel up, increase scale
            elif(button == 4):
                self.app.viewport[2] *= 1.1

            # mousewheel up, decrease scale
            elif(button == 3):
                self.app.viewport[2] /= 1.1


    def motion(self, x, y):
        # drag center
        self.app.viewport[0] = self.vp_start_x + self.app.viewport[2] * (x - self.mouse_start_x) / self.app.screen[0];
        self.app.viewport[1] = self.vp_start_y + self.app.viewport[2] * (y - self.mouse_start_y) / self.app.screen[1];
        

class DefaultInterferenceMouse(DefaultMouse):
    def button(self, button, state, x, y):
        DefaultMouse.button(self, button, state, x, y)

    def motion(self, x, y):
        DefaultMouse.motion(self, x, y)


class DefaultEpimorphismMouse(DefaultMouse):
    def button(self, button, state, x, y):
        DefaultMouse.button(self, button, state, x, y)

        # drag center
        self.state.sphere_rot[0] = self.app.viewport[0] = self.vp_start_x + self.app.viewport[2] * (x - self.mouse_start_x) / self.app.screen[0];
        self.state.sphere_rot[1] = self.app.viewport[1] = self.vp_start_y + self.app.viewport[2] * (y - self.mouse_start_y) / self.app.screen[1];
        self.state.sphere_rot = self.app.viewport[0] + self.app.viewport[1] * 1j

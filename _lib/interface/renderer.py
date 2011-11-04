# The renderer is an OpenGL context, via GLUT, which is responsible for rendering the Engine's output
# It is synchronized with the engine via a pbo

import time, sys, os, commands, threading

from common.globals import *
from common.runner import *

from ctypes import *
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

from ctypes import *

import common.glFreeType
FONT_PATH = "_lib/common/FreeSansBold.ttf"

from common.log import *
set_log("RENDERER")


class Renderer(object):
    ''' The Renderer object is responsible for displaying the system via OpenGL/GLUT '''

    def __init__(self):
        debug("Initializing Renderer")
        Globals().load(self)

        # set variables
        self.screen = self.app.screen

        # initialize glut
        glutInit(1, [])

        # create window
        debug("Creating window")

        glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGBA)

        try:
            if(self.app.screen == "auto"):
                if(os.name == "posix"):
                    # call xrandr & parse output
                    output = commands.getstatusoutput("xrandr")[1].split("\n")[1]
                    print output
                    output = output[output.index("maximum") + 8:].split(" x ")                    
                    print output
                    max = (int(output[0]), int(output[1]))
                    print str(max)
                else:
                    # TODO generalize to other operating systems
                    max = (1024, 768) 
                self.app.screen = [max[0], max[1], True]

            if(self.app.screen[2]):
                glutGameModeString(str(self.app.screen[0]) + "x" +
                                   str(self.app.screen[1]) + ":24@60")
                glutEnterGameMode()

            else:
                glutInitWindowSize(self.app.screen[0], self.app.screen[1])
                glutInitWindowPosition(10, 10)
                glutCreateWindow(self.app.name)
        except:
            exception("Failed to create window")
            sys.exit()

        glutSetCursor(GLUT_CURSOR_NONE)

        # register callbacks
        glutReshapeFunc(self.reshape)

        # init gl
        glEnable(GL_TEXTURE_2D)
        glClearColor(0.0, 0.0, 0.0, 0.0)
        glShadeModel(GL_SMOOTH)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glClearDepth(1.0)			
        glDepthFunc(GL_LESS)			
        glEnable(GL_DEPTH_TEST)			

        # quadric
        self.quad = gluNewQuadric()
        gluQuadricNormals(self.quad, GLU_SMOOTH)
	gluQuadricTexture(self.quad, GL_TRUE)        

        # fps data
        self.d_time_start = self.d_time = self.d_timebase = 0
        self.frame_count = 0.0

        # misc variables
        self.show_console = False
        self.show_fps = False
        self.fps = self.fps_avg = 100
        self.fps_font_size = 16
        self.fps_font = common.glFreeType.font_data(FONT_PATH, self.fps_font_size)

        self.echo_string = None
        self.echo_font_size = int(0.0123 * self.app.screen[0] + 2.666)
        self.echo_font = common.glFreeType.font_data(FONT_PATH, self.echo_font_size)

        self.do_main_toggle_console = False

        self.pbo_ptr = None

        self.have_pixels = threading.Event()
        self.have_pixels.set()
        self.pixels = []
        

    def __del__(self):
        debug("Deleting Renderer")

        self.pbo_ptr = None


    def generate_pbo(self, buffer_dim):
        ''' Generate and return pbo of given dimension '''

        self.buffer_dim = buffer_dim

        # generate pbo
        self.pbo_ptr = GLuint()
        glGenBuffers(1, byref(self.pbo_ptr))
        glBindBuffer(GL_ARRAY_BUFFER, self.pbo_ptr)

        num_texels = self.buffer_dim ** 2

        empty_buffer = (c_char * (sizeof(c_char) * 4 * num_texels))()
        glBufferData(GL_ARRAY_BUFFER, num_texels * 4 * sizeof(c_char),
                     empty_buffer, GL_DYNAMIC_DRAW)
        glBindBuffer(GL_ARRAY_BUFFER, 0)

        # generate texture & set parameters
        self.display_tex = GLuint()
        glGenTextures(1, byref(self.display_tex))
        glBindTexture(GL_TEXTURE_2D, self.display_tex)

        glPixelStorei(GL_UNPACK_ALIGNMENT,1)
        glTexImage2D(GL_TEXTURE_2D, 0, 3, self.buffer_dim, self.buffer_dim,
                     0, GL_RGBA, GL_UNSIGNED_BYTE, None)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

        return self.pbo_ptr


    def reshape(self, w, h):
        debug("Reshape %dx%d" % (w, h))

        # set viewport
        self.app.screen[0] = w
        self.app.screen[1] = h
        self.aspect = float(w) / float(h)
        glViewport(0, 0, self.app.screen[0], self.app.screen[1])

        # configure projection matrix
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        if(self.state.render_mode != '2D'):
            gluPerspective(90.0, self.aspect, 0.1, 100.0)
        else:
            glOrtho(-1.0, 1.0, -1.0, 1.0, -1.0, 1.0)
        glMatrixMode(GL_MODELVIEW)

        
    def grab_pixels(self):
        info("Grabbing pixels")
        self.have_pixels.clear()
        self.have_pixels.wait()
        return self.pixels

    def render_fps(self):
        # if this isn't set font looks terrible
        glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_MODULATE)

        # render text into ulc
        glColor3ub(0xff, 0xff, 0xff)
        self.fps_font.glPrint(6, self.app.screen[1] - self.fps_font_size - 6, "fps: %.2f" % (1000.0 / self.fps))
        self.fps_font.glPrint(6, self.app.screen[1] - 2 * self.fps_font_size - 10, "avg: %.2f" % (1000.0 / self.fps_avg))


    def echo(self):
        # if this isn't set font looks terrible
        glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_MODULATE)

        # render text into llc
        glColor3ub(0xff, 0xff, 0xff)
        self.echo_font.glPrint(6, 6, self.echo_string)


    def main_toggle_console(self):
        ''' Main thread callback to toggle console '''

        self.do_main_toggle_console = False

        # toggle console
        self.show_console = not self.show_console

        # juggle keyboard handlers
        if(self.show_console):
            glutKeyboardFunc(self.console_keyboard)
            glutSpecialFunc(self.console_keyboard)
        else:
            glutSpecialFunc(self.keyboard)
            glutKeyboardFunc(self.keyboard)


    def do(self):
        # test for existence of pbo
        if(not self.pbo_ptr):
            critical("can't render without a pbo")
            sys.exit()
            return

        # main thread toggle_console
        if(self.do_main_toggle_console) : self.main_toggle_console()

        # compute frame rate
        if(self.d_time == 0):
            self.frame_count = 0
            self.d_time_start = self.d_time = self.d_timebase = glutGet(GLUT_ELAPSED_TIME)
        else:
            self.frame_count += 1
            self.d_time = glutGet(GLUT_ELAPSED_TIME)
            if(self.frame_count % 10 == 0):
                self.fps = (1.0 * self.d_time - self.d_timebase) / 10
                self.fps_avg = (1.0 * self.d_time - self.d_time_start) / self.frame_count
                self.d_timebase = self.d_time

        # copy texture from pbo
        glBindBuffer(GL_PIXEL_UNPACK_BUFFER_ARB, self.pbo_ptr.value)
        glBindTexture(GL_TEXTURE_2D, self.display_tex)
        glTexSubImage2D(GL_TEXTURE_2D, 0, 0, 0, self.buffer_dim, self.buffer_dim,
                        GL_BGRA, GL_UNSIGNED_BYTE, None)
        glBindBuffer(GL_PIXEL_UNPACK_BUFFER_ARB, 0)

        glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL)
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);

	glLoadIdentity();			
        if(self.state.render_mode == 'Sphere'):
            glTranslatef(0, 0, -1.0 * self.app.viewport[2])
            glRotatef(100.0 * self.state.sphere_rot[0], 1.0,0.0,0.0)                      	
            glRotatef(100.0 * self.state.sphere_rot[1], 0.0,1.0,0.0)                      	

            gluSphere(self.quad, 1.3, 256, 256);

        else:

            # compute texture coordinates
            x0 = .5 - self.app.viewport[2] / 2 - self.app.viewport[0] * self.aspect
            x1 = .5 + self.app.viewport[2] / 2 - self.app.viewport[0] * self.aspect
            y0 = .5 - self.app.viewport[2] / (2 * self.aspect) + self.app.viewport[1]
            y1 = .5 + self.app.viewport[2] / (2 * self.aspect) + self.app.viewport[1]

            # render texture
            glBegin(GL_QUADS)

            glTexCoord2f(x0, y0)
            glVertex3f(-1.0, -1.0, 0)
            glTexCoord2f(x1, y0)
            glVertex3f(1.0, -1.0, 0)
            glTexCoord2f(x1, y1)
            glVertex3f(1.0, 1.0, 0)
            glTexCoord2f(x0, y1)
            glVertex3f(-1.0, 1.0, 0)
            glEnd()    

        # render console
        if(self.show_console):
            self.render_console()

        # render fps
        if(self.show_fps):
            self.render_fps()

        # messages
        if(self.app.echo and self.echo_string):
            self.echo()

        if(not self.have_pixels.isSet()):
            debug("internal grab pixels")
            glBindBuffer(GL_ARRAY_BUFFER, self.pbo_ptr.value)
            #self.pixels = glReadPixelsb(0, 0, self.app.kernel_dim, self.app.kernel_dim, GL_RGBA)
            self.pixels = glMapBuffer(GL_ARRAY_BUFFER, GL_READ_ONLY)
            self.pixels = cast(self.pixels, POINTER(c_ubyte * 4 * self.app.kernel_dim ** 2)).contents
            glUnmapBuffer(GL_ARRAY_BUFFER)
            glBindBuffer(GL_ARRAY_BUFFER, 0)
            self.have_pixels.set()


        # repost
        glutSwapBuffers()
        glutPostRedisplay()



    ######################################### PUBLIC ##################################################


    def set_inner_loop(self, inner_loop):
        ''' Set the display function to be inner_loop
            this is the main thread of the application '''

        glutDisplayFunc(inner_loop)


    def start(self):
        ''' Starts the main glut loop '''
        debug("Start GLUT main loop")

        glutMainLoop()


    def stop(self):
        ''' Stops the main glut loop '''
        debug("Stop GLUT main loop")

        glutLeaveMainLoop()


    def register_callbacks(self, keyboard, mouse, motion):
        ''' Registers input & console callbacks with openGL '''
        debug("Registering input callbacks")

        self.keyboard = keyboard
        glutKeyboardFunc(keyboard)
        glutSpecialFunc(keyboard)
        glutMouseFunc(mouse)
        glutMotionFunc(motion)


    def register_console_callbacks(self, render_console, console_keyboard):
        ''' Registers console callbacks '''
        debug("Registering console callbacks")

        self.render_console = render_console
        self.console_keyboard = console_keyboard


    def flash_message(self, msg, t=3):
        ''' Temporarily displays a message on the screen. '''

        self.echo_string = msg

        def delayed_reset_echo():
            time.sleep(t)
            self.echo_string = None

        async(delayed_reset_echo)


    def toggle_console(self):
        ''' Toggles the interactive console '''
        debug("Toggle console")

        self.do_main_toggle_console = True


    def toggle_fps(self):
        ''' Toggles the fps display '''
        debug("Toggle FPS")

        # reset debug information
        self.d_time = 0

        # toggle fps display
        self.show_fps = not self.show_fps


    def toggle_echo(self):
        ''' Toggles echoing '''

        # toggle echo
        self.app.echo = not self.app.echo

        info("Toggle echo %s", str(self.app.echo))





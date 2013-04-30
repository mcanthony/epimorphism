# The renderer is an OpenGL context, via GLUT, which is responsible for rendering the Engine's output
# It is synchronized with the engine via a pbo

import time, sys, threading

from common.globals import *
from common.runner import *

from ctypes import *
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

from ctypes import *

import config

if config.PIL_available:
    from PIL import Image
    import common.glFreeType

FONT_PATH = "_lib/common/FreeSansBold.ttf"

from common.log import *
set_log("RENDERER")


class Renderer(object):
    ''' The Renderer object is responsible for displaying the system via OpenGL/GLUT '''

    def __init__(self):
        info("Initializing Renderer")
        Globals().load(self)

        # set variables
        self.screen = self.app.screen

        # initialize glut
        glutInit(1, [])

        # application will continue after glut exits - make sure app is cleaned up
        #glutSetOption(GLUT_ACTION_ON_WINDOW_CLOSE, GLUT_ACTION_CONTINUE_EXECUTION)

        # create window
        info("Creating window")

        glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGBA)

        if(self.app.screen == "auto"):
            self.window = glutCreateWindow(self.app.name)
            glutFullScreen()
            self.app.screen=[0,0]
        else:
            glutInitWindowSize(self.app.screen[0], self.app.screen[1])
            glutInitWindowPosition(10, 10)
            self.window = glutCreateWindow(self.app.name)

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
        self.frame_count = 0.0

        # misc variables
        self.show_console = False
        self.show_fps = False
        self.fps = self.fps_avg = 100

        self.echo_string = None

        self.do_main_toggle_console = False

        self.pbo_ptr = None

        self.have_image = threading.Event()
        self.have_image.set()

        self.image = None
        

    def __del__(self):
        info("Deleting Renderer")

        self.pbo_ptr = None


    def generate_pbo(self, buffer_dim):
        ''' Generate and return pbo of given dimension '''

        self.buffer_dim = buffer_dim

        # generate pbo
        self.pbo_ptr = glGenBuffers(1)
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
        info("Reshape %dx%d" % (w, h))

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
        
        # create echo font 
        if config.PIL_available:
            self.echo_font_size = int(0.0123 * self.app.screen[0] + 2.666)
            self.echo_font = common.glFreeType.font_data(FONT_PATH, self.echo_font_size)
            self.fps_font_size = 20
            self.fps_font = common.glFreeType.font_data(FONT_PATH, self.fps_font_size)

        
    def grab_image(self):
        if not config.PIL_available:
            warning("PIL is not available")
            return None

        info("Grabbing pixels")
        self.have_image.clear()
        self.have_image.wait()
        return self.image


    def render_fps(self):
        # if this isn't set font looks terrible
        glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_MODULATE)

        # render text into ulc
        glColor3ub(0xff, 0xff, 0xff)
        self.fps_font.glPrint(6, self.app.screen[1] - self.fps_font_size - 6, "fps: %.2f" % (1000.0 / self.fps))


    def echo(self):
        # if this isn't set font looks terrible
        glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_MODULATE)

        # render text into ulc
        glColor3ub(0xff, 0xff, 0xff)
        self.fps_font.glPrint(6, 6, self.echo_string)


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

        self.frame_count += 1
        # compute frame rate
        if(self.frame_count % 60 == 0):            
            cur_time = glutGet(GLUT_ELAPSED_TIME)
            self.fps = (cur_time - self.d_timebase) / 60.0
            self.d_timebase = cur_time

        # copy texture from pbo
        glBindBuffer(GL_PIXEL_UNPACK_BUFFER_ARB, self.pbo_ptr)
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
        if(self.show_fps and config.PIL_available):
            self.render_fps()

        # messages
        if(self.app.echo and self.echo_string and config.PIL_available):
            self.echo()

        # grab image
        if(not self.have_image.isSet()):
            debug("internal grab image")
            glBindBuffer(GL_ARRAY_BUFFER, self.pbo_ptr)
            #self.pixels = glReadPixelsb(0, 0, self.app.kernel_dim, self.app.kernel_dim, GL_RGBA)
            pixels = glMapBuffer(GL_ARRAY_BUFFER, GL_READ_ONLY)
            pixels = cast(pixels, POINTER(c_ubyte * 4 * self.app.kernel_dim ** 2)).contents
            self.image = Image.frombuffer('RGBA', (self.app.kernel_dim, self.app.kernel_dim), pixels, 'raw', 'BGRA', 0, 1).transpose(Image.FLIP_TOP_BOTTOM)
            self.have_image.set()
            glUnmapBuffer(GL_ARRAY_BUFFER)
            glBindBuffer(GL_ARRAY_BUFFER, 0)


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
        info("Start GLUT main loop")

        self.d_timebase = glutGet(GLUT_ELAPSED_TIME)
        glutMainLoop()


    def stop(self):
        ''' Stops the main glut loop '''
        info("Stop GLUT main loop")
        glutDestroyWindow(self.window)
        self.app.exit = True


    def register_callbacks(self, keyboard, mouse, motion):
        ''' Registers input & console callbacks with openGL '''
        info("Registering input callbacks")

        self.keyboard = keyboard
        glutKeyboardFunc(keyboard)
        glutSpecialFunc(keyboard)
        glutMouseFunc(mouse)
        glutMotionFunc(motion)


    def register_console_callbacks(self, render_console, console_keyboard):
        ''' Registers console callbacks '''
        info("Registering console callbacks")

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
        info("Toggle console")

        self.do_main_toggle_console = True


    def toggle_fps(self):
        ''' Toggles the fps display '''
        info("Toggle FPS")

        # toggle fps display
        self.show_fps = not self.show_fps


    def toggle_echo(self):
        ''' Toggles echoing '''

        # toggle echo
        self.app.echo = not self.app.echo

        info("Toggle echo %s", str(self.app.echo))





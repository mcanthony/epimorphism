from common.globals import *
from common.runner import *

from ctypes import *
from OpenGL.GL import *
from OpenGL.GLUT import *

if config.PIL_available:
    import common.glFreeType
FONT_PATH = "/_lib/common/FreeSansBold.ttf"

class Console(object):
    ''' The Console object is responsible for rendering the console in the
        Renderer as well as relaying key events to the Cmdcenter '''

    def __init__(self):
        Globals().load(self)

        # console parameters
        self.console_font_size = 12
        self.max_num_status_rows = 50
        self.status_rows = []
        self.console_width = 600
        self.active_text = ""
        self.cmd_queue = []
        self.queue_idx = -1
        self.cursor_pos = 0

        if(config.is_windows):
            self.font = None
        else:
            self.font = common.glFreeType.font_data(FONT_PATH, self.console_font_size)


    def render_console(self):

        # don't render pbo
        glBindTexture(GL_TEXTURE_2D, 0)
        
        # compute num_rows
        num_rows = min(len(self.status_rows), self.max_num_status_rows)

        # calculate dimensions
        dims = [2.0 * float(self.console_width) / self.app.screen[0],
                2.0 * (10 + (self.console_font_size + 4) * (1 + num_rows)) / float(self.app.screen[0])]

        dims_v = [self.app.screen[0] - self.console_width, 0]

        glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_COMBINE)
        # draw box
        glColor4f(0.15, 0.15, 0.15, 0.75)

        glBegin(GL_QUADS)
        glVertex3f(-1.0, -1.0, 0.1)
        glVertex3f(-1.0 + dims[0], -1.0, 0.1)
        glVertex3f(-1.0 + dims[0], -1.0 + dims[1], 0.1)
        glVertex3f(-1.0, -1.0 + dims[1], 0.1)
        glEnd()

        glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_MODULATE)

        # render active_text
        glColor3ub(0xff, 0xff, 0xff)
        tmp = self.active_text
        self.active_text = self.active_text[0:self.cursor_pos] + '|' + self.active_text[self.cursor_pos:]
        self.font.glPrint(6, 5, self.active_text)
        self.active_text = tmp

        # render status
        for i in range(0, num_rows):
            row = self.status_rows[-(i + 1)]
            if(row[1] == 0):
                glColor3ub(0, 0, 0xff)
            elif(row[1] == 1):
                glColor3ub(0, 0xff, 0)
            elif(row[1] == 2):
                glColor3ub(0xff, 0, 0)
            self.font.glPrint(6, 5 + (4 + self.console_font_size) * (i + 1), row[0])


    def console_keyboard(self, key, x, y):

        # exit
        if(key == "\033"):
            self.cmdcenter.app.exit = True

        # toggle console
        elif(key == "`"):
            self.cmdcenter.interface.renderer.toggle_console()

        # delete character
        elif(key == "\010"): # backspace
            if(self.cursor_pos == 0):
                return
            else:
                self.active_text = self.active_text[:self.cursor_pos-1] + self.active_text[self.cursor_pos:]
                self.cursor_pos -= 1

        # send command
        elif(key == "\015"): # enter
            self.cursor_pos = 0
            self.cmd_queue.append(self.active_text)
            def send_cmd(text):
                response = self.cmdcenter.cmd(text, True, True)
                self.status_rows.append([text, 0])
                for line in response[0].split("\n"):
                    if(line != ""):
                        self.status_rows.append([line, 1])
                for line in response[1].split("\n"):
                    if(line != ""):
                        self.status_rows.append([line, 2])

            if(self.active_text[0:1] == "~"):
                send_cmd(self.active_text[1:])
            else:
                async(lambda : send_cmd(self.active_text))

            self.queue_idx = 0
            self.active_text = ""

        # cycle up through queue
        elif(key == GLUT_KEY_UP):
            if(len(self.cmd_queue) == 0):
                return
            self.queue_idx += 1
            self.queue_idx %= len(self.cmd_queue)
            self.active_text = self.cmd_queue[-(self.queue_idx)]
            self.cursor_pos = len(self.active_text)

        # cycle down through queue
        elif(key == GLUT_KEY_DOWN):
            if(len(self.cmd_queue) == 0):
                return
            self.queue_idx -= 1
            self.queue_idx %= len(self.cmd_queue)
            self.active_text = self.cmd_queue[-(self.queue_idx)]
            self.cursor_pos = len(self.active_text)

        # cursor left
        elif(key == GLUT_KEY_LEFT):
            if(self.cursor_pos != 0):
                self.cursor_pos -= 1

        # cursor right
        elif(key == GLUT_KEY_RIGHT):
            if(self.cursor_pos != len(self.active_text)):
                self.cursor_pos += 1

        # add character to buffer
        else:
            self.active_text = self.active_text[0:self.cursor_pos] + str(key) + self.active_text[self.cursor_pos:]
            self.cursor_pos += 1



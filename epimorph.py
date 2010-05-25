#! /usr/bin/python


import sys
import os
import atexit
import re

import config
config.app = None
from config.structs import *

# define & register exit handler
def exit():
    debug("Running exit handler")

    # remove unclutter
    os.system("killall unclutter")

atexit.register(exit)

# run unclutter to remove mouse pointer
# os.system("unclutter -idle 0.25 -jitter 1 -root&")

# import pygame
# pygame.init()
# print pygame.mouse.set_visible(False)

# create structures
app = App('launch')
config.app = app

# execute command line arguments
for cmd in sys.argv[1:]:
    cmd = cmd.split('=')
    
    if(len(cmd) == 1):
        exec(cmd[0])
    else:
        try:
            val = eval(cmd[1])
        except:
            val = "'" + cmd[1] + "'"

        exec("app.%s=%s" % (cmd[0], val))

from common.globals import *
from noumena.interface import *
from viro.engine import *
from phenom.cmdcenter import *
from common.runner import *

from common.log import *
set_log("EPIMORPH")

info("Starting Epimorphism")
if(len(sys.argv[1:]) != 0):
    debug("with args %s" % (str(sys.argv[1:])))

# encapsulated for asynchronous execution
def main():
    info("Starting main loop")

    # initialize modules
    debug("Initializing modules")    
    interface, engine, cmdcenter = Interface(), Engine(), CmdCenter()
    Globals().init(app, cmdcenter, interface, engine)
    interface.init() and engine.init() and cmdcenter.init()

    # start main loop
    debug("Starting CmdCenter")
    cmdcenter.start()

    info("Main loop completed")
    app.exit = True

    # delete objects
    interface.__del__()
    engine.__del__()
    cmdcenter.__del__()


# start
def start():
    async(main)

# autostart
if(app.autostart):
    start()


#! /usr/bin/python

import sys
import os
import atexit
import re

from globals import *
from config.structs import *
from noumena.interface import *
from viro.engine import *
from phenom.cmdcenter import *
from common.runner import *
from common.log import *

set_log("EPIMORPH")
info("Starting Epimorphism")


# define & register exit handler
def exit():
    debug("Exiting program")

    # remove unclutter
    os.system("killall unclutter")

atexit.register(exit)

# run unclutter to remove mouse pointer
os.system("unclutter -idle 0.25 -jitter 1 -root&")


# create structures
debug("Creating Application")
if(len(sys.argv[1:]) != 0):
    debug("with args %s" % (str(sys.argv[1:])))
app = App()

# execute command line arguments
for cmd in sys.argv[1:]:
    cmd = cmd.split('=')

    try:
        val = eval(cmd[1])
    except:
        val = "'" + cmd[1] + "'"

    exec("app.%s=%s" % (cmd[0], val))


# encapsulated for asynchronous execution
def main():
    info("Starting main loop")

    # initialize modules
    debug("Initializing modules")    
    interface, engine, cmdcenter = Interface(), Engine(), CmdCenter()
    Globals().init(app, app._env, app._context, app._profile, app._state, cmdcenter, interface, engine)
    interface.init() and engine.init() and cmdcenter.init()

    # start main loop
    debug("Starting")
    cmdcenter.start()
    app._env.exit = True
    info("Main loop completed")

    # clean objects
    interface.__del__()
    engine.__del__()
    cmdcenter.__del__()


# start
def start():
    async(main)

# autostart
if(app._env.autostart):
    start()


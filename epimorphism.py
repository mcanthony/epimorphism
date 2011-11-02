#!/usr/bin/python

import sys, atexit
sys.path.append("_lib")
sys.path.append("_lib/sources")

# create configuration objects & execute command line arguments
import config
from common.structs import State
from config.applications import *

# sort arguments
app_names = [arg for arg in sys.argv[1:] if len(arg.split('=')) == 1]
assignments = [arg for arg in sys.argv[1:] if len(arg.split('=')) == 2]

# create app
if(len(app_names) == 0):
    app = config.app = Test()
elif(len(app_names) == 1):
    app = config.app = eval(app_names[0].capitalize() + "()")
elif(len(app_names) == 2):
    app = config.app = eval(app_names[0].capitalize() + "('%s')" % app_names[1])

# create state
state = app.state

for cmd in assignments:
    cmd = cmd.split('=')
    try:
        val = eval(cmd[1])
    except:
        val = eval("'" + cmd[1] + "'")

    if(hasattr(app, cmd[0])):
        setattr(app, cmd[0], val)
    elif(hasattr(state, cmd[0])):
        setattr(state, cmd[0], val)
    else:
        print "failed to parse argument:", cmd

# setup logging
from common.log import *
set_log(app.name.upper())

info("STARTING " + app.name)
if(len(sys.argv) != 1):
    debug("with args %s" % (str(sys.argv[1:])))


# define & register exit handler
def exit():
    debug("Running exit handler")
atexit.register(exit)


# create main application objects & initialize globals
from common.globals import Globals
from interface.interface import Interface
from engine.engine import Engine
from cmdcenter.cmdcenter import CmdCenter
from common.runner import *


def main():
    info("Starting main loop")

    # initialize modules
    debug("Initializing modules")    
    interface, engine, cmdcenter = Interface(), Engine(), CmdCenter()
    Globals().init(app, state, cmdcenter, interface, engine)
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


def start():
    async(main)


if(app.autostart):
    start()


#!/usr/bin/env python

import sys, atexit
sys.path.insert(1, "_lib/sources")
sys.path.append("_lib")

# setup logging
from common.log import *
set_log("EPIMORPHISM", logging.DEBUG)

info("STARTING")
if(len(sys.argv) != 1):
    info("with args %s" % (str(sys.argv[1:])))

# create configuration objects & execute command line arguments
from common.structs import State
from config.applications import *

# sort arguments
app_names = [arg for arg in sys.argv[1:] if len(arg.split('=')) == 1]
assignments = [arg for arg in sys.argv[1:] if len(arg.split('=')) == 2]

# create app
if(len(app_names) == 0):
    app = Epimorphism()
elif(len(app_names) == 1):
    app = eval(app_names[0].capitalize() + "()")
elif(len(app_names) == 2):
    app = eval(app_names[0].capitalize() + "('%s')" % app_names[1])

# parse additional cmd line assignments
for cmd in assignments:
    cmd = cmd.split('=')
    try:
        val = eval(cmd[1])
    except:
        val = eval("'" + cmd[1] + "'")

    if(hasattr(app, cmd[0])):
        setattr(app, cmd[0], val)
    elif(hasattr(app.state, cmd[0])):
        setattr(app.state, cmd[0], val)
    else:
        print "failed to parse argument:", cmd

# create main application objects & initialize globals
from common.globals import Globals
from interface.interface import Interface
from engine.engine import Engine
from cmdcenter.cmdcenter import CmdCenter
from common.runner import *

def main():
    info("Starting main loop")

    # initialize modules
    info("Initializing modules")    
    interface, engine, cmdcenter = Interface(), Engine(), CmdCenter()
    Globals().init(app, app.state, cmdcenter, interface, engine)
    interface.init() and engine.init() and cmdcenter.init()

    # start main loop
    info("Starting CmdCenter")
    cmdcenter.start()

    info("Main loop completed")
    app.exit = True

    # delete objects
    #del interface, engine, cmdcenter
    interface.__del__()
    engine.__del__()
    cmdcenter.__del__()

def start():
    async(main)

if(app.autostart):
    start()

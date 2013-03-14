#!/usr/bin/env python

import sys, os
sys.path.append("_lib/sources")
sys.path.append("_lib")

# add location of dlls to path if windows
if sys.platform == "win32":
    if 'PROGRAMFILES(X86)' in os.environ:  # 64 bit windows
        os.environ['PATH'] = '_lib/sources/win64' + ';' + os.environ['PATH']
    else:
        os.environ['PATH'] = '_lib/sources/win32' + ';' + os.environ['PATH']

# test for availability of PIL
import config
try: 
    import PIL
    config.PIL_available = True 
except ImportError: 
    config.PIL_available = False 

# setup logging
from common.log import *
set_log("EPIMORPHISM", logging.WARNING)

info("STARTING")
if(len(sys.argv) != 1):
    info("with args %s" % (str(sys.argv[1:])))

# create configuration objects & execute command line arguments
from common.structs import State
from config.applications import *

# sort arguments
app_names = [arg for arg in sys.argv[1:] if len(arg.split('=')) == 1]
assignments = [arg for arg in sys.argv[1:] if len(arg.split('=')) == 2]

# create new application if requested
from config.generator import *
if len(app_names) == 2 and app_names[0] == "generate":
    generate_application(app_names[1])
    print "%s application successfully generated\nMain kernel file is kernels/%s.cl" % (app_names[1].capitalize(), app_names[1])
    sys.exit(0)

# create app
if(len(app_names) == 0):
    print "Choose an application:"
    app_names = [app.__name__ for app in App.__subclasses__()]
    app_names.sort()
    for i, app in enumerate(app_names):
        print "%d: %s" % (i+1, app)
    input = raw_input('> ')
    if(input == ""):
        i = 1
    else:
        i = int(input)
    app = eval(app_names[i - 1].capitalize())()
    app_name = app.__class__.__name__.lower()
    state_names = sorted([filename[len(app_name) + 1:-4] for filename in os.listdir("config/state") if filename.startswith(app_name)])
    if len(state_names) != 1:
        print "Choose a preset"
        for i, state in enumerate(state_names):
            print "%d: %s" % (i+1, state)
        input = raw_input('> ')
        if(input == ""):
            i = 1
        else:
            i = int(input)
    else:
        i = 1
    app.state = State(app_name, state_names[i - 1])
elif(len(app_names) == 1):
    app = eval(app_names[0].capitalize())()
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
    Globals().init(cmdcenter, interface, engine)
    interface.init() and engine.init() and cmdcenter.init()

    # start main loop
    info("Starting CmdCenter")
    cmdcenter.start()

    info("Main loop completed")

def start():
    main()

if(app.autostart):
    start()

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

# debug messages
debug("Initializing state/profile/context/env")
if(len(sys.argv[1:]) != 0):
    debug("with args %s" % (str(sys.argv[1:])))

cmd = []
app_name = "default"
# parse command line arguments
for arg in sys.argv[1:]:

    # application
    split = re.compile("=").split(arg)
    if(len(split) == 1):
        app_name = arg
        continue
    else:
        cmd.append(arg)

# create structures
debug("Creating Data Structures")
app     = App(app_name)
env     = Environment(app._env) 
profile  = Profile(app._profile) 
context = Context(app._context) 
state   = State(app._state) 



#configmanager.merge_with_default("app", args["application"], **args["app"])
#env     = configmanager.merge_with_default("environment", app._env, **args["env"].merge)
#context = configmanager.merge_with_default("context", app._context, **args["context"])
#profile = configmanager.merge_with_default("profile", app._profile, **args["profile"])
#state   = configmanager.merge_with_default("state", app._state, **args["state"])

# encapsulated for asynchronous execution
def main():
    info("Starting main loop")

    # initialize modules
    debug("Initializing modules")    

    interface, engine, cmdcenter = Interface(), Engine(), CmdCenter()
    Globals().init(app, env, context, profile, state, cmdcenter, interface, engine)
    interface.init() and engine.init() and cmdcenter.init()

    # start main loop
    debug("Starting")
    cmdcenter.start()
    env.exit = True
    info("Main loop completed")

    # clean objects
    interface.__del__()
    engine.__del__()
    cmdcenter.__del__()

# start
def start():
    async(main)

# autostart
if(env.autostart):
    start()


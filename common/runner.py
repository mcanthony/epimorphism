import threading

from common.log import *
set_log("RUNNER")

class Runner(threading.Thread):
    ''' A runner object spawns a new thread to call a function '''

    def __init__(self, func, s):
        debug("init " + s)
        if(s == 'shiz'):
            debug("returning")
            return
        self.func = func

        debug("ASD " + str(func))
        # init thread
        threading.Thread.__init__(self)


    def run(self):

        # call func
        self.func()


def async(func, s):
    print "as1"
    # create and start thread
    Runner(func, s).start()
    print "as2"


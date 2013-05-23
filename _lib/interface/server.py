#!/usr/bin/env python

# geneServer.py
#
# mvr adapted from http://twistedmatrix.com/documents/current/core/examples/echoserv.py
#              and geneServer.original.py

import config
if(config.app and config.app.server):

    from common.globals import *

    from twisted.internet.protocol import Protocol, Factory
    from twisted.internet import reactor

    from common.runner import *
    from common.log import *
    set_log("SERVER")

    global cmdcenter

    # define helpers
    def get_val(x):       return x
    def set_val(x, y):    return y
    def get_radius(z):    return r_to_p(z)[0]
    def set_radius(z, r): return p_to_r([r, r_to_p(z)[1]])
    def get_th(z):        return r_to_p(z)[1]
    def set_th(z, th):    return p_to_r([r_to_p(z)[0], th])

    import math
    from common.complex import *

    class Echo(Protocol):
        def dataReceived(self, data):
            """
            As soon as any data is received, write it back.
            """

            # execute command
            # info("executing: %s" % data.strip())
            # res = cmdcenter.cmd(data.strip(), True, True)
            # send response
            #self.transport.write(str(res) + "\r\n")
            
            for cmd in [e for e in data.split("\n\n\n") if e]:
                self.parseMidi(cmd) 

        def parseMidi(self, cmd):
            print [elem.encode("hex") for elem in cmd]
            if(ord(cmd[0]) == 176):
                channel = ord(cmd[1])
                if(len(cmd) == 2):
                    return
                val = ord(cmd[2])
                
                if(val == 1):
                    val = 0
                    
                f = val / 128.0
                if(val == 127.0): f = 1.0

                # switich time
                if(channel == 1):                        
                    spb = 60.0 / cmdcenter.state.bpm
                    mult = -4 + math.floor(f * 8)
                    print "set mult ", mult
                    cmdcenter.app.state_intrp_time = cmdcenter.app.midi_speed = spb * (2 ** mult)
                # zn                    
                elif(channel <= 50):
                    is_r = (channel % 2 == 0)
                    channel = (channel - 2) / 2
                    old = cmdcenter.get_val('state.zn', channel)
                    if(is_r):
                        f = f * 4.0;
                        val = set_radius(old, f)
                    else:
                        f = f * 2.0 * math.pi;
                        val = set_th(old, f)

                    print "set z", channel, r_to_p(val), f
                    cmdcenter.radial_2d('zn', channel, cmdcenter.app.midi_speed, r_to_p(old), r_to_p(val))
                        
                


    class Server(object):
        def __init__(self):
            Globals().load(self)

            global cmdcenter
            cmdcenter = self.cmdcenter

            f = Factory()
            f.protocol = Echo
            reactor.listenTCP(8563, f)

        def go(self):
            global cmdcenter
            while(not cmdcenter.app.exit):
                reactor.iterate()


        def start(self):
            async(self.go)















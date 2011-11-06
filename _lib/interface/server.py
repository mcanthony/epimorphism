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

    class Echo(Protocol):
        def dataReceived(self, data):
            """
            As soon as any data is received, write it back.
            """

            # execute command
            info("executing: %s" % data.strip())
            res = cmdcenter.cmd(data.strip(), True)
            # send response
            self.transport.write(str(res) + "\r\n")


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

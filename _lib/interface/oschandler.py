from common.globals import *

from common.runner import * 
from common.log import *
set_log("OSC")

import socket, threading, re
import OSC

class OSCHandler(threading.Thread):

    def __init__(self):
        debug("Initializing OSC server")

        Globals.load(self)            

        # initialize component list
        self.components = self.cmdcenter.componentmanager.component_list()

        # ghetto way to get ip address
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("gmail.com",80))
        ip = s.getsockname()[0]
           
        # create server & client
        self.server = OSC.OSCServer((ip, self.app.OSC_input_port))
        self.client = OSC.OSCClient()    

        # add address handlers
        for func in dir(self):
            if(func [0:4] == 'hnd_'):
                self.server.addMsgHandler('/' + func[4:], getattr(self, func))

        for (regex, func) in iter(sorted(self.regex_callbacks.iteritems())):
            self.server.addMsgHandler(re.compile(regex), func)

        #initialize thread
        threading.Thread.__init__(self)


    def run(self):            
        if(self.app.OSC_echo):
            debug("Sending defaults to OSC device")
            self.mirror_all()
        while(not self.cmdcenter.app.exit):
            self.server.handle_request()
            

    def _send(self, addr, args):
        msg = OSC.OSCMessage()
        msg.setAddress(addr)
        for arg in args:
            msg.append(arg)
            #try:
            self.client.sendto(msg, self.app.OSC_client_address)
            #except OSC.OSCClientError:
            #    debug("couldn't connect to OSC client")


    def mirror_all(self):
        for name in self.state.par_names:
            self.mirror(self.state.par, self.state.par_idx(name), self.state.get_par(name))
        for i in xrange(len(self.state.zn)):
            self.mirror(self.state.zn, i, self.state.zn[i])
        for (k,v) in  iter(sorted(self.state.components.iteritems())):
            self.mirror(self.state.components, k, v)


    def mirror(self, obj, key, val):
        pass

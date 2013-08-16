from common.globals import *

from common.runner import * 
from common.log import *
set_log("OSC")

import socket, threading, re, time
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

        for regex, func in self.regex_callbacks.items():
            self.server.addMsgHandler(re.compile(regex), func)

        self.msg_bundle = None

        #initialize thread
        threading.Thread.__init__(self)


    def run(self):            
        if(self.app.OSC_echo):
            debug("Sending defaults to OSC device")
            self.mirror_all()
        while(not self.cmdcenter.app.exit):
            self.server.handle_request()
            

    def _send(self, addr, args, bundle = False):
        if(bundle and not self.msg_bundle):
            self.msg_bundle = OSC.OSCBundle()
        msg = OSC.OSCMessage()
        msg.setAddress(addr)

        for arg in args:
            msg.append(arg)
            

        if(bundle or self.msg_bundle):
            self.msg_bundle.append(msg)

        if(not bundle):
            try:
                self.client.sendto(self.msg_bundle or msg, self.app.OSC_client_address)
            except OSC.OSCClientError:
                debug("couldn't connect to OSC client")
            
            if(self.msg_bundle):
                self.msg_bundle = None


    def mirror_all(self):
        pass


    def mirror(self, obj, key, val):
        pass

import config
if(config.app and config.app.midi_enabled):
    from common.globals import *

    import threading
    import pypm
    import re

    import time

    from common.complex import *
    from noumena.setter import *

    from noumena.mididevices import *

    from common.log import *
    set_log("MIDI")


    class MidiHandler(threading.Thread):
        ''' The MidiHandler object is a threaded object that handles midi input
        events and that sends midi output information '''


        def __init__(self):
            Globals().load(self)

            # find devices - MAYBE A BIT FLAKEY
            for i in range(pypm.CountDevices()):

                interf,name,inp,outp,opened = pypm.GetDeviceInfo(i)
                if(not re.compile("Midi Through Port|TiMidity").search(name)):
                    debug("ID: %d INTERFACE: %s NAME: %s %s OPENED? %s" % (i, interf, name, (inp == 1 and "INPUT" or "OUTPUT"), str(opened)))

                if(re.compile(self.context.midi_controller[0]).search(name) and inp == 1):
                    self.input_device = i
                    break

                if(re.compile(self.context.midi_controller[0]).search(name) and outp == 1):
                    self.output_device = i

            # open devices
            try:
                self.midi_in = pypm.Input(self.input_device)
                self.midi_out = pypm.Output(self.output_device, 10)
                info("Found MIDI device")
            except:
                self.midi_in = None
                self.midi_out = None
                info("MIDI device not found")
                self.app.midi_enabled = False

            # set default bindings
            self.binding_idx = 0

            # load bindings
            self.load_bindings()

            # init thread
            threading.Thread.__init__(self)


        def load_bindings(self):
            ''' Loads bindings '''
            debug("Loading bindings")

            self.bindings = eval(self.context.midi_controller[1])

            # send defaults
            self.send_bindings()


        def output_binding(self, binding_id):
            ''' Evaluates and outputs value of a binding '''

            binding = self.bindings[self.binding_idx][binding_id]

            f = ((eval("get_" + binding[2])(self.cmdcenter.get_val(binding[0], eval(binding[1])))) - binding[3][1]) / binding[3][0]

            self.writef(binding_id[0], binding_id[1], f)


        def mirror(self, obj, key):
            ''' Echos a change in obj to a midi controller'''

            # lookup bindings
            bindings = self.bindings[self.binding_idx]

            # send correct binding - a bit weird
            for binding_id, binding in bindings.items():
                if(eval("self.cmdcenter.%s" % binding[0]) == obj and eval(binding[1]) == key):
                    self.output_binding(binding_id)


        def send_bindings(self):
            ''' Send all bindings to midi controller '''

            # lookup bindings
            bindings = self.bindings[self.binding_idx]

            # send all bindings
            for binding_id in bindings:
                self.output_binding(binding_id)

            # send binding buttons - HACK: for switching bindings
            for i in xrange(0, 8):
                self.writef(0, 65 + i, 0.0)
                if(self.binding_idx == i) : self.writef(0, 65 + i, 1.0)


        def writef(self, bank, channel, f):
            ''' Write a value out '''

            # return if midi output disabled
            if(not self.context.midi_output):
                return

            # get val
            val = int(f * 128.0)
            if(val == 128): val = 127

            # send
            if(self.midi_out):
                self.midi_out.Write([[[176 + bank, channel, val, 0], pypm.Time()]])


        def run(self):
            ''' Main execution loop '''

            # run loop
            while(True and self.app.midi_enabled):

                # sleep / exit
                while(not self.midi_in.Poll() and not self.cmdcenter.app.exit):
                    time.sleep(0.01)
                if(self.cmdcenter.app.exit) : exit()

                if(len(self.state.scripts) != 0):
                    self.state.paths=[]
                    self.state.scripts=[]
                self.context.last_midi_event = self.cmdcenter.time()

                # read
                data = self.midi_in.Read(1)

                # set vars
                bank = data[0][0][0] % 16
                channel = data[0][0][1]
                val = data[0][0][2]

                # get f
                f = val / 128.0
                if(val == 127.0) : f = 1.0

                # print "MIDI", bank, channel, val, f
                # print self.state.par[self.state.par_names.index("_COLOR_BASE_PHI")]
                # check bindings
                bindings = self.bindings[self.binding_idx]
                if(bindings.has_key((bank, channel))):
                    binding = bindings[(bank, channel)]

                    # compute & output value
                    f = binding[3][0] * f + binding[3][1]

                    old = self.cmdcenter.get_val(binding[0], eval(binding[1]))
                    val = eval("set_" + binding[2])(old, f)
                    #print old, val, str(binding[1])
                    # HACK to smoothen valuesx
                    if(binding[2] == "radius" or binding[2] == "th"):
                        self.cmdcenter.radial_2d('state.zn', eval(binding[1]), self.cmdcenter.interface.context.midi_speed, r_to_p(old), r_to_p(val))
                    else:
                        self.cmdcenter.linear_1d('state.par', eval(binding[1]), self.cmdcenter.interface.context.midi_speed, old, val)


                # change bindings - sortofHACK: buttons switch bindings

                elif(channel >= 65 and channel <= 72):

                    self.binding_idx = (channel - 65) % len(self.bindings)
                    if val == 0 : self.binding_idx = 0
                    self.send_bindings()

#                elif(channel >= 33 and channel <= 40):
#
#                    self.binding_idx = (channel - 33) % len(self.bindings)
#
#                    self.send_bindings()


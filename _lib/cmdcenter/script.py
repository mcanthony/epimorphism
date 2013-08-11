import config

from common.globals import *
from program import Program
from common.structs import * 
from common.runner import *
from common.complex import *

from common.log import *
set_log("SCRIPT")

import time, copy, os

class ScriptParseError(Exception):
    """Exception raised script parsing errors."""

    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg

class Script(DictObj, Program):
    ''' Contains a timestamped sequence of commands which are executed in the Cmd environment '''

    def __init__(self, app=None, name = "default"):
        info("Creating script")
        self.extension = "scr"
        Program.__init__(self, None)
        
        DictObj.__init__(self, "script", app, name)
        self.repr_blacklist += ["exit", "sleep_event", "freeze_event", "next_event_in"]


    def _execute(self):
        ''' Internal execution loop '''

        if(len(self.data["events"]) == 0):
            self.state.programs.remove(self)
            self.exit = True
            return

        self.next_event_in = self.data["events"][0]["time"] + self.data["phase"] - self.cmdcenter.time()

        if(self.next_event_in > 0):
            return

#        print self.data["events"].pop(0)["cmd"]
        async(lambda: self.cmdcenter.cmd(self.data["events"].pop(0)["cmd"], False))
        #self.cmdcenter.cmd(self.data["events"].pop(0)["cmd"], False)


    def add_event(self, time, cmd):
        ''' Add an event to the collection of events '''
        info("Adding event at %f" % time)

        # compute insertion index
        lst = [(i == 0 or time >= self.data["events"][i-1]["time"])
               and (i >= len(self.data["events"]) or time <= self.data["events"][i]["time"])
               for i in xrange(len(self.data["events"]) + 1)]
        idx = lst.index(True)

        # insert event
        self.data["events"].insert(idx, {"time": time, "cmd": cmd})


    def last_event_time(self):
        ''' Returns the time of the last event '''

        return self.data["events"][-1]["time"]


    def push(self, time, cmd):
        ''' Push an event to the top of the stack '''

        self.data["events"].append({"time":time, "cmd":cmd})

        
class BeatScript(Script):
    ''' Contains a timestamped sequence of commands which are executed in the Cmd environment, where the timestamps are specified by in terms of beats'''

    def __init__(self, app=None, name = "default"):
        info("Creating beat script")

        try:
            with open("config/script/%s_%s.bscr" % (app, name)) as f:
                contents = [line for line in f.readlines() if line[0] != '#']
        except Exception as e:
            raise ScriptParseError("couldn't find script %s.bscr" % name)

        # get bpm
        bpm = float(contents.pop(0).replace("bpm", ""))
        spb = 60.0 / bpm

        # speed parse func
        def parse_spd(spd):
            if spd == "0":
                return 0            
            suf = spd[-1]
            if suf == "W":
                m1 = 4.0 * spb
            elif suf == "H":
                m1 = 2.0 * spb;
            elif suf == "Q":
                m1 = 1.0 * spb;
            elif suf == "E":
                m1 = 0.5 * spb;
            elif suf == "S":
                m1 = 0.25* spb;
            elif suf == "T":
                m1 = 1.0 / 3.0 * spb;                            
                
            m2 = int(spd[0:-1])

            return m1 * m2
            
        
        # parse events
        events = [{'cmd':"state.bpm = %f" % bpm, 'time':0.0},
                  {'cmd':"state.t_speed = 1.0", 'time':0.0}]
        
        for line in contents:
            components = line.split()

            #parse t
            t = components.pop(0)
            sections = t.split('.')            
            t = spb * (4 * int(sections[0]) + int(sections[1]) + int(sections[2]) / (10.0 ** len(sections[2])))
            
            # parse event
            cmd = components.pop(0)
            if cmd == "do":
                cmd = components.pop(0)
                events.append({'cmd':cmd, 'time':t})
            elif cmd == "switch":
                cmd = "switch_component('%s', '%s')" % (components.pop(0), components.pop(0))
                spd = parse_spd(components.pop())
                events.append({'cmd':'app.state_intrp_time=%s' % spd, 'time':t})                                                
                events.append({'cmd':cmd, 'time':t})
            elif cmd == "tex":
                spd = parse_spd(components.pop())
                cmd = "run_program(SwitchAux({'idx': %s, 'tex': '%s'}))" % (components.pop(0), components.pop(0))
                events.append({'cmd':'app.state_intrp_time=%s' % spd, 'time':t})                                                
                events.append({'cmd':cmd, 'time':t})
            elif cmd == "zn":

                idx = components.pop(0)
                path_type = components.pop(0)
                start = "r_to_p(state.zn[%s])" % idx                
                end = components.pop(0)
                spd = parse_spd(components.pop(0))
                if path_type == "rad":
                    cmd = "state.paths.append(Radial2D('zn', %s, %f, {'s':%s, 'e':r_to_p(complex(%s))}))" % (idx, spd, start, end)
                elif path_type == "rads":
                    cmd = "state.paths.append(Radial2DSmooth('zn', %s, %f, {'s':%s, 'e':r_to_p(complex(%s))}))" % (idx, spd, start, end)                    
                events.append({'cmd':cmd, 'time':t})                                                                    
            elif cmd == "par":
                name = components.pop(0)
                idx = components.pop(0)
                path_type = components.pop(0)
                start = "state.par['%s'][%s]" % (name, idx)
                end = components.pop(0)
                spd = parse_spd(components.pop(0))
                if path_type == "lin":
                    cmd = "state.paths.append(Linear1D(\"par['%s']\", %s, %s, {'s':%s, 'e':%s, 'loop':False}))" % (name, idx, spd, start, end)
                elif path_type == "lins":
                    cmd = "state.paths.append(Linear1DSmooth(\"par['%s']\", %s, %s, {'s':%s, 'e':%s, 'loop':False}))" % (name, idx, spd, start, end)                    
                events.append({'cmd':cmd, 'time':t})
            elif cmd == "save_fog":
                block = int(sections[0]) / 16
                cmd = "execute_paths();state.audio_block=%d;state.programs=[];state.save('fog%d')" % (block, block)
                events.append({'cmd':cmd, 'time':t})
                
                     
        # copy template data
        template = Script(app, "default")
        self.__dict__ = template.__dict__        
        self.extension = "bscr"
        self.name = name

        self.data['events'] = events

        print self.__dict__





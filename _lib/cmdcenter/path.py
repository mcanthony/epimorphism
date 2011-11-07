from common.globals import *

from cmd.paths import *

from common.log import *
set_log("Path")

class Path(object):


    def __init__(self, type, obj, idx, phase, start, spd, **vars):
        self.data_keys = vars.keys()
        self.type, self.obj, self.idx, self.phase, self.start, self.spd = type, obj, idx, phase, start, spd
        self.__dict__.update(vars)
        

    def execute(self, t):
        (res, status) = eval(self.type)(self, t)

        # set result
        if(self.obj):
            eval('config.%s' % self.obj)[self.idx] = res

        return status


    def __repr__(self):
        return "Path('%s', %s, %s, %f, %f, %f, %s)" % (self.type, self.obj and ("'" + self.obj + "'") or "None", self.idx or "None", self.phase, self.start, self.spd, str(self.data_keys))

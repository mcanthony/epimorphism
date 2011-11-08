from common.globals import *

from cmd.paths import *

from common.log import *
set_log("Path")

class Path(object):


    def __init__(self, type, obj, idx, phase, start, spd, vars):
        self.data_keys = vars.keys()
        self.type, self.obj, self.idx, self.phase, self.start, self.spd = type, obj, idx, phase, start, spd
        try:
            self.idx = int(self.idx)
        except:
            pass
        #print self.obj, self.idx, str(self)
        self.__dict__.update(vars)
        

    def execute(self, t):
        (res, status) = eval(self.type)(self, t)

        # set result
        if(self.obj):
            eval('config.%s' % self.obj)[self.idx] = res

        return status


    def __repr__(self):
        vars = dict((k, getattr(self, k)) for k in self.__dict__.keys() if k in self.data_keys)
        return "Path('%s', '%s', '%s', %f, %f, %f, %s)" % (self.type, str(self.obj), str(self.idx), self.phase, self.start, self.spd, str(vars))

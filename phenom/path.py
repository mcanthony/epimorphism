from aeon.datapath import *

from common.log import *
set_log("Path")

class Path(object):


    def __init__(self, type, obj, idx, phase, start, spd, data, cmdcenter):
        self.type, self.obj, self.idx, self.phase, self.start, self.spd, self.data, self.cmdcenter = type, obj, idx, phase, start, spd, data, cmdcenter


    def execute(self, t):
        (res, status) = eval(self.type)(self, self.phase + t, self.data)

        # set result
        if(self.obj):
            self.cmdcenter.set_val(res, self.obj, self.idx)

        return status

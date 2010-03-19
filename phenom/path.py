from aeon.datapath import *

from common.log import *
set_log("Path")

class Path(object):


    def __init__(self, type, obj, idx, start, spd, data):
        self.type, self.obj, self.idx, self.start, self.spd, self.data = type, obj, idx, start, spd, data


    def execute(self, t):
        return eval(self.type)(t, self.data)

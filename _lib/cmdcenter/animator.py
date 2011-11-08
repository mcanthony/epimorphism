import config

from path import *

from cmd.paths import *

from common.log import *
set_log("ANIMATOR")

class Animator(object):
    ''' The Animator class is a module for Cmdcenter that is
        responsible for automation of data. '''


    # helpers
    def radial_2d(self, obj, idx, spd, z0, z1):
        ''' Helper function for creating radial_2d paths. '''
        return Radial2D(obj, idx, spd, {"s" : z0, "e" : z1})


    def linear_1d(self, obj, idx, spd, x0, x1):
        ''' Helper function for creating linear_1d paths. '''
        return Linear1D(obj, idx, spd, {"s" : x0, "e" : x1})


    # do execution
    def execute_paths(self):

        # get time
        t = config.cmdcenter.time()

        # execute paths traverse list backward, in case we need to r
        for path in config.state.paths[::-1]:

            # execute path
            (res, status) = path.do((t - path.phase) / path.spd) 

            # set result
            getattr(config.state, path.obj)[path.idx] = res

            # if necessary, remove path
            if(not status):
                config.state.paths.remove(path)





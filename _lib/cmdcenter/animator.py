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
        #debug("Radial 2d: %s %s %s %s %s", obj, idx, spd, str(z0), str(z1))
        return Radial2D(obj, idx, spd, {"s" : z0, "e" : z1})


    def linear_1d(self, obj, idx, spd, x0, x1):
        ''' Helper function for creating linear_1d paths. '''
        #debug("Linear 1d: %s %s %s %s %s", obj, idx, spd, x0, x1)

        return Linear1D(obj, idx, spd, {"s" : x0, "e" : x1})


    # do execution
    def execute_paths(self):

        # get time
        t = config.cmdcenter.time()

        # execute paths traverse list backward, in case we need to r
        for path in self.state.paths[::-1]:

            # execute path
            (res, status) = path.do((t - path.phase) / path.spd) 

            # set result
            getattr(config.state, self.obj)[self.idx] = res

            # if necessary, remove path
            if(not status):
                self.state.paths.remove(path)





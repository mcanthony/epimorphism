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

        path = Radial2D(obj, idx, spd, {"s" : z0, "e" : z1})

        # remove any previously existing paths for these vars
        [p.stop() for p in config.state.paths if (path.obj, path.idx) == (p.obj, p.idx)]

        # add path to state
        config.state.paths.append(path)

        return path


    def linear_1d(self, obj, idx, spd, x0, x1):
        ''' Helper function for creating linear_1d paths. '''

        path = Linear1D(obj, idx, spd, {"s" : x0, "e" : x1})

        # remove any previously existing paths for these vars
        [p.stop() for p in config.state.paths if (path.obj, path.idx) == (p.obj, p.idx)]

        # add path to state
        config.state.paths.append(path)

        return path


    # do execution
    def execute_paths(self):

        # get time
        t = config.cmdcenter.time()

        # execute paths traverse list backward, in case we need to remove one
        for path in config.state.paths[::-1]:

            # execute path
            (res, status) = path.do((t - path.phase) / path.spd) 

            # set result
            #getattr(config.state, path.obj)[path.idx] = res
            eval("config.state." + path.obj)[path.idx] = res
            

            # if necessary, remove path
            if(not status):
                path.stop()





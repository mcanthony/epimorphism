from phenom.path import *

from common.log import *
set_log("ANIMATOR")

class Animator(object):
    ''' The Animator class is a module for Cmdcenter that is
        responsible for automation of data. '''


    def __init__(self):
        pass


    def radial_2d(self, obj, idx, spd, z0, z1):
        ''' Helper function for creating radial_2d paths. '''
        debug("Radial 2d: %s %s %s %s %s", obj, idx, spd, str(z0), str(z1))

        return self.animate_var("radial_2d", obj, idx, spd, {"s" : z0, "e" : z1}, None)


    def linear_1d(self, obj, idx, spd, x0, x1):
        ''' Helper function for creating linear_1d paths. '''
        debug("Linear 1d: %s %s %s %s %s", obj, idx, spd, x0, x1)

        return self.animate_var("linear_1d", obj, idx, spd, {"s" : x0, "e" : x1}, None)


    def animate_var(self, type, obj, idx, spd, data, exclude="Exclude"):
        ''' Adds a path to the animator. '''

        if(not data.has_key("loop")): data["loop"] = False

        active_paths = filter(lambda path: path.obj == obj and path.idx == idx, self.state.paths)
        if(len(active_paths) == 1):
            active_path = active_paths[0]

            # if Exclude, don't add another path 
            if(exclude == "Exclude"):
                return False

            self.state.paths.remove(active_path)            

        if(obj):
            eval("self."+obj).midi_echo = False

        # add path
        path = Path(type, obj, idx, 0.0, self.time(), spd, **data)
        self.state.paths.append(path)

        return path


    def execute_paths(self):

        # get time
        t = self.time()

        # execute paths
        for path in self.state.paths[::-1]:

            # initialize path if necessary
            if(not path.globals_initialized):
                path.initialize_globals()

            # execute path
            status = path.execute((t + path.phase - path.start) / path.spd)

            # if necessary, remove path
            if(not status):
                self.state.paths.remove(path)





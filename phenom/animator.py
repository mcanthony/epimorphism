from phenom.path import *

from common.log import *
set_log("ANIMATOR")

class Animator(object):
    ''' The Animator class is a module for Cmdcenter that is
        responsible for automation of data. '''


    def __init__(self):
        self.paths = []


    def radial_2d(self, obj, idx, spd, z0, z1):
        ''' Helper function for creating radial_2d paths. '''
        debug("Radial 2d: %s %s %s %s %s", obj, idx, spd, str(z0), str(z1))

        return self.animate_var("radial_2d", obj, idx, spd, {"s" : z0, "e" : z1}, "Overwrite")


    def linear_1d(self, obj, idx, spd, x0, x1):
        ''' Helper function for creating linear_1d paths. '''
        debug("Linear 1d: %s %s %s %s %s", obj, idx, spd, x0, x1)

        return self.animate_var("linear_1d", obj, idx, spd, {"s" : x0, "e" : x1}, "Overwrite")


    def animate_var(self, type, obj, idx, spd, data, exclude="Exclude"):
        ''' Adds a path to the animator. '''

        # obj.midi_echo = False
        eval("self." + obj).midi_echo = False

        if(not data.has_key("loop")): data["loop"] = False

        active_paths = filter(lambda path: path.obj == obj and path.idx == idx, self.paths)

        # if Exclude, don't add another path if one exists
        if(exclude == "Exclude" and len(active_paths) != 0):
            return False

        # if Overwrite, remove existing path
        if(exclude == "Overwrite"):
            self.remove_paths(obj, idx);
            eval("self."+obj).midi_echo = False

        # add path
        path = Path(type, obj, idx, self.time(), spd, data)
        self.paths.append(path)

        return path


    def remove_paths(self, obj, idx):
        ''' Removes all paths for obj[idx] '''

        active_paths = filter(lambda path: path.obj == obj and path.idx == idx, self.paths)
        for path in active_paths:
            self.paths.remove(path)


        eval("self."+obj).midi_echo = False


    def execute_paths(self):

        # get time
        t = self.time()

        # execute paths
        for path in self.paths[::-1]:

            # execute path
            (res, status) = path.execute((t - path.start) / path.spd)

            # set result
            self.set_val(res, path.obj, path.idx)

            # if necessary, remove path
            if(not status):
                self.remove_paths(path.obj, path.idx)





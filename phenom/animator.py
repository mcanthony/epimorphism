from aeon.datapath import *

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

        self.animate_var("radial_2d", obj, idx, spd, {"s" : z0, "e" : z1}, "Overwrite")


    def linear_1d(self, obj, idx, spd, x0, x1):
        ''' Helper function for creating linear_1d paths. '''
        debug("Linear 1d: %s %s %s %s %s", obj, idx, spd, x0, x1)

        self.animate_var("linear_1d", obj, idx, spd, {"s" : x0, "e" : x1}, "Overwrite")


    def animate_var(self, type, obj, idx, speed, data, exclude="Exclude"):
        ''' Adds a path to the animator. '''

        # obj.midi_echo = False
        eval("self." + obj).midi_echo = False

        key = {"obj":obj, "idx":idx}

        if(not data.has_key("loop")): data["loop"] = False

        active_paths = filter(lambda x: x[0] == key, self.paths)

        # if Exclude, don't add another path if one exists
        if(exclude == "Exclude" and len(active_paths) != 0):
            return False

        # if Overwrite, remove existing path
        if(exclude == "Overwrite"):
            self.remove_paths(obj, idx);
            eval("self."+obj).midi_echo = False

        # add path
        self.paths.append((key, {"start": self.time(), "speed": speed, "func":(lambda t: eval(type)(t, data))}))

        return True


    def remove_paths(self, obj, idx):
        ''' Removes all paths for obj[idx] '''

        key = {"obj":obj, "idx":idx}
        active_paths = filter(lambda x: x[0] == key, self.paths)
        for path in active_paths:
            self.paths.remove(path)


        eval("self."+obj).midi_echo = False


    def execute_paths(self):

        # get time
        t = self.time()

        # execute paths
        for path in self.paths[::-1]:

            # execute path
            (res, status) = path[1]["func"]((t - path[1]["start"]) / path[1]["speed"])

            # set result
            # path[0]["obj"][path[0]["idx"]] = res
            self.set_val(res, path[0]["obj"], path[0]["idx"])

            # if necessary, remove path
            if(not status):
                self.remove_paths(path[0]["obj"], path[0]["idx"])

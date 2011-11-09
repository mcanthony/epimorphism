from common.globals import *

from datamanager import *

import time, random

from common.log import *
set_log("COMPONENT")


class ComponentManager(object):


    def __init__(self):
        Globals().load(self)

        self.switching_components = False
        self.compiling = False

        # start datamanager
        self.datamanager = DataManager()


    def component_list(self):
        ''' Returns a list of components '''

        return self.datamanager.component_names


    def print_components(self):
        ''' Prints the currently listed components '''

        keys = self.datamanager.component_names

        # print components
        for i in xrange(len(keys)) :
            component = self.state.components[keys[i]]
            print i+1, ":", keys[i], "-", component, "-", self.datamanager.comment(keys[i], component)


    def inc_data(self, name, ofs):
        ''' Increments a component index '''
        info("Inc data: %s, %s" % (name, ofs))

        # abort if already switching
        if(self.switching_components):
            warning("Already switching components")
            return

        # get components
        components = self.datamanager.components[name.upper()]

        try:
            idx = [elt[0] for elt in components].index(self.state.components[name])
        except:
            idx = 0

        if(ofs == 0):
            idx = random.randint(0, len(components) - 1)
        else:
            idx += ofs

        # get component
        self.switch_components({name: components[idx % len(components)][0]})



    def switch_components(self, data):
        ''' Switches the system to the new components specified in data '''
        info("Switching components: %s" % str(data))

        self.switching_components = True

        if(len(data) == 0):
            return True

        # create interpolation strings
        for component_name, val in data.items():
            if(self.state.components[component_name] == val):
                continue

            if(len(data) == 1):
                self.interface.renderer.flash_message("Switching %s to %s" % (component_name, val))

            idx_idx = self.datamanager.component_names.index(component_name)

            intrp = "intrp(%s, %s, (time - internal[%d]) / %f)" % (self.state.components[component_name], val, idx_idx, self.app.state_intrp_time * self.state.t_speed)        

            self.state.components[component_name] = intrp

        # compile engine
        self.engine.compile()

        # set internal values
        for component_name, val in data.items():
            idx_idx = self.datamanager.component_names.index(component_name)
            self.state.internal[idx_idx] = self.cmdcenter.time()

        # wait until interpolation is done
        time.sleep(self.app.state_intrp_time)
        self.switching_components = False
        for k,v in data.items():
            self.state.components[k] = v


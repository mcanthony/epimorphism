from common.globals import *
from common.runner import *

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

        # init indices for components
        self.component_idx = [0 for i in xrange(20)]

        self.set_component_indices()


    def set_component_indices(self):
        ''' Given the current components in state, sets the
            component index into datamanager '''

        for component_name in self.datamanager.component_names:
            idx = self.datamanager.component_names.index(component_name)
            if(component_name.upper() not in self.state.components):
                val = ""
            else:
                val = self.state.components[component_name.upper()]

            try:
                data = [elt[0] for elt in self.datamanager.components[component_name]]
                self.component_idx[2 * idx] = data.index(val)
            except:
                warning("couldn't find index for: %s - %s" %(component_name, val))
                self.component_idx[2 * idx] = 0


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


    def inc_data(self, component_name, idx):
        ''' Increments a component index '''
        info("Inc data: %s, %s" % (component_name, idx))

        # abort if already switching
        if(self.switching_components):
            warning("Already switching components")
            return

        # get components
        components = self.datamanager.components[component_name]

        if(len(components) == 1):
            return

        # get and update index
        idx_idx = self.datamanager.component_names.index(component_name)

        val_idx = self.component_idx[2 * idx_idx]
        if(idx == 0):
            val_idx = random.randint(0, len(components) - 1)
        else:
            val_idx += idx
            val_idx %= len(components)

        # get component
        component = components[val_idx]

        self.switch_components({component_name: component[0]})


    def can_switch_to_components(self, data):
        ''' Checks if given components are loaded into kernel '''

        can_switch = True

        for component_name, val in data.items():
            # idx_idx = self.datamanager.component_names.index(component_name)
            components = self.datamanager.components[component_name]
            try:
                [c for c in components if c[0] == val][0]
            except:
                warning("Can't load component: %s - %s" % (component_name, val))
                can_switch = False

        return can_switch


    def switch_components(self, data):
        ''' Switches the system to the new components specified in data '''
        info("Switching components: %s" % str(data))

        self.switching_components = True

        if(len(data) == 0):
            return True

        # create interpolation strings
        for component_name, val in data.items():
            if(len(data) == 1):
                self.interface.renderer.flash_message("Switching %s to %s" % (component_name, val))

            idx_idx = self.datamanager.component_names.index(component_name)
            components = self.datamanager.components[component_name]
            try:
                component = [c for c in components if c[0] == val][0]
            except:
                error("couldn't find val in components - %s, %s" % (component_name, val))
                return False

            val_idx = components.index(component)

            name = component_name.lower()

            intrp = "intrp(%s, %s, (time / %f - internal[%d]) / %f)" % (self.state.components[component_name], val, self.state.t_speed, idx_idx, self.app.state_intrp_time)        

            self.state.components[component_name] = intrp

            self.component_idx[2 * idx_idx] = val_idx

        # compile engine
        self.engine.compile()

        # set internal values
        for component_name, val in data.items():
            idx_idx = self.datamanager.component_names.index(component_name)
            self.state.internal[idx_idx] = self.cmdcenter.time()
            self.state.components[component_name] = val            

        # wait until interpolation is done
        def finish():
            time.sleep(self.app.state_intrp_time)
            self.switching_components = False

        async(finish)


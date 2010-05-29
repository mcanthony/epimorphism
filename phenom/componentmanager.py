from common.globals import *

from phenom.datamanager import *

import time

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
        debug("Inc data: %s, %s" % (component_name, idx))

        # abort if already switching
        if(self.switching_components):
            return

        # get components
        components = self.datamanager.components[component_name]

        if(len(components) == 1):
            return

        # get and update index
        idx_idx = self.datamanager.component_names.index(component_name)

        val_idx = self.component_idx[2 * idx_idx]
        val_idx += idx
        val_idx %= len(components)

        # get component
        component = components[val_idx]

        self.switch_components({component_name: component[0]})


    def can_switch_to_components(self, data):
        ''' Checks if given components are loaded into kernel '''

        can_switch = True

        for component_name, val in data.items():
            idx_idx = self.datamanager.component_names.index(component_name)
            components = self.datamanager.components[component_name]
            try:
                component = [c for c in components if c[0] == val][0]
            except:
                warning("Can't load component: %s - %s" % (component_name, val))
                can_switch = False

        return can_switch


    def switch_components(self, data):
        ''' Switches the system to the new components specified in data '''
        debug("Switching components: %s" % str(data))

        self.switching_components = True

        if(len(data) == 0):
            return True

        # non-spliced
        if(not self.app.splice_components):
            for component_name, val in data.items():
                idx_idx = self.datamanager.component_names.index(component_name)
                components = self.datamanager.components[component_name]
                try:
                    component = [c for c in components if c[0] == val][0]
                except:
                    error("couldn't find val in components - %s, %s" % (component_name, val))
                    return False

                val_idx = components.index(component)

                name = component_name.lower()

                intrp = "\t%s1 = %s;\n" % (name, val)
                intrp += "\tintrp_t = min((time - internal[%d]) / switch_time, 1.0f);\n" % (idx_idx)
                intrp += "\tif(intrp_t == 1.0f)\n\t\t%s=%s1;\n\telse{\n" % (name, name)
                intrp += "\t\t%s0 = %s;\n" % (name, self.state.components[component_name])
                intrp += "\t\tintrp_t = (1.0 + erf(4.0f * intrp_t - 2.0f)) / 2.0;\n"
                intrp += "\t\t%s = ((1.0f - intrp_t) * (%s0) + intrp_t * (%s1));\n\t}" % (name, name, name)                

                self.state.components[component_name] = intrp
                # self.compiling = True
                #t0 = self.cmdcenter.time()
                self.engine.prg = self.engine.compile()
                # self.compiling = False
                #t1 = self.cmdcenter.time()
                #print t1-t0

                self.state.internal[idx_idx] = self.cmdcenter.time()

                self.state.components[component_name] = val
                # self.engine.prg = self.engine.compile()
                self.component_idx[2 * idx_idx] = val_idx

                # wait until interpolation is done
                time.sleep(self.app.state_switch_time)
                self.switching_components = False        

                return

        updates = {}
        first_idx = None
        for component_name, val in data.items():
            idx_idx = self.datamanager.component_names.index(component_name)
            components = self.datamanager.components[component_name]
            try:
                component = [c for c in components if c[0] == val][0]
            except:
                error("couldn't find val in components - %s, %s" % (component_name, val))
                return False

            val_idx = components.index(component)
            updates[component_name] = {"val":val, "component":component, "val_idx":val_idx, "idx_idx":idx_idx}

            if(not first_idx):
                first_idx = idx_idx

            self.component_idx[2 * idx_idx + 1] = val_idx
            self.state.internal[idx_idx] = self.cmdcenter.time()

        # if were only changing 1 component, show a message
        if(len(updates) == 1):
            self.cmdcenter.interface.renderer.flash_message("switching %s to: %s" % (updates.keys()[0], updates[updates.keys()[0]]["val"]))

        # wait until interpolation is done
        t = self.app.state_switch_time - (self.cmdcenter.time() - self.state.internal[first_idx])
        time.sleep(t)

        # update state
        for component_name, update in updates.items():
            val_idx = update["val_idx"]
            idx_idx = update["idx_idx"]
            val = update["val"]

            self.state.components[component_name] = val
            self.state.internal[idx_idx] = 0
            self.component_idx[2 * idx_idx] = val_idx

        self.switching_components = False


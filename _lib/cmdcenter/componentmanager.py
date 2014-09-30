from common.globals import *

from datamanager import *

import time, random, re

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
            print i
#            component = self.state.components[keys[i]]
#            print i+1, ":", keys[i], "-", component, "-", self.datamanager.comment(keys[i], component)


    def inc_data(self, name, ofs, return_result=False):
        ''' Increments a component index '''
        info("Inc data: %s, %s" % (name, ofs))

        # abort if already switching
        if(self.switching_components):
            warning("Already switching components")
            return

        # get components
        base_name = re.sub("\d+", "", name.upper())
        print base_name
        components = self.datamanager.components[base_name]

        try:
            idx = [elt[0] for elt in components].index(self.state.components[name])
        except:
            idx = 0

        if(ofs == 0):
            idx = random.randint(0, len(components) - 1)
        else:
            idx += ofs

        new_component = components[idx % len(components)]
        if(return_result):
            return new_component[0]

        # switch component
        self.switch_components({name: new_component[0]})


    def switch_component(self, component, val):
        self.switch_components({component: val})


    def switch_components_all(self, data, par, aux0, aux1, aux2):
        self.aux0 = aux0
        self.aux1 = aux1
        self.aux2 = aux2
        self.par  = par
        self.switch_components(data, self.update_all)


    def update_all(self):
        self.cmdcenter.switch_aux(0, self.aux0, self.app.state_intrp_time)
        self.cmdcenter.switch_aux(1, self.aux1, self.app.state_intrp_time)
        self.cmdcenter.switch_aux(2, self.aux2, self.app.state_intrp_time)

        for k,v in self.par.items():
            old = self.state.par[k[0]][k[1]]
            #self.state.paths.append(Linear1D("par['%s']" % k[0], k[1], self.app.midi_speed, {'a':old, 'b':v, 'th':0.0}))
            #print "par['%s']" % k[0]
            self.cmdcenter.linear_1d("par['%s']" % k[0], k[1], self.app.midi_speed, old, v)



    def switch_components(self, data, callback=None):
        ''' Switches the system to the new components specified in data '''
        info("Switching components: %s" % str(data))

        print "                START SWITCHING                    "

#        self.cmdcenter.freeze=True
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
        print "                COMPILE                    "
        self.engine.compile(callback)
        print "              DONE COMPILE                 "

        # set internal values
        for component_name, val in data.items():
            idx_idx = self.datamanager.component_names.index(component_name)
            self.state.internal[idx_idx] = self.cmdcenter.time()

        # wait until interpolation is done
        #time.sleep(self.app.state_intrp_time)
        self.cmdcenter.block_for(self.app.state_intrp_time)
        for k,v in data.items():
            self.state.components[k] = v



        print "              DONE BLOCK                 "

        # recompile without interpolation
        self.engine.compile()

        print "              DONE RECOMPILE                 "

        print "              DONE SWITCHING                "
        self.switching_components = False

            #self.cmdcenter.freeze=False

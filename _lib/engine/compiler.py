import config

from common.globals import *

import os, re, sys, time

from common.log import *
from common.runner import *
set_log("COMPILER")

from pycl import *

class Compiler():
    ''' OpenCL Program compiler '''

    def __init__(self, ctx, callback):
        info("Initializing Compiler")
        Globals().load(self)

        self.ctx, self.callback = ctx, callback
        self.substitutions = {"KERNEL_DIM": self.app.kernel_dim}
        self.program = None        

    def compile(self, internal_callback=None):
        ''' Executes the main Compiler sequence '''
        info("Compiling")

        contents = [self.get_definitions()] + [open("kernels/%s.cl" % source).read() for source in self.app.sources]
        debug_out = open("kernels/debug.cl", "w")
        debug_out.write("".join(contents))
        debug_out.close()
        
        try:            
            self.program = clCreateProgramWithSource(self.ctx, contents)
            #self.program.build("-Ikernels -I_lib/cl -cl-mad-enable -cl-no-signed-zeros", callback=create_build_callback(self.callback))
            self.program.build("-Ikernels -I_lib/cl -cl-mad-enable -cl-no-signed-zeros")
            t1 = self.cmdcenter.time()
        except BuildProgramFailureError as e:
            print e
            sys.exit(0)

        info("Done Compiling")            
        if internal_callback:
            internal_callback()
            time.sleep(0.01) # mad ghetto
            
        self.callback(self.program, None)            
        self.cmdcenter.cmd("state.t_phase -= %f" % (t1 - config.last_frame_time))


    def get_definitions(self):
        ''' Turn substutions into defines '''

        info("Getting definitions")        

        definitions = "#define _EPI_\n"

        # components
        for component_name in self.cmdcenter.componentmanager.datamanager.component_names:
            if(component_name in self.state.components):
                self.substitutions[component_name] = self.state.components[component_name]
            else:
                self.substitutions[component_name] = ""

        # get substitutions from application
        self.substitutions.update(self.app.get_substitutions())

        for k, v in self.substitutions.items():
            if(v and v != ""):
                definitions += "#define $%s$ %s\n" % (k, v)

        # bind PAR_NAMES        
        keys = self.state.par.keys()
        keys.sort()
        for i, k in enumerate(keys):
            definitions += "#define %s(idx) par[%d * %d + idx]\n" % (k, self.state.par_dim, i)            

        if not self.state.aux is None:
            definitions += "#define _NUM_AUX %d\n" % len(self.state.aux)
        return definitions

from common.globals import *

import os, re, sys

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

    def compile(self):
        ''' Executes the main Compiler sequence '''
        info("Compiling")

        contents = [self.get_definitions()] + [open("kernels/%s.cl" % source).read() for source in self.app.sources]

        t0 = self.cmdcenter.abs_time()

        try:
            self.program = clCreateProgramWithSource(self.ctx, contents)
            #self.program.build("-Ikernels -I_lib/cl -cl-mad-enable -cl-no-signed-zeros", callback=create_build_callback(self.callback))
            self.program.build("-Ikernels -I_lib/cl -cl-mad-enable -cl-no-signed-zeros")
        except BuildProgramFailureError as e:
            print e
            sys.exit(0)
  
        t1 = self.cmdcenter.abs_time()

        #self.cmdcenter.cmd("state.t_phase -= %f" % (t1 - t0))
        print t1-t0

        self.callback(self.program, None)        


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
            definitions += "#define %s par[%d]\n" % (k, i)            

        return definitions

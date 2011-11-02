from common.globals import *

import os, re, sys

from common.log import *
from common.runner import *
set_log("COMPILER")

from pycl import *

class Compiler():
    ''' OpenCL Program compiler '''

    def __init__(self, ctx, callback):
        debug("Initializing Compiler")
        Globals().load(self)

        self.ctx, self.callback = ctx, callback
        self.substitutions = {"KERNEL_DIM": self.app.kernel_dim}
        self.program = None        

    def compile(self):
        ''' Executes the main Compiler sequence '''
        debug("Compiling")

#        t0 = self.cmdcenter.get_time()

        # render ecu files
        [self.render_file(file) for file in os.listdir("kernels") if re.search("^[^\.]*?\.ecl$", file)]

        # load program from binaries
        contents = open("kernels/__" + self.app.kernel + ".cl").read()

        try:
            self.program = clCreateProgramWithSource(self.ctx, contents)
            self.program.build("-Ikernels -I_lib/cl -cl-mad-enable -cl-no-signed-zeros")
        except BuildProgramFailureError as e:
            print e
            sys.exit(0)
  
        self.callback(self.program)
                     
#        t1 = self.cmdcenter.get_time()
#        self.cmdcenter.t_phase -= t1 - t0

        # remove tmp files
#        files = [file for file in os.listdir("kernel") if re.search("\.ecu$", file)]


    def render_file(self, name):
        ''' Substitues escape sequences in a .ecu file with dynamic content '''

        # open file & read contents
        file = open("kernels/" + name)
        contents = file.read()
        file.close()

        if(not re.search(self.app.kernel, contents.split("\n")[0])):
            return

        info("Rendering: %s", name)        

        # components
        for component_name in self.cmdcenter.componentmanager.datamanager.component_names:
            if(component_name in self.state.components):
                self.substitutions[component_name] = "%s = %s;" % (component_name.lower(),  self.state.components[component_name])
            else:
                self.substitutions[component_name] = ""

        # get substitutions from application
        self.substitutions.update(self.app.substitutions)

        # bind PAR_NAMES
        par_name_str = ""

        for i in xrange(len(self.state.par_names)):
            if(self.state.par_names[i] != ""):
                par_name_str += "#define %s par[%d]\n" % (self.state.par_names[i], i)

        self.substitutions["PAR_NAMES"] = par_name_str[0:-1]

        # replace variables
        for key in self.substitutions:
            contents = re.compile("\%" + key + "\%").sub(str(self.substitutions[key]), contents)

        # write file contents                             
        file = open("kernels/__%s" % (name.replace(".ecl", ".cl")), 'w')
        file.write(contents)
        file.close()

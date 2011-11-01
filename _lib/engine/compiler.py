from common.globals import *

import os, re, commands, sys, gc

from common.log import *
from common.runner import *
set_log("COMPILER")

from ctypes import *
from opencl import *
openCL = PyDLL("libOpenCL.so")

class Compiler():
    ''' OpenCL Program compiler '''

    def __init__(self, device, ctx, callback):
        debug("Initializing Compiler")
        Globals().load(self)

        self.device, self.ctx, self.callback = device, ctx, callback
        self.substitutions = {"KERNEL_DIM": self.app.kernel_dim}
        self.substitutions.update(self.app.substitutions)
        self.program = None        


    def catch_cl(self, err_num, msg):
        if(err_num != 0):
            error(msg + ": " + ERROR_CODES[err_num])
            sys.exit(0)


    def compile(self):
        ''' Executes the main Compiler sequence '''
        debug("Executing")

        # render ecu files
#        t0 = self.cmdcenter.get_time()
        [self.render_file(file) for file in os.listdir("kernels") if re.search("^[^\.]*?\.ecl$", file)]

        # load program from binaries
        contents = open("kernels/__" + self.app.kernel + ".cl").read()
        contents = c_char_p(contents)
        err_num = create_string_buffer(4)        
        self.program = openCL.clCreateProgramWithSource(self.ctx, 1, pointer(contents), (c_long * 1)(len(contents.value)), err_num)
        err_num = cast(err_num, POINTER(c_int)).contents.value
        self.catch_cl(err_num, "creating program")

        print "PROGRAM:", self.program

        err_num = openCL.clBuildProgram(self.program, 0, None, "-Ikernels -I_lib/cl -cl-mad-enable -cl-no-signed-zeros", None, None)
        if(err_num != 0):
            log = create_string_buffer(100000)
            err_num = openCL.clGetProgramBuildInfo(self.program, self.device, PROGRAM_BUILD_LOG, 10000, log, None)
            self.catch_cl(err_num, "getting log")        
            error(log.value)
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

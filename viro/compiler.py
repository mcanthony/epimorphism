from common.globals import *

import pyopencl as cl

import os, re, hashlib, time, commands, subprocess, sys

from common.log import *
from common.runner import *
set_log("COMPILER")

from ctypes import *
from opencl import *
openCL = CDLL("libOpenCL.so")

class CompilerCtypes():
    ''' OpenCL Program compiler '''

    def __init__(self, context, device):
        debug("Initializing Compiler")
        Globals().load(self)

        self.context, self.device = context, device
        self.substitutions = {"KERNEL_DIM": self.profile.kernel_dim, "FRACT": self.profile.FRACT}


    def compile(self):
        ''' Executes the main Compiler sequence '''
        debug("Executing")

        # remove emacs crap
        if(commands.getoutput("ls aeon/.#*").find("No such file or directory") == -1):
            os.system("rm aeon/.#*")

        # render ecu files
        files = [self.render_file(file) for file in os.listdir("aeon") if re.search("\.ecl$", file)]

        contents = open("aeon/__kernel.cl").read()
        contents = c_char_p(contents)
        err_num = create_string_buffer(4)        
        self.program = openCL.clCreateProgramWithSource(self.context, 1, byref(contents), (c_long * 1)(len(contents.value)), byref(err_num))
        err_num = cast(err_num, POINTER(c_int)).contents.value
        if(err_num != 0):
            error("creating program: " + ERROR_CODES[err_num])
            sys.exit(0)

        err_num = openCL.clBuildProgram(self.program, 1, (c_int * 1)(self.device), c_char_p("-I /home/gene/epimorphism/aeon -cl-unsafe-math-optimizations -cl-mad-enable -cl-no-signed-zeros"), None, None)
        if(err_num != 0):
            error("building program: " + ERROR_CODES[err_num])
            sys.exit(0)        

        # start subprocess
        #os.system("rm kernels/kernel.bcl")
        #sub = subprocess.Popen("kernels/compile_kernel.py", stdout=subprocess.PIPE)
        #(stdout, stderr) = sub.communicate()

        #if(len(stdout) != 0):
        #    critical("CRITICAL: Couldn't compile kernel")
        #    critical(stdout)
        #    sys.exit(0)

        #t0 = self.cmdcenter.get_time()
        #prg = cl.Program(self.ctx, [cl.get_platforms()[0].get_devices()[0]], [open("kernels/kernel.bcl").read()])
        #prg.build()

        #   info("Compiling kernel - %s" % name)
        #kernel_contents = open("aeon/__kernel.cl").read()
        #prg = cl.Program(self.ctx, kernel_contents)
        #try:
        #    t1 = time.time()
        #    prg.build(options="-I /home/gene/epimorphism/aeon")
        #    t2 = time.time()
        #    self.cmdcenter.t_phase -= (t2 - t1)
        #except:
        #    critical("Error:")
        #    critical(prg.get_build_info(self.ctx.devices[0], cl.program_build_info.LOG))
        #    self.app.exit = True
        #    sys.exit(0)
                       
        t1 = self.cmdcenter.get_time()
        self.cmdcenter.t_phase -= t1 - t0

        # remove tmp files
        files = [file for file in os.listdir("aeon") if re.search("\.ecu$", file)]

        return self.program


    def render_file(self, name):
        ''' Substitues escape sequences in a .ecu file with dynamic content '''
        debug("Rendering: %s", name)

        # open file & read contents
        file = open("aeon/" + name)
        contents = file.read()
        file.close()

        # cull mode
        if(self.app.cull_enabled):
            self.substitutions['CULL_ENABLED'] = "#define CULL_ENABLED"
        else:
            self.substitutions['CULL_ENABLED'] = ""

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
        file = open("aeon/__%s" % (name.replace(".ecl", ".cl")), 'w')
        file.write(contents)
        file.close()

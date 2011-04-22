from common.globals import *

import os, re, hashlib, time, commands, sys

from common.log import *
from common.runner import *
set_log("COMPILER")

from ctypes import *
from opencl import *
openCL = CDLL("libOpenCL.so")

class CompilerCtypes():
    ''' OpenCL Program compiler '''

    def __init__(self, ctx):
        debug("Initializing Compiler")
        Globals().load(self)

        self.ctx = ctx
        self.substitutions = {"KERNEL_DIM": self.profile.kernel_dim, "FRACT": self.profile.FRACT}
        self.program = None


    def catch_cl(self, err_num, msg):
        if(err_num != 0):
            error(msg + ": " + ERROR_CODES[err_num])
            sys.exit(0)


    def compile(self, device, callback):
        ''' Executes the main Compiler sequence '''
        debug("Executing")

        self.device = device

        # remove emacs crap
        if(commands.getoutput("ls aeon/.#*").find("No such file or directory") == -1):
            os.system("rm aeon/.#*")

        # render ecu files
        t0 = self.cmdcenter.get_time()
        files = [self.render_file(file) for file in os.listdir("aeon") if re.search("\.ecl$", file)]

        # start subprocess
        # sub = subprocess.Popen(["python", "viro/crazy.py", str(self.ctx)], stdout=subprocess.PIPE)
        # (stdout, stderr) = sub.communicate()

        # debug("c1")        
        # load program from source
        #contents = open("kernels/kernel.bcl").read()
        #contents = c_char_p(contents)
        #err_num = create_string_buffer(4)        
        #self.program = openCL.clCreateProgramWithBinary(self.ctx, 1, (c_long * 1)(device), (c_long * 1)(len(contents.value)), byref(contents), None, err_num)
        #err_num = cast(err_num, POINTER(c_int)).contents.value
        #self.catch_cl(err_num, "loading program")

        # load program from binaries
        contents = open("aeon/__kernel.cl").read()
        contents = c_char_p(contents)
        err_num = create_string_buffer(4)        
        self.program = openCL.clCreateProgramWithSource(self.ctx, 1, pointer(contents), (c_long * 1)(len(contents.value)), err_num)
        err_num = cast(err_num, POINTER(c_int)).contents.value
        self.catch_cl(err_num, "creating program")

        # debug("c2")
        CBCKFUNC = CFUNCTYPE(None, c_long, c_void_p)

        def tmp_callback(program, data):
            callback()

        # debug("c2.1")
        err_num = openCL.clBuildProgram(self.program, 0, None, c_char_p("-I /home/gene/epimorphism/aeon -cl-mad-enable -cl-no-signed-zeros"), None, None)
        if(err_num != 0):
            log = create_string_buffer(10000)
            err_num = openCL.clGetProgramBuildInfo(self.program, self.device, PROGRAM_BUILD_LOG, 10000, log, None)
            self.catch_cl(err_num, "getting log")        
            error(log.value)
            sys.exit(0)

        # debug("c2.2")
        callback()
        # debug("c2.3")

        # save binaries
        #binaries = create_string_buffer(1000000)
        #err_num = openCL.clGetProgramInfo(self.program, PROGRAM_BINARIES, 1000000, byref(cast(binaries, c_void_p)), None)
        #self.catch_cl(err_num, "getting program binaries")        
        #open("kernels/kernel.bcl", "w").write(binaries.value)
                       
        t1 = self.cmdcenter.get_time()
        self.cmdcenter.t_phase -= t1 - t0

        # remove tmp files
        files = [file for file in os.listdir("aeon") if re.search("\.ecu$", file)]


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

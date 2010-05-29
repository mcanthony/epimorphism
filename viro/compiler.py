from common.globals import *

import pyopencl as cl

import os, re, hashlib, time, commands, subprocess, sys

from common.log import *
from common.runner import *
set_log("COMPILER")

class Compiler():
    ''' OpenCL Program compiler '''

    def __init__(self, ctx):
        debug("Initializing Compiler")
        Globals().load(self)

        self.substitutions = {"KERNEL_DIM": self.profile.kernel_dim, "FRACT": self.profile.FRACT}
        self.ctx = ctx


    def compile(self):
        ''' Executes the main Compiler sequence '''
        debug("Executing")

        # remove emacs crap
        if(commands.getoutput("ls aeon/.#*").find("No such file or directory") == -1):
            os.system("rm aeon/.#*")

        # render ecu files
        files = [file for file in os.listdir("aeon") if re.search("\.ecl$", file)]
        for file in files:
            self.render_file(file)

        # hash files
        contents = "".join([open("aeon/" + file).read() for file in os.listdir("aeon") if re.search("\.cl$", file)])

        # seed to force recompilation if necessary
        if(not self.app.splice_components): contents += str(time.clock())

        # os.system("rm kernels/kernel.bcl")

        #print "%s compile_kernel.py" % sys.executable
        #sub = subprocess.Popen("./compile_kernel.py", stdout=subprocess.PIPE)
        #(stdout, stderr) = sub.communicate()        

        #print stdout
        #sys.exit(0)

        #os.system("./compile_kernel.py")

        #while(not os.path.exists("kernels/kernel.bcl")):
        #    time.sleep(0.01)

        #prg = cl.Program(self.ctx, cl.get_platforms()[0].get_devices(), [stdout])
        #prg.build()

        

        #    info("Compiling kernel - %s" % name)
        kernel_contents = open("aeon/__kernel.cl").read()
        prg = cl.Program(self.ctx, kernel_contents)
        try:
            t1 = time.time()
            prg.build(options="-I /home/gene/epimorphism/aeon")
            t2 = time.time()
            self.cmdcenter.t_phase -= (t2 - t1)
        except:
            critical("Error:")
            critical(prg.get_build_info(self.ctx.devices[0], cl.program_build_info.LOG))
            self.app.exit = True
            sys.exit(0)

        
        #binaries = prg1.binaries
        #prg = cl.Program(self.ctx, cl.get_platforms()[0].get_devices(), [binaries[0]])

        #prg.build()

        #print prg.get_build_info(self.ctx.devices[0], cl.program_build_info.STATUS)
        #sys.exit(0)

        # remove tmp files
        files = [file for file in os.listdir("aeon") if re.search("\.ecu$", file)]

        return prg


    def splice_components(self):
        ''' This method dynamicly generates the interpolated component switch
            statements that are spliced into the kernels '''
        debug("Splicing components")        

        for component_name in self.cmdcenter.componentmanager.datamanager.component_names:
            component_list = self.cmdcenter.componentmanager.datamanager.components[component_name]

            idx = self.cmdcenter.componentmanager.datamanager.component_names.index(component_name)

            if(len(component_list) == 0):
                self.substitutions[component_name] = ""

            elif(len(component_list) == 1):
                self.substitutions[component_name] = "%s = %s;" % (component_name.lower(), component_list[0][0])

            else:
                clause1 = "switch(indices[2 * %d]){\n" % idx
                for component in component_list:
                    name = component[0]
                    clause1 += "case %d: %s0 = %s;break;\n" % (component_list.index(component), component_name.lower(), name)
                clause1 += "}\n"

                clause2 = "switch(indices[2 * %d + 1]){\n" % idx
                for component in component_list:
                    name = component[0]
                    clause2 += "case %d: %s1 = %s;break;\n" % (component_list.index(component), component_name.lower(), name)
                clause2 += "}\n"

                interp = "if(internal[%d] != 0){\n" % idx
                interp += "intrp_t = min((time - internal[%d]) / switch_time, 1.0f);\n" % (idx)
                interp += "intrp_t = (1.0 + erf(4.0f * intrp_t - 2.0f)) / 2.0;\n"
                sub = "intrp_t"
                interp += "%s\n%s = ((1.0f - %s) * (%s0) + %s * (%s1));" % (clause2,  component_name.lower(), sub, component_name.lower(), sub, component_name.lower())
                interp += "\n}else{\n%s = %s0;\n}" % (component_name.lower(), component_name.lower())

                self.substitutions[component_name] = clause1 + interp


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
        if(self.app.splice_components):
            self.splice_components()
        else:
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

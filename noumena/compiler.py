from phenom.datamanager import *

import os
import re
import sys
import hashlib
import threading
import StringIO
import time

from ctypes import *

def bind_kernel(name):

    # attempt to load kernel
    try:
        lib = cdll.LoadLibrary("tmp/%s.so" % name)#, RTLD_LOCAL)
        # os.system("rm tmp/" + name)
    except:
        print "kernel not found.  exiting."
        exit()

    # extract function
    kernel = lib.__device_stub__Z9kernel_fbP6float4mP6uchar4iffff
    kernel.restype = None
    kernel.argtypes = [ c_void_p, c_ulong, c_void_p, c_int, c_float, c_float, c_float, c_float ]

    reset = lib.__device_stub__Z5resetP6float4m
    reset.restype = None
    reset.argtypes = [ c_void_p, c_ulong ]

    return (kernel, reset)


class Compiler(threading.Thread):
    ''' A Compiler object if responsible for asynchronously calling nvcc.
        The compilation can be restarted by a call to update. '''

    def __init__(self, data, callback, context):

        self.callback, self.context = callback, context

        self.data = data.copy()

        # init update_vars
        self.update_vars = {}
        self.update_vars.update(data)

        # start datamanager & manage components
        self.datamanager = DataManager()

        if(self.context.splice_components):
            self.splice_components()
        else:
            for component_name in self.datamanager.components:
                self.data[component_name] = "%s = %s;" % (component_name.lower(), self.data[component_name])

        # init thread
        threading.Thread.__init__(self)


    def splice_components(self):

        var = self.data
        for component_name in self.datamanager.components:
            component_list = getattr(self.datamanager, component_name)

            idx = self.datamanager.components.index(component_name)

            clause1 = "switch(component_idx[%d][0]){\n" % idx
            for component in component_list:
                name = component[0]
                if(component_name == "T"):
                    name = "zn[0] * (%s) + zn[1]" % name.replace("(z)", "(zn[2] * z + zn[3])")
                elif(component_name == "T_SEED"):
                    name = "zn[8] * (%s) + zn[9]" % name.replace("(z)", "(zn[10] * z + zn[11])")
                clause1 += "case %d: %s0 = %s;break;\n" % (component_list.index(component), component_name.lower(), name)
            clause1 += "}\n"


            clause2 = "switch(component_idx[%d][1]){\n" % idx
            for component in component_list:
                name = component[0]
                if(component_name == "T"):
                    name = "zn[0] * (%s) + zn[1]" % name.replace("(z)", "(zn[2] * z + zn[3])")
                elif(component_name == "T_SEED"):
                    name = "zn[8] * (%s) + zn[9]" % name.replace("(z)", "(zn[10] * z + zn[11])")
                clause2 += "case %d: %s1 = %s;break;\n" % (component_list.index(component), component_name.lower(), name)
            clause2 += "}\n"

            interp = "if(internal[%d] != 0){" % idx
            sub = "min((_clock - internal[%d]) / switch_time, 1.0f)" % (idx)
            interp += "%s\n%s = ((1.0f - %s) * (%s0) + %s * (%s1));" % (clause2,  component_name.lower(), sub, component_name.lower(), sub, component_name.lower())
            interp += "}else{\n%s = %s0;\n}" % (component_name.lower(), component_name.lower())

            self.data[component_name] = clause1 + interp

        return self


    def render_file(self, name):

        # open file & read contents
        file = open("aeon/" + name)
        contents = file.read()
        file.close()

        # bind PAR_NAMES
        par_name_str = ""

        for i in xrange(len(self.data["par_names"])):
            par_name_str += "#define %s par[%d]\n" % (self.data["par_names"][i], i)

        contents = re.compile('\%PAR_NAMES\%').sub(par_name_str, contents)

        # replace variables
        for key in self.update_vars:
            contents = re.compile("\%" + key + "\%").sub(str(self.data[key]), contents)

        # print contents

        # write file contents
        file = open("aeon/__%s" % (name.replace(".ecu", ".cu")), 'w')
        file.write(contents)
        file.close()


    def run(self):

        # render ecu files
        files = [file for file in os.listdir("aeon") if re.search("\.ecu$", file)]

        for file in files:
            self.render_file(file)

        # hash files
        files = [file for file in os.listdir("aeon") if re.search("\.cu$", file)]

        contents = ""
        for file in files:
            contents += open("aeon/" + file).read()

        hash = hashlib.sha1(contents).hexdigest()

        # make name
        name = "%s-%s" % ((self.context.splice_components and "spliced" or "uniq"), hash)

        # compile if library doesn't exist
        if(not os.path.exists("tmp/%s.so" % name)):
            print "compile kernel ", name
            os.system("/usr/local/cuda/bin/nvcc  --host-compilation=c -Xcompiler -fPIC -o tmp/%s.so --shared %s aeon/__kernel.cu" % (name, self.context.ptxas_stats and "--ptxas-options=-v" or ""))

            # remove tmp files
            files = [file for file in os.listdir("aeon") if re.search("\.ecu$", file)]
            for file in files:
                os.system("rm aeon/__%s" % (file.replace(".ecu", ".cu")))
            if(os.path.exists("__kernel.linkinfo")) : os.system("rm __kernel.linkinfo")

        else:
            time.sleep(1)

        # execute callback
        self.callback(name)


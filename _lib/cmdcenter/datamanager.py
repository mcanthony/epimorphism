from common.globals import *

from common.log import *
set_log("DATAMANAGER")

import os, re

class DataManager(object):
    ''' The DataManager singleton object is responsible for loading components from
        .lib and .cl library files in the kernels directory '''


    def __init__(self):
        Globals().load(self)

        # load components from files of form *.epi
        files = [file for file in os.listdir("kernels") if re.search("^%s(.*?)\.lib$"  % self.app.lib_prefix, file)]

        self.components = {}

        for file_name in files:

            # get component name
            component_name = file_name[len(self.app.lib_prefix) + 1:].split('.')[0]

            # open file & read contents
            file = open("kernels/" + file_name)
            contents = file.read()
            file.close()

            # set component
            self.components[component_name.upper()] = []
            values = self.components[component_name.upper()]

            # get all components
            for line in contents.split("\n"):

                # skip blank lines
                if(line == "") : continue

                # parse line
                component = line.split(':')

                # get component
                component[0] = component[0].strip()

                # print component_name, component[0]

                # get defaults
                if(len(component) == 2):
                    component[1] = [cmd.strip() for cmd in component[1].strip().split('#')]
                else:
                    component[1] = []

                # add comment
                component.append(component_name)

                # add component
                values.append(component)


        # load components from files of form *.cl
        files = [file for file in os.listdir("kernels") if re.search("^%s(.*?)\.e*cl$" % self.app.lib_prefix, file)]

        for file_name in files:

            # get component name
            component_name = file_name[len(self.app.lib_prefix) + 1:].split('.')[0].upper()
            file = open("kernels/" + file_name)
            contents = file.read()
            file.close()

            # only parse library files
            if(re.search("library file", contents)):

                # set component
                self.components[component_name.upper()] = []
                values = self.components[component_name.upper()]

                # get all function definitions
                funcs = re.findall("^_%s_.+?^}$" % self.app.lib_prefix.upper(), contents, re.M | re.S)

                for func in funcs:

                    # get function name & args
                    try:
                        func_name = re.search("_%s_ .+? (\S+)\(" % self.app.lib_prefix.upper(), func).group(1)
                        args = [arg.split(" ")[-1] for arg in re.search("\(.+\)", func).group(0)[1:-1].split(", ")]
                    except:
                        error("invalid function definition: %s" % func)
                        continue

                    # find comments
                    comments = re.findall("//\s*(.+)", func)

                    # default if no comments
                    if(len(comments) == 0) : comments = [""]

                    # skip EXCLUDE funcs
                    if(not re.match("EXCLUDE", comments[0])):
                        levels = [level.strip() for level in comments[1].split(',')]

                        # filter by level
                        if(self.app.component_level in levels):
                            # make clause
                            clause = "(" + ", ".join(args) + ")"
                            component = [func_name + clause, comments[0]]

                            # add component
                            values.append(component)

        #self.component_names = self.components.keys()
        self.component_names = self.state.components.keys()
        self.component_names.sort()


    def get_component_for_val(self, component_name, val):
        ''' This function returns the component object given its name and value '''

        # get list
        res = [data for data in self.components['component_name'] if len(data) != 0 and data[0] == val]

        # return component
        if(len(res) != 0):
            return res[0]
        else:
            return None


    def comment(self, component_name, val):
        ''' This function returns the comment for a given component_name with a given value '''

        # get component
        component = self.get_component_for_val(component_name, val)

        # get comment
        if(component):
            return component[1]
        else:
            return ""


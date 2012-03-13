from shutil import *

def generate_application(name):

    # create application object
    f = open("config/applications.py", 'r+')

    if name.capitalize() in f.read():
        return

    f.write("\n\nclass %s(App):\n    def __init__(self, name='default'):\n        App.__init__(self, '%s', name)\n" % (name.capitalize(), name))

    f.close()
    

    # create default application configuration
    f = open("config/app/%s_default.app" % name, "w")
    f.write("{'app':'%s',\n 'state': State('%s', 'default'),\n 'sources': ['util', 'math', 'colorspace', '%s'],\n 'kernel': '%s'}" % (name, name, name, name))
    f.close()

    # create default application state
    f = open("config/state/default.est", "r")
    contents = f.read()
    f.close()
    contents = contents.replace("default", name)
    f = open("config/state/%s_default.est" % name, 'w')
    f.write(contents)
    f.close()

    # create default kernel
    f = open("kernels/test.cl", "r")
    contents = f.read()
    f.close()
    contents = contents.replace("test", name)
    f = open("kernels/%s.cl" % name, 'w')
    f.write(contents)
    f.close()

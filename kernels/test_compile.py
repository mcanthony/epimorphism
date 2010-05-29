from sources.OpenGL.GL import *
from OpenGL.GLUT import *
import OpenGL.raw.GL as rawgl
import threading, time, sys
import pyopencl as cl

def async(func):
    threading.Thread(target=func).start()

glutInit(sys.argv)
glutCreateWindow("")

from common.runner import *

device = cl.get_platforms()[0].get_devices()[0]
ctx    = cl.Context([device])
queue  = cl.CommandQueue(ctx, properties=cl.command_queue_properties.PROFILING_ENABLE)

def test():
    i=0
    t0 = time.time()
    while(time.time() - t0 < 5):
        print i
        i += 1

def compile(conn):
    a = cl.Program(ctx, open("aeon/__kernel.cl").read())
    a.build(options="-I /home/gene/epimorphism/aeon")
    print "a1"
    conn.send(a)
    print "b1"
    conn.close()
    
#async(test)
    
from multiprocessing import Process, Pipe
parent_con, child_con = Pipe()
p = Process(target=compile, args=(child_con,))
p.start()
print "a"
print parent_con.recv()
print "b"
sys.exit(0)
p.join()

#import subprocess
#subprocess.Popen(' '.join([sys.executable] + sys.argv + ['assholes']), shell=True)
#test()
#while 1:
#    print time.time()



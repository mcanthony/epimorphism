#! /usr/bin/python

from OpenGL.GL import *
from OpenGL.GLUT import *
import OpenGL.raw.GL as rawgl
import threading, time
import pyopencl as cl
import sys
from os import system

glutInit(sys.argv)
glutCreateWindow("")

device = cl.get_platforms()[0].get_devices()[0]
ctx    = cl.Context([device])
queue  = cl.CommandQueue(ctx, properties=cl.command_queue_properties.PROFILING_ENABLE)
prg = cl.Program(ctx, open("aeon/__kernel.cl").read())

system("rm kernels/kernel.bcl")

try:
    prg.build(options="-I /home/gene/epimorphism/aeon")
except:
    print "Error:"
    print prg.get_build_info(device, cl.program_build_info.LOG)
    sys.exit(0)

#print prg.binaries

f = open("kernels/kernel.bcl", "w")
f.write(prg.binaries[0])
f.close()

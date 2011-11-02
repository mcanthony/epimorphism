#!/usr/bin/env python
import sys, gc, time
sys.path.append('_lib')
sys.path.append('_lib/sources')

from common.runner import *

from pycl import *


from array import array
source = '''
kernel void mxplusb(float m, global float *x, float b, global float *out) {
     int i = get_global_id(0);
     out[i] = m*x[i]+b;
 }
'''

global building
building = False
global program
program = None

ctx = clCreateContext()
print ctx.value
queue = clCreateCommandQueue(ctx)

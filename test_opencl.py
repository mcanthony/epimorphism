#!/usr/bin/env python
import sys, gc, time
sys.path.append('_lib')

from common.runner import *

from pycl import *


from ctypes import *
openCL = CDLL("libOpenCL.so")

block_size = 16
kernel_dim = 256

DEVICE_TYPE_GPU = 1<<2

# intalize opencl
#platforms = create_string_buffer(4)
#openCL.clGetPlatformIDs (1, platforms, None)
#platform = cast(platforms, POINTER(c_int))[0]

#device = create_string_buffer(4)
#openCL.clGetDeviceIDs(platform, c_long(DEVICE_TYPE_GPU), 1, device, None);
#device = cast(device, POINTER(c_int))[0]

#ctx = openCL.clCreateContext(0, 1, (c_int * 1)(device), None, None, None);

#queue = openCL.clCreateCommandQueue(ctx, device, 0, None);

ctx = clCreateContext()
queue = clCreateCommandQueue(ctx)

#ctx = ctx1.value
#queue = queue1.value


contents = ''' __kernel void main(){}'''
#contents = c_char_p(contents)
#contents = (c_char_p * 1)(contents)


from array import array
source = '''
kernel void mxplusb(float m, global float *x, float b, global float *out) {
     int i = get_global_id(0);
     out[i] = m*x[i]+b;
 }
'''

# repeatedly build & execute kernel

global building
building = False
global program
program = None

def build():
    global building
    global program
    if(building):
        print("building")
        return
    building = True
    #program = openCL.clCreateProgramWithSource(ctx, 1, contents, 0, None) 
    program = clCreateProgramWithSource(ctx, source).build()
    print "PROGRAM:", program.value

    #openCL.clBuildProgram(program, 0, None, None, None, None)

    building = False
    

while(True):
    global main_kernel
    global program
    #async(build)
    build()

    while(building):
        time.sleep(0.01)

    kernel = program['mxplusb']
    kernel.argtypes = (cl_float, cl_mem, cl_float, cl_mem)
    x = array('f', range(100))
    x_buf, in_evt = buffer_from_pyarray(queue, x, blocking=False)
    y_buf = x_buf.empty_like_this()
    run_evt = kernel(2, x_buf, 5, y_buf).on(queue, len(x), wait_for=in_evt)
    y, evt = buffer_to_pyarray(queue, y_buf, wait_for=run_evt, like=x)
    evt.wait()
    print y[0:10]

    #main_kernel = openCL.clCreateKernel(program.value, "main", None)
    #print "MAIN KERNEL:", main_kernel

    #openCL.clEnqueueNDRangeKernel(queue, main_kernel, 1, None, (c_long * 1)(kernel_dim), (c_long * 1)(block_size), 0, None, None) 
    #gc.collect()

#none of these seem to help
    #openCL.clReleaseKernel(main_kernel)
    #openCL.clReleaseProgram(program)

    #    del program
    #    del main_kernel

#openCL.clFinish(queue)
#openCL.clFlush(queue) 

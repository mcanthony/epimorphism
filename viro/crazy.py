#! /usr/bin/python

import sys
from opencl import *
from ctypes import *

openCL = CDLL("libOpenCL.so")

ctx = sys.argv[1]

def catch_cl(self, err_num, msg):
    if(err_num != 0):
        print(msg + ": " + ERROR_CODES[err_num])
        #sys.exit(0)

contents = open("aeon/__kernel.cl").read()
contents = c_char_p(contents)

err_num = create_string_buffer(4)        

print "asdfasdf"

print ctx

program = openCL.clCreateProgramWithSource(int(ctx), 1, byref(contents), (c_long * 1)(len(contents.value)), err_num)

err_num = cast(err_num, POINTER(c_int)).contents.value
catch_cl(err_num, "creating program")

print program


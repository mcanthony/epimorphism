from util import *
from ctypes import *

openCL = CDLL("libOpenCL.so")
# glut = CDLL("libglut.so.3")
# glx = CDLL("libglx.so")

# def initOpenCL():
num_platforms = create_string_buffer(4)
ciErrNum = openCL.clGetPlatformIDs(0, None, num_platforms)
num_platforms = cast(num_platforms, POINTER(c_int)).contents
print "num platforms = ", num_platforms

platforms = create_string_buffer(4 * num_platforms.value)
ciErrNum = openCL.clGetPlatformIDs (num_platforms, platforms, None)
platform = cast(platforms, POINTER(c_int))[0]
print "platform = ", platform

dev_count = create_string_buffer(4)
ciErrNum = openCL.clGetDeviceIDs(platform, DEVICE_TYPE_GPU, 0, None, dev_count);
dev_count = cast(dev_count, POINTER(c_int)).contents
print "dev count = ", dev_count

devices = create_string_buffer(4 * dev_count.value)
ciErrNum = openCL.clGetDeviceIDs(platform, DEVICE_TYPE_GPU, 1, devices, None);
device = cast(devices, POINTER(c_int))[0]
print "device = ", device

#info = create_string_buffer(128)
#ciErrNum = openCL.clGetDeviceInfo(device, DEVICE_PROFILE, 128, info, None)
#print info.value

properties = (c_long * 3)(CONTEXT_PLATFORM, platform, 0)

ciErrNum = create_string_buffer(4)
devices = (c_int * 1)(device)
cxGPUContext = openCL.clCreateContext(properties, 1, devices, None, None, byref(ciErrNum));
# cxGPUContext = openCL.clCreateContextFromType(properties, DEVICE_TYPE_GPU, None, None, byref(ciErrNum));
ciErrNum = cast(ciErrNum, POINTER(c_int)).contents
print "context = ", cxGPUContext

cqCommandQueue = openCL.clCreateCommandQueue(cxGPUContext, device, 0, byref(ciErrNum));
print "queue = ", cqCommandQueue

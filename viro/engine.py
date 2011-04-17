from common.globals import *

from viro.compiler import *

# import pyopencl as cl
import numpy

import sys
import itertools
import time
import threading

import Image

from common.log import *
set_log("ENGINE")

mf = cl.mem_flags
block_size = 16


from ctypes import *
from opencl import *
openCL = CDLL("libOpenCL.so")
gl = CDLL("libGL.so.1")

class EngineCtypes(object):
    ''' The Engine object is the applications interface, via cuda, to the graphics hardware.
        It is responsible for the setup and maintenence of the cuda environment and the graphics kernel.
        It communicates to out via a pbo  '''

    def init(self):
        debug("Initializing Engine")
        Globals().load(self)

        # self.print_opencl_info()

        # OpenCL objects
        self.initOpenCL()

        self.compiler = CompilerCtypes(self.context, self.device)

        # timing vars
        num_time_events = 3
        self.time_events = False
        self.event_accum_tmp = [0 for i in xrange(num_time_events)]
        self.event_accum = [0 for i in xrange(num_time_events)]
        self.last_frame_time = 0
        self.frame_num = 0

        # fb download vars
        self.new_fb_event = threading.Event()
        self.do_get_fb = False


        return True

    def catch_cl(self, err_num, msg):
        if(err_num != 0):
            error(msg + ": " + ERROR_CODES[err_num])
            sys.exit(0)

    
    def initOpenCL(self):
        debug("Setting up OpenCL")

        num_platforms = create_string_buffer(4)
        err_num = openCL.clGetPlatformIDs(0, None, num_platforms)
        self.catch_cl(err_num, "counting platforms")
        num_platforms = cast(num_platforms, POINTER(c_int)).contents.value

        platforms = create_string_buffer(4 * num_platforms)
        err_num = openCL.clGetPlatformIDs (num_platforms, platforms, None)
        self.catch_cl(err_num, "getting platforms")
        self.platform = cast(platforms, POINTER(c_int))[0]

        num_devices = create_string_buffer(4)
        err_num = openCL.clGetDeviceIDs(self.platform, DEVICE_TYPE_GPU, 0, None, num_devices);
        self.catch_cl(err_num, "counting devices")
        num_devices = cast(num_devices, POINTER(c_int)).contents.value

        devices = create_string_buffer(4 * num_devices)
        err_num = openCL.clGetDeviceIDs(self.platform, DEVICE_TYPE_GPU, num_devices, devices, None);
        self.catch_cl(err_num, "getting devices")
        self.device = cast(devices, POINTER(c_int))[0]

        properties = (c_long * 7)(GL_CONTEXT_KHR, gl.glXGetCurrentContext(), GLX_DISPLAY_KHR, gl.glXGetCurrentDisplay(), CONTEXT_PLATFORM, self.platform, 0)
        err_num = create_string_buffer(4)
        self.context = openCL.clCreateContext(properties, 1, (c_int * 1)(self.device), None, None, byref(err_num));
        err_num = cast(err_num, POINTER(c_int)).contents.value
        self.catch_cl(err_num, "creating context")

        err_num = create_string_buffer(4)
        self.queue = openCL.clCreateCommandQueue(self.context, self.device, 0, byref(err_num));
        err_num = cast(err_num, POINTER(c_int)).contents.value
        self.catch_cl(err_num, "creating queue")

        # create images
        format = (c_uint * 2)(BGRA, FLOAT)

        err_num = create_string_buffer(4)
        self.fb = openCL.clCreateImage2D(self.context, MEM_READ_WRITE or MEM_COPY_HOST_PTR or MEM_ALLOC_HOST_PTR, format, self.profile.kernel_dim, self.profile.kernel_dim, None, None, byref(err_num))
        err_num = cast(err_num, POINTER(c_int)).contents.value
        self.catch_cl(err_num, "creating fb")

        err_num = create_string_buffer(4)
        self.out = openCL.clCreateImage2D(self.context, MEM_READ_WRITE or MEM_COPY_HOST_PTR or MEM_ALLOC_HOST_PTR, format, self.profile.kernel_dim, self.profile.kernel_dim, None, None, byref(err_num))
        err_num = cast(err_num, POINTER(c_int)).contents.value
        self.catch_cl(err_num, "creating out")

        err_num = create_string_buffer(4)
        self.aux = openCL.clCreateImage2D(self.context, MEM_READ_WRITE or MEM_COPY_HOST_PTR or MEM_ALLOC_HOST_PTR, format, self.profile.kernel_dim, self.profile.kernel_dim, None, None, byref(err_num))
        err_num = cast(err_num, POINTER(c_int)).contents.value
        self.catch_cl(err_num, "creating aux")

        err_num = create_string_buffer(4)
        format = (c_uint * 2)(BGRA, UNSIGNED_INT8)
        self.img = openCL.clCreateImage2D(self.context, MEM_READ_WRITE or MEM_COPY_HOST_PTR or MEM_ALLOC_HOST_PTR, format, self.profile.kernel_dim, self.profile.kernel_dim, None, None, byref(err_num))
        err_num = cast(err_num, POINTER(c_int)).contents.value
        self.catch_cl(err_num, "creating img")

        # create pbo
        err_num = create_string_buffer(4)
        self.pbo_ptr = self.interface.renderer.generate_pbo(self.profile.kernel_dim)
        self.pbo = openCL.clCreateFromGLBuffer(self.context, MEM_WRITE_ONLY, self.pbo_ptr, byref(err_num))
        err_num = cast(err_num, POINTER(c_int)).contents.value
        self.catch_cl(err_num, "create_pbo")

        # OpenCL buffers
        #data       = numpy.zeros((self.profile.kernel_dim, self.profile.kernel_dim, 4), dtype=numpy.float)
        #data_uint8 = numpy.zeros((self.profile.kernel_dim, self.profile.kernel_dim, 4), dtype=numpy.uint8)
        #self.upload_image(self.fb, numpy.asarray(Image.open('test.png').convert("RGBA")))

        #contents = open("aeon/__kernel.cl").read()
        #contents = c_char_p(contents)
        #err_num = create_string_buffer(4)        
        #self.program = openCL.clCreateProgramWithSource(self.context, 1, byref(contents), (c_long * 1)(len(contents.value)), byref(err_num))
        #err_num = cast(err_num, POINTER(c_int)).contents.value
        #self.catch_cl(err_num, "creating program")

        #err_num = openCL.clBuildProgram(self.program, 1, (c_int * 1)(self.device), c_char_p("-I /home/gene/epimorphism/aeon -cl-unsafe-math-optimizations -cl-mad-enable -cl-no-signed-zeros"), None, None)
        #self.catch_cl(err_num, "building program")

        #err_num = create_string_buffer(4)        
        #self.kernel = openCL.clCreateKernel(self.program, c_char_p("epimorph"), byref(err_num))
        #err_num = cast(err_num, POINTER(c_int)).contents.value
        #self.catch_cl(err_num, "creating program")

        #sys.exit(0)




    def __del__(self):
        debug("Deleting Engine")
        self.new_fb_event.set()
        self.pbo = None


    def do(self):
        ''' Main event loop '''      
        
        self.timings = [time.time()]

        # create args
        args = [(byref(cast(self.fb, c_void_p)), 8), (byref(cast(self.out, c_void_p)), 8), (byref(cast(self.pbo, c_void_p)), 8)]    

        for data in self.frame:
            # convert to ctypes
            if(data["type"] == "float"):
                args.append((byref(c_float(data["val"])), 4))
            elif(data["type"] == "float_array"):
                buf = openCL.clCreateBuffer(self.context, MEM_READ_ONLY or MEM_COPY_HOST_PTR, 4 * len(data["val"]), (c_float * len(data["val"]))(data["val"]))
                args.append(cl.Buffer((byref(cast(buf, c_void_p)), 8)))
            elif(data["type"] == "int_array"):
                buf = openCL.clCreateBuffer(self.context, MEM_READ_ONLY or MEM_COPY_HOST_PTR, 4 * len(data["val"]), (c_int * len(data["val"]))(data["val"]))
                args.append(cl.Buffer((byref(cast(buf, c_void_p)), 8)))
            elif(data["type"] == "complex_array"):
                buf = openCL.clCreateBuffer(self.context, MEM_READ_ONLY or MEM_COPY_HOST_PTR, 4 * len(data["val"]) * 2, (c_float * (len(data["val"]) * 2))(list(itertools.chain(*[(z.real, z.imag) for z in data["val"]]))))
                args.append(cl.Buffer((byref(cast(buf, c_void_p)), 8)))

        for i in xrange(len(args)):
            err_num = openCL.clSetKernelArg(self.kernel, i, args[i][1], args[i][0])
            self.catch_cl(err_num, "creating argument %d" % i)

        # execute kernel
        self.timings.append(time.time())

        event = create_string_buffer(8)
        err_num = openCL.clEnqueueAcquireGLObjects(self.queue, 1, (c_int * 1)(self.pbo), None, None, event)
        self.catch_cl(err_num, "enque acquire pbo")
        err_num = openCL.clWaitForEvents(1, event)
        self.catch_cl(err_num, "waiting to acquire pbo")

        event = create_string_buffer(8)
        err_num = openCL.clEnqueueNDRangeKernel(self.queue, self.kernel, 2, None, 
                                                (c_uint * 2)(self.profile.kernel_dim, self.profile.kernel_dim), 
                                                (c_uint * 2)(block_size, block_size), 
                                                None, None, event)
        self.catch_cl(err_num, "enque execute kernel")
        err_num = openCL.clWaitForEvents(1, event)
        self.catch_cl(err_num, "waiting to execute kernel")

        self.timings.append(time.time())

        # copy out to fb
        event = create_string_buffer(8)
        err_num = openCL.clEnqueueCopyImage(self.queue, self.out, self.fb, (c_long * 3)(0, 0, 0), (c_long * 3)(0, 0, 0), (c_long * 3)(self.profile.kernel_dim, self.profile.kernel_dim, 1), None, None, event)
        self.catch_cl(err_num, "enque copy fb")
        err_num = openCL.clWaitForEvents(1, event)        
        self.catch_cl(err_num, "waiting to copy fb")


        self.timings.append(time.time())

        # post processing
        if(self.state.get_par("_POST_PROCESSING") != 0.0):
            self.prg.post_process(self.queue, (self.profile.kernel_dim, self.profile.kernel_dim),
                                  self.fb, self.pbo, args[3], args[5],
                                  local_size=(block_size,block_size)).wait()
            self.timings.append(time.time())

        event = create_string_buffer(8)
        err_numopenCL.clEnqueueReleaseGLObjects(self.queue, 1, (c_int * 1)(self.pbo), None, None, event)
        self.catch_cl(err_num, "enque release pbo")
        err_num = openCL.clWaitForEvents(1, event)
        self.catch_cl(err_num, "waiting to release pbo")

        self.frame_num += 1
        self.print_timings()

        # grab frame buffer - must be at end of function
        if(self.do_get_fb):
            self.do_get_fb = False
            self.get_fb_internal()


    def get_fb_internal(self):
        debug("Get fb internal")

        # compute image
        self.prg.get_image(self.queue, (self.profile.kernel_dim, self.profile.kernel_dim),                       
                           self.fb, self.img,
                           local_size=(block_size,block_size)).wait()

        # download image        
        cl.enqueue_read_image(self.queue, self.img, (0,0,0), (self.profile.kernel_dim, self.profile.kernel_dim, 1), self.fb_contents, 0, 0, None, True).wait()    

        self.new_fb_event.set()


    def print_opencl_info(self):
        def print_info(obj, info_cls):
            for info_name in sorted(dir(info_cls)):
                if not info_name.startswith("_") and info_name != "to_string":
                    info = getattr(info_cls, info_name)
                    try:
                        info_value = obj.get_info(info)
                    except:
                        info_value = "<error>"

                    debug("%s: %s" % (info_name, info_value))

        for platform in cl.get_platforms():
            debug(75*"=")
            debug(platform)
            debug(75*"=")
            print_info(platform, cl.platform_info)

            for device in platform.get_devices():
                debug(75*"=")
                debug(platform)
                debug(75*"=")
                print_info(device, cl.device_info)


    def print_timings(self):
        if(self.time_events):
            if(self.frame_num % self.profile.debug_freq == 0):
                # get times
                times = [1000 * (self.timings[i + 1] - self.timings[i]) for i in xrange(len(self.timings) - 1)]

                # set accumulators
                self.event_accum_tmp = [self.event_accum_tmp[i] + times[i] for i in xrange(len(times))]
                self.event_accum = [self.event_accum[i] + times[i] for i in xrange(len(times))]

                # print times
                for i in range(len(times)):
                    print "event" + str(i) + "-" + str(i + 1) + ": " + str(self.event_accum_tmp[i] / self.profile.debug_freq) + "ms"
                    print "event" + str(i) + "-" + str(i + 1) + "~ " + str(self.event_accum[i] / self.frame_num) + "ms"

                # print totals
                print "total cuda:", str(sum(self.event_accum_tmp) / self.profile.debug_freq) + "ms"
                print "total cuda~", str(sum(self.event_accum) / self.frame_num) + "ms"

                # print abs times
                abs = 1000 * ((time.time() - self.last_frame_time) % 1) / self.profile.debug_freq
                print "python:", abs - sum(self.event_accum_tmp) / self.profile.debug_freq
                print "abs:", abs

                # reset tmp accumulator
                self.event_accum_tmp = [0 for i in xrange(len(times))]

                self.last_frame_time = time.time()


    ######################################### PUBLIC ##################################################
    def start(self):
        ''' Start engine '''
        info("Starting engine")

        # compile kernel
        self.prg = self.compile()


    def compile(self):
        ''' Compile the kernel'''
        debug("Compiling kernel")        
        return self.compiler.compile()


    def upload_image(self, cl_image, data):
        ''' Upload an image to the DEVICE '''
        debug("Uploading image")

        cl.enqueue_write_image(self.queue, cl_image, (0,0,0), (self.profile.kernel_dim, self.profile.kernel_dim, 1), data, 0, 0, None, True).wait()        


    def get_fb(self):
        ''' Download the fb '''
        debug("Downloading frame buffer")

        self.do_get_fb = True
        self.new_fb_event.clear()
        self.new_fb_event.wait()

        # return contents
        return self.fb_contents


    def reset_fb(self):
        ''' Clear the current frame buffer '''

        self.upload_image(self.fb, numpy.zeros(4 * self.profile.kernel_dim ** 2, dtype=numpy.float))

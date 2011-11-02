from common.globals import *

from compiler import *

import sys, gc
import itertools
import time
import threading

from array import array

# import Image

from common.log import *
set_log("ENGINE")

block_size = 16

from pycl import *

#from ctypes import *
#from opencl import *
#openCL = PyDLL("libOpenCL.so")
#gl = PyDLL("libGL.so.1")

class Engine(object):
    ''' The Engine object is the applications interface, via cuda, to the graphics hardware.
        It is responsible for the setup and maintenence of the cuda environment and the graphics kernel.
        It communicates to out via a pbo  '''

    def init(self):
        debug("Initializing Engine")
        Globals().load(self)

        # self.print_opencl_info()

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

        self.do_flash_fb = False
        self.program = None
        self.cl_initialized = False

        return True


    def __del__(self):
        debug("Deleting Engine")    
        self.new_fb_event.set()
        self.pbo = None

    
    def initCL(self):
        debug("Setting up OpenCL")        

        self.ctx = clCreateContextFromType(CL_DEVICE_TYPE_GPU, None, gl_interop_ctx_props())
        self.queue = clCreateCommandQueue(self.ctx)

        # create buffers
        format = cl_image_format(CL_BGRA, CL_FLOAT)

        if(self.app.feedback_buffer):
            self.fb = clCreateImage2D(self.ctx, self.app.kernel_dim, self.app.kernel_dim, format)
            self.out = clCreateImage2D(self.ctx, self.app.kernel_dim, self.app.kernel_dim, format)

        # auxiliary buffer
        self.aux = clCreateImage2D(self.ctx, self.app.kernel_dim, self.app.kernel_dim, format)

        # map pbo
        self.pbo_ptr = self.interface.renderer.generate_pbo(self.app.kernel_dim)
        self.pbo = clCreateFromGLBuffer(self.ctx, self.pbo_ptr, CL_MEM_WRITE_ONLY)       
            
        self.arg_buffers = {}

        # create compiler & misc data
        self.compiler = Compiler(self.ctx, self.compiler_callback)
        self.empty = cast(create_string_buffer(16 * self.app.kernel_dim ** 2), POINTER(c_float))
        self.fb_contents = cast(create_string_buffer(16 * self.app.kernel_dim ** 2), POINTER(c_float))

        self.cl_initialized = True


    def compiler_callback(self, program):

        self.program = program
        self.main_kernel = self.program[self.app.kernel]

        # initialize arguments
        if(self.app.feedback_buffer):
            self.main_kernel.argtypes=(cl_mem, cl_mem, cl_mem, cl_float, cl_float, cl_mem, cl_mem, cl_mem)
        else:
            self.main_kernel.argtypes=(cl_mem, cl_float, cl_float, cl_mem, cl_mem, cl_mem)


    def do(self):
        ''' Main event loop '''          
        #debug("start do")

        if(not self.cl_initialized):
            self.initCL()
            self.compiler.compile()
        
        self.timings = [time.time()]

        # acquire pbo
        event = cl_event()
        clEnqueueAcquireGLObjects(self.queue, [self.pbo], None, event)
        event.wait()
        
        # create args
        if(self.app.feedback_buffer):
            args = [self.fb, self.out, self.pbo]
        else:
            args = [self.pbo]            
        for data in self.frame:
            if(data["type"] == "float"):
                args.append(data["val"])
            elif(data["type"] == "float_array"):
                buf = self.arg_buffers.has_key(data["name"]) and self.arg_buffers[data["name"]] or None
                self.arg_buffers[data["name"]] = buffer_from_pyarray(self.queue, array('f', data["val"]), buf)[0]
                args.append(self.arg_buffers[data["name"]])
            elif(data["type"] == "complex_array"):
                buf = self.arg_buffers.has_key(data["name"]) and self.arg_buffers[data["name"]] or None
                val = list(itertools.chain(*[(z.real, z.imag) for z in data["val"]]))
                self.arg_buffers[data["name"]] = buffer_from_pyarray(self.queue, array('f', val), buf)[0]
                args.append(self.arg_buffers[data["name"]])
             
        self.main_kernel(*args).on(self.queue, (self.app.kernel_dim, self.app.kernel_dim), (block_size, block_size)).wait()

        if(self.app.feedback_buffer):
            # copy out to fb
            event = create_string_buffer(8)
            err_num = openCL.clEnqueueCopyImage(self.queue, self.out, self.fb, (c_long * 3)(0, 0, 0), (c_long * 3)(0, 0, 0), (c_long * 3)(self.app.kernel_dim, self.app.kernel_dim, 1), None, None, event)
            self.catch_cl(err_num, "enque copy fb")
            err_num = openCL.clWaitForEvents(1, event)        
            self.catch_cl(err_num, "waiting to copy fb")

            self.timings.append(time.time())



        # post processing
#        if(self.state.get_par("_POST_PROCESSING") != 0.0):
#            post_args = [args[0], args[2], args[3], args[5]]
#            for i in xrange(len(post_args)):
#                err_num = openCL.clSetKernelArg(self.post_process, i, post_args[i][1], post_args[i][0])
#                self.catch_cl(err_num, "creating post argument %d" % i)
#            event = create_string_buffer(8)
#            err_num = openCL.clEnqueueNDRangeKernel(self.queue, self.post_process, 2, None, 
#                                                    (c_long * 2)(self.app.kernel_dim, self.app.kernel_dim), 
#                                                    (c_long * 2)(block_size, block_size), 
#                                                    None, None, event)
#            self.catch_cl(err_num, "enque post execute kernel")
#            err_num = openCL.clWaitForEvents(1, event)
#            self.catch_cl(err_num, "waiting to execute post kernel")

#            self.timings.append(time.time())

        # release pbo

        event = cl_event()
        clEnqueueReleaseGLObjects(self.queue, [self.pbo], None, event)
        event.wait()

        self.frame_num += 1
        self.print_timings()

        #openCL.clFinish(self.queue)

        #debug("end do")


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
            if(self.frame_num % self.app.debug_freq == 0):
                # get times
                times = [1000 * (self.timings[i + 1] - self.timings[i]) for i in xrange(len(self.timings) - 1)]

                # set accumulators
                self.event_accum_tmp = [self.event_accum_tmp[i] + times[i] for i in xrange(len(times))]
                self.event_accum = [self.event_accum[i] + times[i] for i in xrange(len(times))]

                # print times
                for i in range(len(times)):
                    print "event" + str(i) + "-" + str(i + 1) + ": " + str(self.event_accum_tmp[i] / self.app.debug_freq) + "ms"
                    print "event" + str(i) + "-" + str(i + 1) + "~ " + str(self.event_accum[i] / self.frame_num) + "ms"

                # print totals
                print "total cuda:", str(sum(self.event_accum_tmp) / self.app.debug_freq) + "ms"
                print "total cuda~", str(sum(self.event_accum) / self.frame_num) + "ms"

                # print abs times
                abs = 1000 * ((time.time() - self.last_frame_time) % 1) / self.app.debug_freq
                print "python:", abs - sum(self.event_accum_tmp) / self.app.debug_freq
                print "abs:", abs

                # reset tmp accumulator
                self.event_accum_tmp = [0 for i in xrange(len(times))]

                self.last_frame_time = time.time()


    ######################################### PUBLIC ##################################################


    def start(self):
        ''' Start engine '''
        info("Starting engine")        

    
    def compile(self):
        self.compiler.compile()


    def upload_image(self, cl_image, data):
        ''' Upload an image to the DEVICE '''
        debug("Uploading image")

        err_num = openCL.clEnqueueWriteImage(self.queue, cl_image, TRUE, (c_long * 3)(0,0,0), (c_long * 3)(self.app.kernel_dim, self.app.kernel_dim, 1), 0, 0, cast(data, POINTER(c_float)), 0, None,None)
        self.catch_cl(err_num, "uploading image")

from common.globals import *

import itertools
import time
import threading

from pycl import *

from array import array

from compiler import *

from common.log import *
set_log("ENGINE")

block_size = 16

class Engine(object):
    ''' The Engine object is the applications interface, via opencl, to the graphics hardware.
        It is responsible for the setup and maintenence of the opencl environment and the graphics kernel.
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

        # create basic structs
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
        #self.empty = cast(create_string_buffer(16 * self.app.kernel_dim ** 2), POINTER(c_float))
        #self.fb_contents = cast(create_string_buffer(16 * self.app.kernel_dim ** 2), POINTER(c_float))

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
        clEnqueueAcquireGLObjects(self.queue, [self.pbo], None).wait()
        
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

        # copy buffer if necessary
        if(self.app.feedback_buffer):
            clEnqueueCopyImage(self.queue, self.out, self.fb).wait()
            self.timings.append(time.time())

        # post processing

        # release pbo
        clEnqueueReleaseGLObjects(self.queue, [self.pbo], None).wait()

        self.frame_num += 1
        self.print_timings()

        #debug("end do")


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
                print "total opencl:", str(sum(self.event_accum_tmp) / self.app.debug_freq) + "ms"
                print "total opencl~", str(sum(self.event_accum) / self.frame_num) + "ms"

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

from common.globals import *

import itertools, time
from pycl import *
from ctypes import *

import ctypes
from ctypes import (c_size_t as size_t)

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

        # timing vars
        num_time_events = 10
        self.event_accum_tmp = [0 for i in xrange(num_time_events)]
        self.event_accum = [0 for i in xrange(num_time_events)]
        self.last_frame_time = 0

        self.frame_num = 0

        self.program = None
        self.cl_initialized = False

        return True


    def __del__(self):
        debug("Deleting Engine")    
        self.pbo = None

    
    def initCL(self):
        debug("Setting up OpenCL")        

        # create basic structs
        self.ctx = clCreateContextFromType(CL_DEVICE_TYPE_GPU, None, get_gl_sharing_context_properties())
        self.queue = clCreateCommandQueue(self.ctx)

        # create buffers
        format = cl_image_format(CL_BGRA, CL_FLOAT)

        self.out = clCreateImage2D(self.ctx, self.app.kernel_dim, self.app.kernel_dim, format)

        if(self.app.feedback_buffer):
            self.fb = clCreateImage2D(self.ctx, self.app.kernel_dim, self.app.kernel_dim, format)
            self.empty = cast(create_string_buffer(16 * self.app.kernel_dim ** 2), POINTER(c_float))
            self.reset_fb()

        #auxilary buffer
        if(self.state.aux):
            self.aux = clCreateImage3D(self.ctx, self.app.kernel_dim, self.app.kernel_dim, len(self.state.aux), cl_image_format(CL_BGRA, CL_UNSIGNED_INT8))

        # map pbo
        self.pbo_ptr = self.interface.renderer.generate_pbo(self.app.kernel_dim)
        self.pbo = clCreateFromGLBuffer(self.ctx, self.pbo_ptr, CL_MEM_WRITE_ONLY)       
        #self.pbo = clCreateFromGLTexture2D(self.ctx, self.pbo_ptr, CL_MEM_READ_ONLY)       
            
        self.arg_buffers = {}

        # create compiler
        self.compiler = Compiler(self.ctx, self.compiler_callback)

        # load aux image
        if(self.state.aux):
            for i in range(len(self.state.aux)):
                if(self.state.aux[i]): self.cmdcenter.load_image(self.state.aux[i], i)

        self.cl_initialized = True


    def compiler_callback(self, program, data):
        self.program = program
        self.main_kernel = self.program[self.app.kernel]

        # initialize main_kernel arguments
        if(self.app.feedback_buffer):
            self.main_kernel.argtypes=(cl_mem, cl_mem, cl_mem, cl_mem, cl_mem, cl_mem, cl_mem, cl_float)
        else:
            self.main_kernel.argtypes=(cl_mem, cl_mem, cl_mem, cl_mem, cl_mem, cl_mem, cl_float)

        # post processing kernel
        if(self.state.post_process):
            self.post_process = self.program[self.state.post_process]
            self.post_process.argtypes = (cl_mem, cl_mem, cl_mem, cl_mem, cl_float)


    def do(self):
        ''' Main event loop '''          
        #debug("start do")

        if(not self.cl_initialized):
            self.initCL()
            self.compiler.compile()
            #self.cmdcenter.load(5)

        if(not self.main_kernel):
            return
        
        self.timings = [time.time()]

        # acquire pbo
        clEnqueueAcquireGLObjects(self.queue, [self.pbo], None).wait()
        
        self.timings.append(time.time())

        # create args
        args = [self.pbo, self.out]
        
        if self.state.aux:
            args += [self.aux]
            
        if(self.app.feedback_buffer):
            args = [self.fb] + args
            
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
             

        self.timings.append(time.time())
        self.main_kernel(*args).on(self.queue, (self.app.kernel_dim, self.app.kernel_dim), (block_size, block_size)).wait()
        self.timings.append(time.time())

        # copy buffer if necessary
        if(self.app.feedback_buffer):
            clEnqueueCopyImage(self.queue, self.out, self.fb).wait()
            self.timings.append(time.time())
        self.timings.append(time.time())

        # post processing
        if(self.state.post_process):
            #i = (self.app.feedback_buffer and 1 or 0)
            args = [args[0], args[1], args[4], args[5], args[7]] # maybe could use some work, if frame format ever changes
            self.post_process(*args).on(self.queue, (self.app.kernel_dim, self.app.kernel_dim), (block_size, block_size)).wait()

        # release pbo
        clEnqueueReleaseGLObjects(self.queue, [self.pbo], None).wait()
        self.timings.append(time.time())

        self.frame_num += 1
        self.print_timings()

        #debug("end do")


    def print_timings(self):
        if(self.app.print_timing_info):
            # get times
            times = [1000 * (self.timings[i + 1] - self.timings[i]) for i in xrange(len(self.timings) - 1)]

            # set accumulators
            self.event_accum_tmp = [self.event_accum_tmp[i] + times[i] for i in xrange(len(times))]
            self.event_accum = [self.event_accum[i] + times[i] for i in xrange(len(times))]

            if(self.frame_num % self.app.debug_freq == 0):
                # print times
                for i in range(len(times)):
                    print "event%d-%d: %0.5fms" % (i, i + 1, self.event_accum_tmp[i] / self.app.debug_freq)
                    print "event%d-%d~ %0.5fms" % (i, i + 1, self.event_accum[i] / self.frame_num)

                # print totals
                print "opencl:   %0.5fms" % (sum(self.event_accum_tmp) / self.app.debug_freq)
                print "opencl~   %0.5fms" % (sum(self.event_accum) / self.frame_num)

                # print abs times
                abs = 1000 * ((time.time() - self.last_frame_time) % 1) / self.app.debug_freq
                print "python:   %0.5fms" % (abs - sum(self.event_accum_tmp) / self.app.debug_freq)
                print "total:    %0.5fms" % abs
                print "***********************"

                # reset tmp accumulator
                self.event_accum_tmp = [0 for i in xrange(len(times))]

                self.last_frame_time = time.time()


    ######################################### PUBLIC ##################################################


    def start(self):
        ''' Start engine '''
        info("Starting engine")        

    
    def compile(self, callback=None):
        self.compiler.compile(callback)


    def upload_image(self, cl_image, data, idx=None):
        ''' Upload an image to the DEVICE '''
        # debug("Uploading image")
        if idx == None:
            clEnqueueWriteImage(self.queue, cl_image, data)
        else:
            clEnqueueWriteImage(self.queue, cl_image, data, (0, 0, idx), (size_t * 3)(self.app.kernel_dim, self.app.kernel_dim, 1))


    def reset_fb(self):
        ''' Clear the current frame buffer '''
        debug("Reset fb")
        if(not self.app.feedback_buffer):
            return

        self.upload_image(self.fb, self.empty)


    def load_aux(self, img, idx):
        ''' Loads an image into the auxilary buffer '''

        self.upload_image(self.aux, img.tostring("raw", "BGRA", 0, -1), idx)



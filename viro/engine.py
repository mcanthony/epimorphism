from common.globals import *

from viro.compiler import *

import pyopencl as cl
import numpy

import sys
import itertools
from time import time

import Image

from common.log import *
set_log("ENGINE")

mf = cl.mem_flags

class Engine(object):
    ''' The Engine object is the applications interface, via cuda, to the graphics hardware.
        It is responsible for the setup and maintenence of the cuda environment and the graphics kernel.
        It communicates to out via a pbo  '''

    def init(self):
        debug("Initializing Engine")
        Globals().load(self)

        debug("Setting up OpenCL")
        self.print_opencl_info()

        self.device = cl.get_platforms()[0].get_devices()[0]
        self.ctx    = cl.Context([self.device])
        self.queue  = cl.CommandQueue(self.ctx, properties=cl.command_queue_properties.PROFILING_ENABLE)

        self.compiler = Compiler(self.ctx)

        self.pbo = None

        data = numpy.zeros((self.profile.kernel_dim, self.profile.kernel_dim, 4), dtype=numpy.uint8)
        self.fb  = cl.Image(self.ctx, mf.READ_WRITE | mf.COPY_HOST_PTR | mf.ALLOC_HOST_PTR, cl.ImageFormat(cl.channel_order.BGRA, cl.channel_type.UNSIGNED_INT8), (self.profile.kernel_dim,)*2, hostbuf=data)
        self.out = cl.Image(self.ctx, mf.READ_WRITE | mf.COPY_HOST_PTR | mf.ALLOC_HOST_PTR, cl.ImageFormat(cl.channel_order.BGRA, cl.channel_type.UNSIGNED_INT8), (self.profile.kernel_dim,)*2, hostbuf=data)
        self.aux = cl.Image(self.ctx, mf.READ_WRITE | mf.COPY_HOST_PTR | mf.ALLOC_HOST_PTR, cl.ImageFormat(cl.channel_order.BGRA, cl.channel_type.UNSIGNED_INT8), (self.profile.kernel_dim,)*2, hostbuf=data)
  
        #self.upload_image(self.fb, numpy.asarray(Image.open('test.png').convert("RGBA")))

        self.par      = cl.Buffer(self.ctx, mf.READ_ONLY | mf.COPY_HOST_PTR | mf.ALLOC_HOST_PTR, hostbuf=numpy.zeros(len(self.state.par), dtype=numpy.float32))
        self.internal = cl.Buffer(self.ctx, mf.READ_ONLY | mf.COPY_HOST_PTR | mf.ALLOC_HOST_PTR, hostbuf=numpy.zeros(len(self.state.internal), dtype=numpy.float32))
        self.indices  = cl.Buffer(self.ctx, mf.READ_ONLY | mf.COPY_HOST_PTR | mf.ALLOC_HOST_PTR, hostbuf=numpy.zeros(len(self.state.components), dtype=numpy.int32)) 
        self.zn       = cl.Buffer(self.ctx, mf.READ_ONLY | mf.COPY_HOST_PTR | mf.ALLOC_HOST_PTR, hostbuf=numpy.zeros(2 * len(self.state.zn), dtype=numpy.float32)) 
      
        self.frame_num = 0

        num_time_events = 3
        self.time_events = False
        self.event_accum_tmp = [0 for i in xrange(num_time_events)]
        self.event_accum = [0 for i in xrange(num_time_events)]
        self.last_frame_time = 0

        return True


    def __del__(self):
        debug("Deleting Engine")

        self.pbo = None


    def do(self):
        ''' Main event loop '''

        if(not self.pbo):
            return
        
        self.timings = [time()]

        block_size = 16

        #cl.enqueue_write_buffer(self.queue, self.par, hostbuf=numpy.array(self.frame["par"], dtype=numpy.float32), is_blocking=True).wait()
        #cl.enqueue_write_buffer(self.queue, self.internal, hostbuf=numpy.array(self.frame["internal"], dtype=numpy.float32), is_blocking=True).wait()
        # cl.enqueue_write_buffer(self.queue, self.indices, hostbuf=numpy.array(self.frame["indices"], dtype=numpy.int32), is_blocking=True).wait()
        #cl.enqueue_write_buffer(self.queue, self.zn, hostbuf=numpy.array(list(itertools.chain(*[(z.real, z.imag) for z in self.frame["zn"]])), dtype=numpy.float32), is_blocking=True).wait()
        args = [self.fb, self.out, self.pbo]
#                numpy.float32(self.frame["time"]), numpy.float32(self.frame["switch_time"]), self.par, self.internal, self.indices, self.zn]
        # copy constants to kernel
        for data in self.frame:
            # convert to ctypes
            if(data["type"] == "float"):
                args.append(numpy.float32(data["val"]))
            elif(data["type"] == "float_array"):
                args.append(cl.Buffer(self.ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=numpy.array(data["val"], dtype=numpy.float32)))
            elif(data["type"] == "int_array"):
                args.append(cl.Buffer(self.ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=numpy.array(data["val"], dtype=numpy.int32)))
            elif(data["type"] == "complex_array"):
               args.append(cl.Buffer(self.ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=numpy.array(list(itertools.chain(*[(z.real, z.imag) for z in data["val"]])), dtype=numpy.float32)))
        self.timings.append(time())

        cl.enqueue_acquire_gl_objects(self.queue, [self.pbo]).wait()
        self.prg.test(self.queue, (self.profile.kernel_dim, self.profile.kernel_dim),                       
                      *args, 
                      local_size=(block_size,block_size)).wait()
        cl.enqueue_release_gl_objects(self.queue, [self.pbo]).wait()
        self.timings.append(time())

        cl.enqueue_copy_image(self.queue, self.out, self.fb, (0, 0), (0, 0), (self.profile.kernel_dim,) * 2).wait()
        self.timings.append(time())

        self.frame_num += 1
        self.print_timings()

        #Image.fromarray(self.download_image(self.out), "RGBA").save("out.png")       
        #sys.exit(0)


    ######################################### PUBLIC ##################################################

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
                abs = 1000 * ((time() - self.last_frame_time) % 1) / self.profile.debug_freq
                print "python:", abs - sum(self.event_accum_tmp) / self.profile.debug_freq
                print "abs:", abs

                # reset tmp accumulator
                self.event_accum_tmp = [0 for i in xrange(len(times))]

                self.last_frame_time = time()


    def start(self):
        ''' Start engine '''
        info("Starting engine")

        # generate pbo
        self.pbo_ptr = self.interface.renderer.generate_pbo(self.profile.kernel_dim)
        self.pbo = cl.GLBuffer(self.ctx, mf.WRITE_ONLY, self.pbo_ptr.value)

        # compile
        self.compile()


    def compile(self):
        ''' Compile the kernel'''
        debug("Compiling kernel")

        self.prg = self.compiler.compile()
        self.kernel = self.prg.test


    def upload_image(self, cl_image, data):
        ''' Upload an image to the DEVICE '''
        debug("Uploading image")

        cl.enqueue_write_image(self.queue, cl_image, (0,0,0), (self.profile.kernel_dim, self.profile.kernel_dim, 1), data, 0, 0, None, True).wait()        


    def download_image(self, cl_image):
        ''' Download an image from the DEVICE '''
        debug("Downloading image")

        data = numpy.zeros((self.profile.kernel_dim, self.profile.kernel_dim, 4), dtype=numpy.uint8)
        cl.enqueue_read_image(self.queue, cl_image, (0,0,0), (self.profile.kernel_dim, self.profile.kernel_dim, 1), data, 0, 0, None, True).wait()
        
        return data



from sources.OpenGL.GL import *

from common.globals import *

from viro.compiler import *

import pyopencl as cl
import numpy

import sys

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
        self.ctx = cl.Context([self.device])
        self.queue = cl.CommandQueue(self.ctx, properties=cl.command_queue_properties.PROFILING_ENABLE)

        self.compiler = Compiler(self.ctx)

        self.pbo = None

        data = numpy.array(Image.open("test.png").convert("RGBA").getdata(), dtype=numpy.uint8)

#        print data

        self.fb = cl.Image(self.ctx, mf.READ_WRITE | mf.COPY_HOST_PTR, cl.ImageFormat(cl.channel_order.BGRA, cl.channel_type.UNSIGNED_INT8), (self.profile.kernel_dim,)*2, hostbuf=data)
        self.out = cl.Image(self.ctx, mf.READ_WRITE, cl.ImageFormat(cl.channel_order.RGBA, cl.channel_type.UNSIGNED_INT8), (self.profile.kernel_dim,)*2)

        data =  0.0 * numpy.ones((512 * 512 * 2.0))

        cl.enqueue_read_image(self.queue, self.fb, (0,0,0), (self.profile.kernel_dim, self.profile.kernel_dim, 1), data, 0, 0, None, True).wait()
        
        print str(data)
        
        self.frame_num = 0

        return True


    def __del__(self):
        debug("Deleting Engine")

        self.pbo = None


    def do(self):
        ''' Main event loop '''

        if(not self.pbo):
            return

        block_size = 16

        cl.enqueue_acquire_gl_objects(self.queue, [self.pbo]).wait()
        self.prg.test(self.queue, (self.profile.kernel_dim, self.profile.kernel_dim), 
                      self.fb, self.out, self.pbo, 
                      numpy.int32(self.profile.kernel_dim), numpy.int32(self.frame_num % self.profile.kernel_dim), 
                      local_size=(block_size,block_size)).wait()
        cl.enqueue_release_gl_objects(self.queue, [self.pbo]).wait()

#        cl.enqueue_copy_image(self.queue, self.out, self.fb, (0, 0), (0, 0), (self.profile.kernel_dim,) * 2).wait()

        self.frame_num += 1


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

    def start(self):
        ''' Start engine '''
        info("Starting engine")

        # generate pbo
        self.pbo_ptr = self.interface.renderer.generate_pbo(self.profile.kernel_dim)
        self.pbo = cl.GLBuffer(self.ctx, mf.WRITE_ONLY, self.pbo_ptr.value)

        # compile
        self.compile()


    def compile(self):
        # compile engine kernel
        debug("Compiling kernel")

        self.prg = self.compiler.compile()
        self.kernel = self.prg.test



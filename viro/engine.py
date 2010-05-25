from common.globals import *

from viro import compiler

from common.log import *
set_log("ENGINE")

import pyopencl as cl
import numpy

from viro.compiler_opencl import *

import sys

class Engine(object):
    ''' The Engine object is the applications interface, via cuda, to the graphics hardware.
        It is responsible for the setup and maintenence of the cuda environment and the graphics kernel.
        It communicates to out via a pbo  '''

    def init(self):
        debug("Initializing Engine")
        Globals().load(self)

        debug("Setting up CUDA")

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

        self.device = cl.get_platforms()[0].get_devices()[0]

        self.ctx = cl.Context([self.device])
        self.queue = cl.CommandQueue(self.ctx, properties=cl.command_queue_properties.PROFILING_ENABLE)

        self.compiler = Compiler(self.ctx)

        # create frame buffer
#        self.channel_desc = cudaCreateChannelDesc(32, 32, 32, 32, cudaChannelFormatKindFloat)
#        self.fb = cudaArray_p()
#        cudaMallocArray(byref(self.fb), byref(self.channel_desc), self.profile.kernel_dim, self.profile.kernel_dim)


        # create output_2D
#        self.output_2D, self.output_2D_pitch = c_void_p(), c_uint()
#        cudaMallocPitch(byref(self.output_2D), byref(self.output_2D_pitch),
#                        self.profile.kernel_dim * sizeof(float4), self.profile.kernel_dim)
#        cudaMemset2D(self.output_2D, self.output_2D_pitch, 0, self.profile.kernel_dim * sizeof(float4),
#                     self.profile.kernel_dim)

        self.pbo = None

        return True


    def __del__(self):
        debug("Deleting Engine")


    def do(self):
        ''' Main event loop '''

        block_size = 16

        a_height = block_size
        a_width = block_size

        h_c = numpy.empty((a_height, a_height)).astype(numpy.float32)

        mf = cl.mem_flags

        d_c_buf = cl.Buffer(self.ctx, mf.WRITE_ONLY, size=h_c.nbytes)

        event = self.kernel(self.queue, (a_height,a_height), d_c_buf,
        local_size=(block_size, block_size))
        event.wait()

        cl.enqueue_read_buffer(self.queue, d_c_buf, h_c).wait()

        print str(h_c)

        sys.exit(0)



    ######################################### PUBLIC ##################################################


    def start(self):
        ''' Start engine '''
        info("Starting engine")

        # generate pbo
        self.pbo = self.interface.renderer.generate_pbo(self.profile.kernel_dim)

        # bind pbo to OpenCL

        # compile
        self.compile()


    def compile(self):
        # compile engine kernel - this needs to be generalized
        debug("Compiling kernel")

        self.prg = self.compiler.compile()
        self.kernel = self.prg.test



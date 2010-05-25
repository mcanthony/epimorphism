kernel_code = """
__kernel 
void
matrixMul( __global float4* C)
{
    // Thread index
    int tx = get_local_id(0);
    int ty = get_local_id(1);



}

"""

import pyopencl as cl
import numpy

block_size = 16

ctx = cl.create_some_context()

for dev in ctx.devices:
        assert dev.local_mem_size > 0

queue = cl.CommandQueue(ctx,
        properties=cl.command_queue_properties.PROFILING_ENABLE)

a_height = block_size
a_width = block_size
b_height = a_width
b_width = a_height

h_c = numpy.empty((a_height, a_height)).astype(numpy.float32)

mf = cl.mem_flags

prg = cl.Program(ctx, kernel_code).build()
kernel = prg.matrixMul

d_c_buf = cl.Buffer(ctx, mf.WRITE_ONLY, size=h_c.nbytes)

event = kernel(queue, (a_height,a_height), d_c_buf,
        local_size=(block_size, block_size))
event.wait()

cl.enqueue_read_buffer(queue, d_c_buf, h_c).wait()

print str(h_c)

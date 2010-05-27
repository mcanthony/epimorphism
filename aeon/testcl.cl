const sampler_t sampler = CLK_NORMALIZED_COORDS_FALSE | CLK_FILTER_NEAREST | CLK_ADDRESS_REPEAT;

__kernel void test(read_only image2d_t fb, write_only image2d_t out, __global char4* g_odata, int kernel_dim, int frame_num)
{
    const int x = get_global_id(0);
    const int y = get_global_id(1);

    //uint4 res = (uint4)((uint)(255.0 * ((frame_num + x) % kernel_dim) / kernel_dim), (uint)(255.0 * ((frame_num + y) % kernel_dim) / kernel_dim), 0, 0);
    //float4 res = read_imagef(fb, sampler, (int2)(x, y));
    uint4 res = read_imageui(fb, sampler, (int2)(x, y));

    //res = (uint4)((res.s0 + val.s0) / 2.0,(res.s1 + val.s1) / 2.0,(res.s2 + val.s2) / 2.0,(res.s3 + val.s3) / 2.0);

    //write_imageui(out, (int2)(x, y), res);

    //uchar4 tmp = (uchar4)(255 * res.s3, 255 * res.s1, 255 * res.s2, 255 * res.s3);

    uchar4 tmp = (uchar4)(res.s0, res.s1, res.s2, res.s3);

    g_odata[y * kernel_dim + x] = tmp;

}

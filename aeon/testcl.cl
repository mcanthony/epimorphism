const sampler_t sampler = CLK_NORMALIZED_COORDS_TRUE | CLK_FILTER_NEAREST | CLK_ADDRESS_REPEAT;

uint4 seed(float2 z, float t){
  z = 0.5f * z + (float2)(0.5f, 0.5f) + (float2)(t, t);
  z = fmod(z, (float2)(1.0f, 1.0f));
  return (uint4)((uint)(255.0 * z.s0), (uint)(255.0 * z.s1), 0, 255);
}


__kernel void test(read_only image2d_t fb, write_only image2d_t out, __global char4* g_odata, int kernel_dim, int frame_num)
{
    const int x = get_global_id(0);
    const int y = get_global_id(1);

    float2 z = (float2)(2.0f / kernel_dim) * (float2)(x, y) + (float2)(1.0f / kernel_dim - 1.0f, 1.0f / kernel_dim - 1.0f);

    uint4 seed_val = seed(z, (float)frame_num / kernel_dim);
    uint4 prev = read_imageui(fb, sampler, (int2)(x, y));

    //uint4 res = (uint4)((prev.s0 + seed_val.s0) / 2.0,(prev.s1 + seed_val.s1) / 2.0,(prev.s2 + seed_val.s2) / 2.0, 255);
    uint4 res = seed_val;

    uchar4 tmp = (uchar4)(res.s0, res.s1, res.s2, res.s3);

    write_imageui(out, (int2)(x, y), res);
    g_odata[y * kernel_dim + x] = tmp;

}

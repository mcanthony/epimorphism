const sampler_t sampler = CLK_NORMALIZED_COORDS_TRUE | CLK_FILTER_NEAREST | CLK_ADDRESS_REPEAT;

uint4 seed(float2 z, float t){
  z = z + (float2)(t, 0);
  z = fmod(z, (float2)(1.0f, 1.0f));
  
  if(z.s0 > 0.9 ||z.s0 < -0.9 || z.s1 > 0.9 || z.s1 < -0.9)
    return (uint4)(255, 0, 0, 255);

  else
    return (uint4)(0, 0, 0, 0);

}


__kernel void test(read_only image2d_t fb, write_only image2d_t out, __global char4* g_odata, int kernel_dim, int frame_num)
{
    const int x = get_global_id(0);
    const int y = get_global_id(1);

    //    float2 z = (float2)(2.0f / kernel_dim) * (float2)(x, y) + (float2)(1.0f / kernel_dim - 1.0f, 1.0f / kernel_dim - 1.0f);

    //    uint4 seed_val = seed(z, (float)frame_num / kernel_dim);


    //    float2 prev_idxf = kernel_dim * (0.5f * z + (float2)(0.5f, 0.5f));
    //int2 prev_idx = (int2)(prev_idxf.s0, prev_idxf.s1);
    //uint4 prev = read_imageui(fb, sampler, prev_idx);
    uint4 res = read_imageui(fb, sampler, (int2)(x,y));

    //uint4 res = (uint4)((prev.s0 + seed_val.s0) / 2.0,(prev.s1 + seed_val.s1) / 2.0,(prev.s2 + seed_val.s2) / 2.0, 255);
    //uint4 res = seed_val;
    //uint4 res = prev;
    //uint4 res = (uint4)((uint)(255.0 * prev_idx.x / kernel_dim), (uint)(255.0 * prev_idx.y / kernel_dim), 0,255);

    uchar4 tmp = (uchar4)(res.s0, res.s1, res.s2, res.s3);

    write_imageui(out, (int2)(x, y), res);
    g_odata[y * kernel_dim + x] = tmp;

}

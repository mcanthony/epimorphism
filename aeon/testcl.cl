const sampler_t sampler = CLK_NORMALIZED_COORDS_TRUE | CLK_FILTER_LINEAR | CLK_ADDRESS_REPEAT;

uint4 seed(float2 z, float t){
  z = (z + (float2)(1.0f, 1.0f)) / 2.0f;
  z = z + (float2)(t, 0);
  z = fmod(z, (float2)(1.0f, 1.0f));
  z = (2.0 * z - (float2)(1.0f, 1.0f));
  
  if(z.s0 > 0.9 ||z.s0 < -0.9 || z.s1 > 0.9 || z.s1 < -0.9)
    return (uint4)(255, 0, 0, 255);

  else
    return (uint4)(0, 0, 0, 0);

}


__kernel void test(read_only image2d_t fb, write_only image2d_t out, __global char4* pbo, int kernel_dim, int frame_num, 
		   float time, __constant float *par, __constant float *internal, __constant int *indices, __constant float2 *zn, float switch_time)
{
    const int x = get_global_id(0);
    const int y = get_global_id(1);
    int2 p = (int2)(x, y);
    float2 z = (float2)(2.0f / kernel_dim) * convert_float2(p) + (float2)(1.0f / kernel_dim - 1.0f, 1.0f / kernel_dim - 1.0f);

    uint4 seed_val = seed(z, (float)frame_num / kernel_dim);

    z *= zn[0].y;
    uint4 prev = read_imageui(fb, sampler, (0.5f * z + (float2)(0.5f, 0.5f)));

    //uint4 res = seed_val;
    //uint4 res = prev;
    uint4 res = (prev + seed_val) / 2; //(uint4)((prev.s0 + seed_val.s0) / 2.0, (prev.s1 + seed_val.s1) / 2.0, (prev.s2 + seed_val.s2) / 2.0, 255);
    write_imageui(out, p, res);

    uchar4 tmp = convert_uchar4(res);//(res.s0, res.s1, res.s2, res.s3);
    pbo[y * kernel_dim + x] = tmp;

}

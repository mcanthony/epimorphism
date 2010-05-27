#include "util.cl"

#define PI 3.1415926535f
#define $i (float2)(0.0, 1.0)
#define $l (float2)(1.0, 0.0)

#include "math.cl"

%PAR_NAMES%

%CULL_ENABLED%

const sampler_t sampler = CLK_NORMALIZED_COORDS_TRUE | CLK_FILTER_LINEAR | CLK_ADDRESS_REPEAT;


float4 seedf(float2 z, float t){  
  if(z.s0 > 0.9 ||z.s0 < -0.9 || z.s1 > 0.9 || z.s1 < -0.9)
    return (float4)(1.0f, 0.0f, 0.0f, 1.0f);

  else
    return (float4)(0.0f, 0.0f, 0.0f, 0.0f);

}


__kernel __attribute__((reqd_work_group_size(16,16,1))) 
void test(read_only image2d_t fb, write_only image2d_t out, __global char4* pbo, int kernel_dim, int frame_num, float time, float switch_time,
	  __constant float *par, __constant float *internal, __constant int *indices, __constant float2 *zn){
  // get coords
  const int x = get_global_id(0);
  const int y = get_global_id(1);
  int2 p = (int2)(x, y);

  // get z
  float2 z = (float2)(2.0f / kernel_dim) * convert_float2(p) + (float2)(1.0f / kernel_dim - 1.0f, 1.0f / kernel_dim - 1.0f);

  // compute seed
  float4 seed = seedf(z, (float)frame_num / kernel_dim);

  // compute T
  z = M(z, zn[0]) + zn[1];


  // get prev
  float4 prev = convert_float4(read_imageui(fb, sampler, (0.5f * z + (float2)(0.5f, 0.5f)))) / 255.0f;

  // blend
  float4 res = (seed.w * seed + (1.0 - seed.w) * prev) * 0.9;

  // write to out
  write_imageui(out, p, convert_uint4(255.0f * res));

  // write to pbo
  uchar4 tmp = convert_uchar4(255.0f * res);
  pbo[y * kernel_dim + x] = tmp;

}


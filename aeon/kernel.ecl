#define _EPI_

#define KERNEL_DIM %KERNEL_DIM%
#define FRACT %FRACT%

#include "util.cl"

#define PI 3.1415926535f
#define $i (float2)(0.0, 1.0)
#define $l (float2)(1.0, 0.0)
%PAR_NAMES%
%CULL_ENABLED%
#include "math.cl"
#include "colorspace.cl"
#include "color.cl"
#include "reduce.cl"

const sampler_t sampler = CLK_NORMALIZED_COORDS_TRUE | CLK_FILTER_LINEAR | CLK_ADDRESS_REPEAT;

float4 seedf(float2 z, float t){  
  z = torus_reduce(z);

  if(z.s0 > 0.9 ||z.s0 < -0.9 || z.s1 > 0.9 || z.s1 < -0.9)
    return color(1.0f, 0.0f, 0.0f, 1.0f);

  else
    return color(0.0f, 0.0f, 0.0f, 0.0f);

}


__kernel __attribute__((reqd_work_group_size(16,16,1))) 
void test(read_only image2d_t fb, write_only image2d_t out, __global char4* pbo, float time, float switch_time,
	  __constant float *par, __constant float *internal, __constant int *indices, __constant float2 *zn){
  // get coords
  const int x = get_global_id(0);
  const int y = get_global_id(1);
  int2 p = (int2)(x, y);

  // get z
  float2 z = (float2)(2.0f / KERNEL_DIM) * convert_float2(p) + (float2)(1.0f / KERNEL_DIM - 1.0f, 1.0f / KERNEL_DIM - 1.0f);
  float2 z_z = z;

  // internal antialiasing
  float4 v = color(0.0f, 0.0f, 0.0f, 0.0f);
  const float i_k = FRACT == 1 ? 0.0f : 1.0f / KERNEL_DIM;  
  const float m_k = FRACT == 1 ? 1.0f : 1.0001f / KERNEL_DIM;  
  const float inc = FRACT == 1 ? 1.0f : 2.0f / (KERNEL_DIM * (FRACT - 1.0f));  

  for(z.x = z_z.x - i_k; z.x < z_z.x + m_k; z.x += inc)
    for(z.y = z_z.y - i_k; z.y < z_z.y + m_k; z.y += inc){
      float2 z_c = z;

      // compute T
      z_c = M(z_c, zn[0]) + zn[1];
      //z_c = D($l, z_c);
      z_c = sinz(z_c);

      // compute seed
      float4 seed = seedf(z_c, time);

      // get frame
      float4 frame = convert_float4(read_imageui(fb, sampler, (0.5f * z_c + (float2)(0.5f, 0.5f)))) / 255.0f;

      // blend
      v += (seed.w * seed + (1.0 - seed.w) * frame);
    }

  const float i_n_sq = 1.0f / (FRACT * FRACT);
  v = i_n_sq * v;
  v.w = v.w / i_n_sq;

  //v = gbr_id(v, z_z, par, time);
  v = rotate_hsls(v, z_z, par, time);

  // write to out
  write_imageui(out, p, convert_uint4(255.0f * v));

  // write to pbo
  uchar4 tmp = convert_uchar4(255.0f * v);
  pbo[y * KERNEL_DIM + x] = tmp;

}


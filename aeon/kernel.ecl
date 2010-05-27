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
#include "reset.cl"
#include "seed_w.cl"
#include "seed_a.cl"
#include "seed_c.cl"
#include "seed_wt.cl"

const sampler_t sampler = CLK_NORMALIZED_COORDS_TRUE | CLK_FILTER_LINEAR | CLK_ADDRESS_REPEAT;

float4 seedf(float2 z, float t){  
  if(z.s0 > 0.9 ||z.s0 < -0.9 || z.s1 > 0.9 || z.s1 < -0.9)
    return (float4)(1.0f, 0.0f, 0.0f, 1.0f);
  else
    return (float4)(0.0f, 0.0f, 0.0f, 0.0f);

}

__kernel __attribute__((reqd_work_group_size(16,16,1))) 
void reset(read_only image2d_t fb, write_only image2d_t out, __global char4* pbo, float time, float switch_time,
	   __constant float *par, __constant float *internal, __constant int *indices, __constant float2 *zn){

  // get coords
  const int x = get_global_id(0);
  const int y = get_global_id(1);
  int2 p = (int2)(x, y);

  // vars
  float intrp_t;
  float4 reset, reset0, reset1;

  // reset
  %RESET%
  write_imageui(out, p, convert_uint4(255.0f * reset));  
}

__kernel __attribute__((reqd_work_group_size(16,16,1))) 
void epimorph(read_only image2d_t fb, write_only image2d_t out, __global char4* pbo, float time, float switch_time,
	      __constant float *par, __constant float *internal, __constant int *indices, __constant float2 *zn){
  // get coords
  const int x = get_global_id(0);
  const int y = get_global_id(1);
  int2 p = (int2)(x, y);

  // intrp_t
  float intrp_t;

  // get z
  float2 z = (float2)(2.0f / KERNEL_DIM) * convert_float2(p) + (float2)(1.0f / KERNEL_DIM - 1.0f, 1.0f / KERNEL_DIM - 1.0f);
  float2 z_z = z;

  // internal antialiasing
  float4 v = (float4)(0.0f, 0.0f, 0.0f, 0.0f);
  const float i_k = FRACT == 1 ? 0.0f : 1.0f / KERNEL_DIM;  
  const float m_k = FRACT == 1 ? 1.0f : 1.0001f / KERNEL_DIM;  
  const float inc = FRACT == 1 ? 1.0f : 2.0f / (KERNEL_DIM * (FRACT - 1.0f));  
  float2 t, t0, t1, t_seed, t_seed0, t_seed1, reduce, reduce0, reduce1;
  float4 seed, seed0, seed1, color, color0, color1;

  for(z.x = z_z.x - i_k; z.x < z_z.x + m_k; z.x += inc)
    for(z.y = z_z.y - i_k; z.y < z_z.y + m_k; z.y += inc){
      float2 z_c = z;

      // compute T
      z = M(zn[2], z) + zn[3];
      %REDUCE%
      z = reduce;
      %T%
      z = t;
      %REDUCE%
      z = recover2(reduce);      

      // compute seed
      z = M(zn[10], (z - zn[11]));

      %T_SEED%
      z = t_seed;
      z = M(zn[8], (z - zn[9]));
      %REDUCE%
      z = recover2(reduce);
      float4 seed = seedf(z, time);

      seed = _gamma3(seed, _COLOR_GAMMA);

      // get framer
      float4 frame = convert_float4(read_imageui(fb, sampler, (0.5f * z + (float2)(0.5f, 0.5f)))) / 255.0f;

    
      // cull mode
      #ifdef CULL_ENABLED

      float new_w;

      if(frame.w >= 0.0f)
	new_w = (1.0 - seed.w) * (frame.w + 1.0f);
      else
	if(seed.w < 0.0001f)
	  new_w = frame.w;
	else
	  new_w = 0.0f;

      frame.w = new_w;

      int null = (frame.w < 0.0f || v.w < 0.0f);

      v += seed.w * seed + (1.0 - seed.w) * frame;      

      if(null)
	v.w = -10000000.0f;
      
      if(_CULL_DEPTH != 0.0f){

	if(v.w > 20 * _CULL_DEPTH - 0.000001)
	  v = (float4)(0.0f, 0.0f, 0.0f, -10000000.0f);
      }

      #else

      // blend
      v += seed.w * seed + (1.0 - seed.w) * frame;      

      #endif

      z = z_c;
    }

  const float i_n_sq = 1.0f / (FRACT * FRACT);
  v = i_n_sq * v;
  v.w = v.w / i_n_sq;

  %COLOR%;
  v = (1.0f - _COLOR_KILL) * color;

  // write to out
  write_imageui(out, p, convert_uint4(255.0f * v));

  // write to pbo
  uchar4 tmp = convert_uchar4(255.0f * v);
  pbo[y * KERNEL_DIM + x] = tmp;

}


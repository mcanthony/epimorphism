const sampler_t sampler = CLK_NORMALIZED_COORDS_TRUE | CLK_FILTER_LINEAR | CLK_ADDRESS_CLAMP_TO_EDGE;
const sampler_t image_sampler = CLK_NORMALIZED_COORDS_FALSE | CLK_FILTER_NEAREST | CLK_ADDRESS_CLAMP_TO_EDGE;

#define _EPI_
#define KERNEL_DIM %KERNEL_DIM%
#define FRACT %FRACT%
#define PI 3.1415926535f
%PAR_NAMES%
%CULL_ENABLED%
#define $i (float2)(0.0, 1.0)
#define $l (float2)(1.0, 0.0)
#include "util.cl"
#include "math.cl"
#include "colorspace.cl"
#include "color.cl"
#include "reduce.cl"
#include "seed_a.cl"
#include "seed_c.cl"
#include "seed_wt.cl"
#include "seed_w.cl"
#include "__seed.cl"
#include "cull.cl"

__kernel __attribute__((reqd_work_group_size(16,16,1))) 
void epimorph(read_only image2d_t fb, write_only image2d_t out, __global char4* pbo, float time, float switch_time,
	      __constant float *par, __constant float *internal, __constant int *indices, __constant float2 *zn){
  float intrp_t;
  float2 t, t0, t1, t_seed, t_seed0, t_seed1, reduce, reduce0, reduce1;
  float4 seed, seed0, seed1, color, color0, color1;

  // get coords
  const int x = get_global_id(0);
  const int y = get_global_id(1);
  int2 p = (int2)(x, y);

  // get z
  float2 z = (float2)(2.0f / KERNEL_DIM) * convert_float2(p) + (float2)(1.0f / KERNEL_DIM - 1.0f, 1.0f / KERNEL_DIM - 1.0f);
  float2 z_z = z;

  // internal antialiasing
  float4 v = (float4)(0.0f, 0.0f, 0.0f, 0.0f);
  const float i_k = (FRACT == 1 ? 0.0f : 0.5f / KERNEL_DIM);  
  const float inc = 1.0f / (KERNEL_DIM * (FRACT - 1.0f));  

  for(int i_x = 0; i_x < (int)FRACT; i_x++)
    for(int i_y = 0; i_y < (int)FRACT; i_y++){
      z = CX(z_z.x - i_k + i_x * inc, z_z.y - i_k + i_y * inc);
      float2 z_c = z;

      // compute T      
      z = M(zn[2], z) + zn[3];
      %REDUCE%
      z = reduce;
      %T%
      z = t;
      z = M(zn[0], z) + zn[1];
      %REDUCE%
      z = recover2(reduce);      
      
      // get frame
      float4 frame = read_imagef(fb, sampler, (0.5f * z + (float2)(0.5f, 0.5f)));

      // compute seed    
      z = M(zn[10], (z - zn[11]));           
      %T_SEED%
      z = t_seed;
      z = M(zn[8], (z - zn[9]));
      %REDUCE%
      z = recover2(reduce);
      %SEED%
      seed = _gamma3(seed, _COLOR_GAMMA);      

      // cull & blending
      #ifdef CULL_ENABLED
      v = cull(v, seed, frame, par);
      #else      
      v += seed.w * seed + (1.0 - seed.w) * frame;      
      #endif

      z = z_c;
    }

  // scale
  v /= (FRACT * FRACT);
  v.w *= (FRACT * FRACT);

  v = recover4(v);
  // compute color
  %COLOR%;

  color = recover4(color);
  // write to out
  write_imagef(out, p, color);

  // write to pbo
  if(_POST_PROCESSING == 0.0f)
    pbo[y * KERNEL_DIM + x] = convert_uchar4(255.0f * color.zyxw);
  //float val = (color.w) / 20;//-1.0f / (color.w / 5 + 1.0f) + 1.0f;
  //pbo[y * KERNEL_DIM + x] = convert_uchar4(255.0f * (float4)(val, 0.0, 0.0, 0.0));

}

__kernel __attribute__((reqd_work_group_size(16,16,1))) 
void get_image(read_only image2d_t fb, write_only image2d_t out){
  const int x = get_global_id(0);
  const int y = get_global_id(1);
  int2 p = (int2)(x, y);

  float4 frame = read_imagef(fb, image_sampler, p);
  frame.w = 1.0;

  write_imageui(out, p, convert_uint4(255.0 * frame).zyxw);
}

//__kernel __attribute__((reqd_work_group_size(16,16,1))) 
//void post_process(read_only image2d_t fb, __global char4* pbo, float time, __constant float* par){

  // get coords
  //  const int x = get_global_id(0);
  // const int y = get_global_id(1);
  //int2 p = (int2)(x, y);

  //float4 v = read_imagef(fb, image_sampler, p);
  //float4 polar = to_rpp(v);
  //float z0 = to_xyz(polar + (float4)(0.0f, -1.0f * _POST_PHI0, PI / 2.0f + _POST_PSI0, 0.0f)).z;
  //v = to_xyz(to_rpp(v));

  //v = (float4)((z0 + 1.0f) / 2.0f, 0.0, 0.0,  v.w);

  /*
  float4 axis0 = (float4)(_POST_PHI0, _POST_PSI0, 1f, 0.0f);
  float4 axis2 = (float4)(_POST_PHI1, _POST_PSI1, 1f, 0.0f);
  float4 axis3 = (float4)(_POST_PHI2, _POST_PSI2, 1f, 0.0f);
  */



  /*
  const int x = get_global_id(0);
  const int y = get_global_id(1);
  int2 p = (int2)(x, y);

  float4 frame00 =  0.0f * read_imagef(fb, image_sampler, p + (int2)(-1,-1));
  float4 frame01 = -1.0f * read_imagef(fb, image_sampler, p + (int2)(-1,0));
  float4 frame02 =  0.0f * read_imagef(fb, image_sampler, p + (int2)(-1,1));
  float4 frame10 = -1.0f * read_imagef(fb, image_sampler, p + (int2)(0,-1));
  float4 frame11 =  5.0f * read_imagef(fb, image_sampler, p + (int2)(0,0));
  float4 frame12 = -1.0f * read_imagef(fb, image_sampler, p + (int2)(0,1));
  float4 frame20 =  0.0f * read_imagef(fb, image_sampler, p + (int2)(1,-1));
  float4 frame21 = -1.0f * read_imagef(fb, image_sampler, p + (int2)(1,0));
  float4 frame22 =  0.0f * read_imagef(fb, image_sampler, p + (int2)(1,1));

  float4 frame = 
    frame00 + frame01 + frame02 + 
    frame10 + frame11 + frame12 + 
    frame20 + frame21 + frame22;

  */

  //pbo[y * KERNEL_DIM + x] = convert_uchar4(255.0 * v.zyxw);
//}


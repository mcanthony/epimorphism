// test

const sampler_t sampler = CLK_NORMALIZED_COORDS_TRUE | CLK_FILTER_LINEAR | CLK_ADDRESS_CLAMP_TO_EDGE;
const sampler_t image_sampler = CLK_NORMALIZED_COORDS_FALSE | CLK_FILTER_NEAREST | CLK_ADDRESS_CLAMP_TO_EDGE;

#define _EPI_
#define KERNEL_DIM %KERNEL_DIM%
#define PI 3.1415926536f
%PAR_NAMES%

#define $i (float2)(0.0, 1.0)
#define $l (float2)(1.0, 0.0)
#include "util.cl"
#include "math.cl"
#include "colorspace.cl"


__kernel __attribute__((reqd_work_group_size(16,16,1))) 
void test(__global uchar4* pbo, float time, float intrp_time, 
	  __constant float *par, __constant float *internal, __constant float2 *zn){
  // get coords
  const int x = get_global_id(0);
  const int y = get_global_id(1);
  int2 p = (int2)(x, y);

  // get z
  float2 z = (float2)(2.0f / KERNEL_DIM) * convert_float2(p) + (float2)(1.0f / KERNEL_DIM - 1.0f, 1.0f / KERNEL_DIM - 1.0f);

  float4 color = HSVtoRGB((float4)(2 * PI * z.x, 1.0f, (z.y + 1.0) / 2.0, 0.0f));

  // assign pbo
  pbo[y * KERNEL_DIM + x] = convert_uchar4(255.0f * color.zyxw);

}

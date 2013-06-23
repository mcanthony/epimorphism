// test

const sampler_t sampler = CLK_NORMALIZED_COORDS_TRUE | CLK_FILTER_LINEAR | CLK_ADDRESS_CLAMP_TO_EDGE;
const sampler_t image_sampler = CLK_NORMALIZED_COORDS_FALSE | CLK_FILTER_NEAREST | CLK_ADDRESS_CLAMP_TO_EDGE;


__kernel __attribute__((reqd_work_group_size(16,16,1))) 
void test(__global uchar4* pbo, write_only image2d_t out, read_only image3d_t aux, 
	  __constant float *par, __constant float *internal, __constant float2 *zn, float time){
  // get p in [0..$KERNEL_DIM]x[0..$KERNEL_DIM]
  const int x = get_global_id(0);
  const int y = get_global_id(1);
  int2 p = (int2)(x, y);

  // get z in [-1..1]x[-1..1]
  float2 z = (float2)(2.0f / $KERNEL_DIM$) * convert_float2(p) + (float2)(1.0f / $KERNEL_DIM$ - 1.0f, 1.0f / $KERNEL_DIM$ - 1.0f);

  // generate color(z)
  float4 color = HSVtoRGB((float4)(2 * PI * z.x, 1.0f, (z.y + 1.0) / 2.0, 0.0f));

  // write out color
  #ifdef $POST_PROCESS$
  write_imagef(out, p, color);   
  #else
  pbo[y * $KERNEL_DIM$ + x] = convert_uchar4(255.0f * color.zyxw);
  #endif
}


// optional post processing.  must be enable in app configuration
__kernel __attribute__((reqd_work_group_size(16,16,1))) 
void post_process(__global uchar4* pbo, read_only image2d_t out, float time, __constant float* par){

  // get coords
  const int x = get_global_id(0);
  const int y = get_global_id(1);
  int2 p = (int2)(x, y);

  float4 v = read_imagef(out, image_sampler, p);

  float4 color = v;
  pbo[y * $KERNEL_DIM$ + x] = convert_uchar4(255.0 * color.xyzw);
}

// julia

const sampler_t sampler = CLK_NORMALIZED_COORDS_TRUE | CLK_FILTER_LINEAR | CLK_ADDRESS_CLAMP_TO_EDGE;
const sampler_t image_sampler = CLK_NORMALIZED_COORDS_FALSE | CLK_FILTER_NEAREST | CLK_ADDRESS_CLAMP_TO_EDGE;


__kernel __attribute__((reqd_work_group_size(16,16,1))) 
void julia(__global uchar4* pbo, write_only image2d_t out, read_only image2d_t aux, 
	  __constant float *par, __constant float *internal, __constant float2 *zn, float time){
  // get coords
  const int x = get_global_id(0);
  const int y = get_global_id(1);
  int2 p = (int2)(x, y);

  // get z
  float2 z_c = 1.0 * ((float2)(2.0f / $KERNEL_DIM$) * convert_float2(p) + (float2)(1.0f / $KERNEL_DIM$ - 1.0f, 1.0f / $KERNEL_DIM$ - 1.0f));
  float2 z = z_c;
  
  float4 color;

  int i = 0;
  int max_iter = 600;
  float escape_rad = 4;

  float fx = z.x;
  float fy = z.y;
  float t;


  while(i < max_iter && z.x * z.x + z.y * z.y < escape_rad){
    z = M(z, z) + zn[0];

    i += 1;
  }

  float mu = i - (native_log(native_log(native_sqrt(z.x * z.x + z.y * z.y))))/ native_log(2.0f);

  if(i == max_iter)
    color = (float4)(0.0,0.0,0.0,0.0);
  else
    color = HSVtoRGB((float4)(mu / 500 + 0.5, 1.0, 1.0, 1.0));


  // write out value
  #ifdef $POST_PROCESS$
  write_imagef(out, p, color);   
  #else
  pbo[y * $KERNEL_DIM$ + x] = convert_uchar4(255.0f * color.zyxw);
  #endif
}


#ifdef $POST_PROCESS$
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
#endif

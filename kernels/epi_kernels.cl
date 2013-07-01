// EPIMORPHISM kernel file

const sampler_t sampler = CLK_NORMALIZED_COORDS_TRUE | CLK_FILTER_LINEAR | CLK_ADDRESS_CLAMP_TO_EDGE;
// const sampler_t image_sampler = CLK_NORMALIZED_COORDS_FALSE | CLK_FILTER_NEAREST | CLK_ADDRESS_CLAMP_TO_EDGE;

__kernel __attribute__((reqd_work_group_size(16,16,1))) 
void epimorphism(read_only image2d_t fb, __global uchar4* pbo, write_only image2d_t out, read_only image3d_t aux,
		 __constant float* par, __constant float *internal, __constant float2 *zn, float time){
	
  float2 t, t_seed, reduce;
  float4 color;

  // get coords
  const int x = get_global_id(0);
  const int y = get_global_id(1);
  int2 p = (int2)(x, y);

  // get z
  float2 z = (float2)(2.0f / $KERNEL_DIM$) * convert_float2(p) + (float2)(1.0f / $KERNEL_DIM$ - 1.0f, 1.0f / $KERNEL_DIM$ - 1.0f);
  float2 z_z = z;
  
  // internal antialiasing
  float4 v = (float4)(0.0f, 0.0f, 0.0f, 0.0f);
  const float i_k = ($FRACT$ == 1 ? 0.0f : 1.0f / $KERNEL_DIM$);  
  const float inc = ($FRACT$ == 1 ? 0.0f : 2.0f / ($KERNEL_DIM$ * ($FRACT$ - 1.0f)));  
	
	
  // scale

  v = recover4(v);

  // compute color  
  color = recover4($COLOR$);

  //z = tri_reduce(4.0f*z);
  //color = (float4)((z.x + 1.0) / 2.0, (z.y + 1.0) / 2.0,0.0f,0.0f);
  //float val = (color.w) / 20;//-1.0f / (color.w / 5 + 1.0f) + 1.0f;
  //pbo[y * $KERNEL_DIM$ + x] = convert_uchar4(255.0f * (float4)(val, 0.0, 0.0, 0.0));
  //pbo[y * $KERNEL_DIM$ + x] = (char4)(0,0,255,255);

  //color.w = 1.0f;

  // write out value
  write_imagef(out, p, color);   
  #ifndef $POST_PROCESS$
  pbo[y * $KERNEL_DIM$ + x] = convert_uchar4(255.0f * color.zyxw);
  #endif

}


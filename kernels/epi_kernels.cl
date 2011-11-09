// EPIMORPHISM kernel file

const sampler_t sampler = CLK_NORMALIZED_COORDS_TRUE | CLK_FILTER_LINEAR | CLK_ADDRESS_CLAMP_TO_EDGE;
const sampler_t image_sampler = CLK_NORMALIZED_COORDS_FALSE | CLK_FILTER_NEAREST | CLK_ADDRESS_CLAMP_TO_EDGE;

__kernel __attribute__((reqd_work_group_size(16,16,1))) 
void epimorphism(read_only image2d_t fb, __global uchar4* pbo, write_only image2d_t out, read_only image2d_t aux,
		 __constant float *par, __constant float *internal, __constant float2 *zn, float time){
  float2 t, t_seed, reduce;
  float4 seed, color;

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

  for(int i_x = 0; i_x < (int)$FRACT$; i_x++)
    for(int i_y = 0; i_y < (int)$FRACT$; i_y++){
      z = CX(z_z.x - i_k + i_x * inc, z_z.y - i_k + i_y * inc);
      
      // compute T      
      z = M(zn[2], z) + zn[3];
      z = $T$;

      // reduce
      reduce = recover2(torus_reduce(z));
      z = M(zn[0], z) + zn[1];
      z = recover2($REDUCE$);      
      
      // get frame
      float4 frame = read_imagef(fb, sampler, (0.5f * z + (float2)(0.5f, 0.5f)));
     
      // compute seed          
      z = M(zn[10], (z - zn[11]));           
      z = $T_SEED$;
      z = M(zn[8], (z - zn[9]));
      z = recover2($REDUCE$);
      
      seed = $SEED$;

      //int4 aux_v = read_imagei(aux, sampler, (0.5f * z + (float2)(0.5f, 0.5f)));
      //seed = convert_float4(aux_v) / 255.0f;

      seed = _gamma3(seed, _GAMMA);      

      // cull & blending
      #ifdef $CULL_ENABLED$
      v = cull(v, seed, frame, par);
      #else      
      v += seed.w * seed + (1.0 - seed.w) * frame;      
      #endif

    }

  // scale
  v = (float4)(v.xyz / ($FRACT$ * $FRACT$), v.w);
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

#ifdef $POST_PROCESS$
__kernel __attribute__((reqd_work_group_size(16,16,1))) 
void post_process(__global uchar4* pbo, read_only image2d_t fb, float time, __constant float* par){

  // get coords
  const int x = get_global_id(0);
  const int y = get_global_id(1);
  int2 p = (int2)(x, y);

  float4 v = read_imagef(fb, image_sampler, p);

  v = RGBtoHSV(v);

  float h = v.x / (2.0 * PI);

  h = 5.9605 * h * h * h - 9.2925 * h * h + 3.332 * h;
  v.x = 2.0 * PI * h;
  v = HSVtoRGB(v);

  pbo[y * $KERNEL_DIM$ + x] = convert_uchar4(255.0 * v.zyxw);
}

//__kernel __attribute__((reqd_work_group_size(16,16,1))) 
//void post_process(read_only image2d_t fb, __global uchar4* pbo, float time, __constant float* par){

  // get coords
  //const int x = get_global_id(0);
  //const int y = get_global_id(1);
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

  //pbo[y * $KERNEL_DIM$ + x] = convert_uchar4(255.0 * v.zyxw);
//}
#endif

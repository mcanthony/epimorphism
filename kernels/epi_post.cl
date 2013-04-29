#ifdef $POST_PROCESS$

const sampler_t post_sampler = CLK_NORMALIZED_COORDS_FALSE | CLK_FILTER_NEAREST | CLK_ADDRESS_CLAMP_TO_EDGE;

__kernel __attribute__((reqd_work_group_size(16,16,1))) 
void post_process(read_only image2d_t fb, __global uchar4* pbo, __constant float* par, float time){

  // get coords
  const int x = get_global_id(0);
  const int y = get_global_id(1);
  int2 p = (int2)(x, y);

  float4 v = read_imagef(fb, post_sampler, p);

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

__kernel __attribute__((reqd_work_group_size(16,16,1))) 
void post_process_colors(read_only image2d_t fb, __global uchar4* pbo, __constant float* par, float time){
  // get coords
  const int x = get_global_id(0);
  const int y = get_global_id(1);
  int2 p = (int2)(x, y);

  float4 v = read_imagef(fb, post_sampler, p);

  v = RGBtoHSV(v);

	float4 c0 = (float4)(1.0,1.0,0.0,0.0);
	float4 c1 = (float4)(1.0,0.27,0.0,0.0);
	float4 c2 = (float4)(0.04,0.37,0.65,0.0);

	float4 res;

	float f;
	if(v.x < 1.0 / 3.0){
		f = 3.0 * v.x;
		res = (1.0 - f) * c0 + f * c1;
	}else if(v.x < 2.0 / 3.0){
		f = 3.0 * v.x - 1.0;
		res = (1.0 - f) * c1 + f * c2;
	}else{
		f = 3.0 * v.x - 2.0;
		res = (1.0 - f) * c2 + f * c0;
	}
	
  res = RGBtoHSV(res);

	v.x = res.x;

	v = HSVtoRGB(v);

  pbo[y * $KERNEL_DIM$ + x] = convert_uchar4(255.0 * v.zyxw);
}

#endif
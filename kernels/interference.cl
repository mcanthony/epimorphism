// interference

const sampler_t sampler = CLK_NORMALIZED_COORDS_TRUE | CLK_FILTER_LINEAR | CLK_ADDRESS_CLAMP_TO_EDGE;
const sampler_t image_sampler = CLK_NORMALIZED_COORDS_FALSE | CLK_FILTER_NEAREST | CLK_ADDRESS_CLAMP_TO_EDGE;

#define MAX_WAVES 30

#define SIN 0
#define P_SIN 1
#define SQUARE 2
#define P_SQUARE 3
#define TRI 4
#define P_TRI 5
#define SAW 6
#define P_SAW 7

#define ENV1 0
#define ENV2 1

float plane_wave(int type, int env, float2 k, float2 z, float w, float time, float ph){

  float a = 1.0f; 

  switch(env){
  case(ENV1):
    a = 1.0f;
    break;
  case(ENV2):
    a = cos(dot(z,z));
    break;
  }
  
  float v = 0.0f;
  float th = dot(k, z) - w * time + ph;
  th = th - floor(th);
  switch(type){
  case SIN:
    v = sin(2.0f * PI * th);
    break;
  case P_SIN:
    v = (1.0f + sin(2.0f * PI * th)) / 2.0f;
    break;
  case SQUARE:
    v = (th < 0.5f ? 1.0f : -1.0f);
    break;
  case P_SQUARE:
    v = (th < 0.5f ? 1.0f : 0.0f);
    break;
  case TRI:
    v = (th < 0.5f ? 4.0f * th - 1.0f: 3.0f - 4.0f * th);
    break;
  case P_TRI:
    v = (th < 0.5f ? 2.0f * th : 2.0f - 2.0f * th);
    break;
  case SAW:
    v = 2.0 * th - 1.0;
    break;
  case P_SAW:
    v = th;
    break;
  }
    
  return a * v;
}


float wrap(float f, int TYPE){
  return plane_wave(TYPE, ENV1, (float2)(1.0f, 0.0f), (float2)(f / 2.0f, 0.0f), 0.0f, 0.0f, 0.0f);
}


float wrapn(float* vals, int num_vals, int TYPE){
  float f = 0.0f;
  for(int i = 0; i < num_vals; i++)
    f += vals[i];  

  return wrap(f, TYPE);
}


__kernel __attribute__((reqd_work_group_size(16,16,1))) 
void interference(read_only image2d_t fb, __global uchar4* pbo, write_only image2d_t out, read_only image3d_t aux,
	      __constant float *par, __constant float *internal, __constant float2 *zn, float time){


  float2 t, z_z;

  // get coords
  const int x = get_global_id(0);
  const int y = get_global_id(1);
  int2 p = (int2)(x, y);

  // get z
  float2 z = (float2)(2.0f / $KERNEL_DIM$) * convert_float2(p) + (float2)(1.0f / $KERNEL_DIM$ - 1.0f, 1.0f / $KERNEL_DIM$ - 1.0f);
  z_z = z;

  // compute val
  float waves[MAX_WAVES];
  for(int i = 0; i <= _SLICES(0); i++){
		float th = i * PI / _SLICES(0);
     
		if(i < _SLICES(0) / 2.0f){
       th -= 1 * (_SLICES(0) / 2.0f - i) * time * 0.01;
     }else if(i > _SLICES(0) / 2.0f){
       th += 1 * (i - _SLICES(0) / 2.0f) * time * 0.01;
     }

     float2 k = (float2)(cos(th), sin(th));

     z = z_z;
     z = M(zn[2], z) + zn[3];
     z = $T$;     
     z = M(zn[0], z) + zn[1];

     waves[i] = plane_wave(_VAL_TYPE(0), ENV1, _N(0) * k, z, time * 0.01, _N(0), 0.0f);
  }


  /*
  float j = 0.0;
  for(int i = 0; i <= _SLICES; i++){
    j+=waves[i];
  }

  float val;
  if(j > 0)
    val = 1.0;
  else
    val = 0.0;
  */

  float val = wrapn(waves, _SLICES(0) + 1, _VAL_WRAP_TYPE(0));
  
  // compute hue
  for(int i = 0; i <= _SLICES(0); i++){
		float th = i * PI / _SLICES(0);

		if(i < _SLICES(0) / 2.0f){
			th -= 1 * (_SLICES(0) / 2.0f - i) * time * 0.01;;
		}else if(i > _SLICES(0) / 2.0f){
			th += 1 * (i - _SLICES(0) / 2.0f) * time * 0.01;;
     }

     float2 k = (float2)(cos(th), sin(th));

     z = z_z;
     z = M(zn[2], z) + zn[3];     
     z = $T$;
     z = M(zn[0], z) + zn[1];

     waves[i] = plane_wave(_HUE_TYPE(0), ENV1, _N(0) * k, z, 2.0f * time * 0.01, _N(0), 0.0f) / 4.0f;
  }

  float hue = wrapn(waves, _SLICES(0) + 1, _HUE_WRAP_TYPE(0));
  
  /*
  // compute rotation
  for(int i = 0; i <= _SLICES; i++){
     float th = i * PI / _SLICES;

     //if(i < _SLICES / 2.0f){
     //  th -= 1 * (_SLICES / 2.0f - i) * _RATE * time;
     //}else if(i > _SLICES / 2.0f){
     //  th += 1 * (i - _SLICES / 2.0f) * _RATE * time;
     //}

     float2 k = (float2)(cos(th), sin(th));

     waves[i] = plane_wave(SIN, ENV1, _N * k, z, 0.5f * time, _N * _RATE, 0.0f) / 2.0f;
  }

  float rot = wrapn(waves, _SLICES + 1, P_TRI);


  // create color
  float4 color = HSVtoRGB((float4)(hue, 1.0f, val, 1.0f));

  color = RGBtoHSLs(color);


  // compute rotation axis
  float phi = rot;
  float psi = 0.0f;//2 * rot;//2.0f * PI / 5.0f;
  float4 axis = (float4)(native_cos(psi) * native_cos(phi), native_cos(psi) * native_sin(phi), native_sin(psi), 0.0f);

  // compute rotation 1  
  float th = rot;//rot;//2.0f * PI / 3.0f;
  //th = remf(CX(th, 0.0f), 2.0f * PI).x;
  color = rotate3D(color, axis, th);

  color = RGBtoHSV(HSLstoRGB(color));
  //color.z = val;
  color = HSVtoRGB(color);
  */

  hue += (M(z, z) + 5 * (cos(time / 2) + 0.5) * cosz(z)).x / 5.0;

  float4 color = HSVtoRGB((float4)(hue, 1.0f, val, 1.0f));

  // write out value
	write_imagef(out, p, color);   
  #ifndef POST_PROCESS
  pbo[y * $KERNEL_DIM$ + x] = convert_uchar4(255.0f * color.zyxw);
  #endif
}

/*
__kernel __attribute__((reqd_work_group_size(16,16,1))) 
void interference_fb(read_only image2d_t fb, __global uchar4* pbo, write_only image2d_t out, read_only image2d_t aux,
		     __constant float *par, __constant float *internal, __constant float2 *zn, float time){


  float2 t, z_z;

  // get coords
  const int x = get_global_id(0);
  const int y = get_global_id(1);
  int2 p = (int2)(x, y);

  // get z
  float2 z = (float2)(2.0f / $KERNEL_DIM$) * convert_float2(p) + (float2)(1.0f / $KERNEL_DIM$ - 1.0f, 1.0f / $KERNEL_DIM$ - 1.0f);
  z_z = z;

  // compute val
  float waves[MAX_WAVES + 1];
  for(int i = 0; i <= _SLICES; i++){
     float th = i * PI / _SLICES;
     
     if(i < _SLICES / 2.0f){
       th -= 1 * (_SLICES / 2.0f - i) * time * 0.01;
     }else if(i > _SLICES / 2.0f){
       th += 1 * (i - _SLICES / 2.0f) * time * 0.01;
     }

     float2 k = (float2)(cos(th), sin(th));

     z = z_z;
     z = M(zn[2], z) + zn[3];
     z = $T$;     
     z = M(zn[0], z) + zn[1];

     waves[i] = plane_wave(_VAL_TYPE, ENV1, _N * k, z, time * 0.01, _N, 0.0f);
  }

  waves[MAX_WAVES] = read_imagef(fb, sampler, (0.5f * z_z + (float2)(0.5f, 0.5f))).x;

  float val = wrapn(waves, _SLICES + 2, _VAL_WRAP_TYPE);
*/
/*

  // compute hue
  for(int i = 0; i <= _SLICES; i++){
     float th = i * PI / _SLICES;

     if(i < _SLICES / 2.0f){
       th -= 1 * (_SLICES / 2.0f - i) * time * 0.01;;
     }else if(i > _SLICES / 2.0f){
       th += 1 * (i - _SLICES / 2.0f) * time * 0.01;;
     }

     float2 k = (float2)(cos(th), sin(th));

     z = z_z;
     z = M(zn[2], z) + zn[3];     
     z = $T$;
     z = M(zn[0], z) + zn[1];

     waves[i] = plane_wave(_HUE_TYPE, ENV1, _N * k, z, 2.0f * time * 0.01, _N, 0.0f) / 4.0f;
  }

  float hue = wrapn(waves, _SLICES + 1, _HUE_WRAP_TYPE);
  float4 color = HSVtoRGB((float4)(hue, 1.0f, val, 1.0f));
  */
/*
  float4 color = (float4)(val, val, val, 1.0);

  // write out value
  #ifdef POST_PROCESS
  write_imagef(out, p, color);   
  #else
  pbo[y * $KERNEL_DIM$ + x] = convert_uchar4(255.0f * color.zyxw);
  #endif
}

#ifdef $POSTPROCESS$
__kernel __attribute__((reqd_work_group_size(16,16,1))) 
void post_process(read_only image2d_t fb, __global uchar4* pbo, float time, __constant float* par){

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
#endif
*/

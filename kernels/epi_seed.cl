// EPIMORPHISM library file
// seed functions

_EPI_ float4 seed_id(int idx, float4 frame, float2 z, read_only image2d_t fb, read_only image3d_t aux, __constant float *par, __constant float *internal, __constant float2 *zn, float time){
  // width, color, alpha, width_trans templated seed family
  // DEV
	return frame;
}


_EPI_ float4 seed_simple(int idx, float4 frame, float2 z, read_only image2d_t fb, read_only image3d_t aux, __constant float *par, __constant float *internal, __constant float2 *zn, float time){
  // width, color, alpha, width_trans templated seed family
  // DEV

  z = grid_reduce(z);

  if(z.x > 0.9 || z.x < -0.9 || z.y > 0.9 || z.y < -0.9)
    return (float4)(1, 1, 0, 1);
  else
    return frame;

}


_EPI_ float4 seed_multi_wca(int idx, float4 frame, float2 z, read_only image2d_t fb, read_only image3d_t aux, __constant float *par, __constant float *internal, __constant float2 *zn, float time){
  // width, color, alpha, width_trans templated seed family
  // DEV

	float4 res, seed;
	float w, a;
	
	switch(idx){
	case 0:
		seed = $SEED_W0$;
		break;
	#ifdef $SEED1$		
	case 1:
		seed = $SEED_W1$;
		break;
	#endif
	#ifdef $SEED2$
	case 2:
		seed = $SEED_W2$;
		break;
	#endif
	}	
	
  w = fmin(seed.x, 1.0f);
	
	switch(idx){
	case 0:
		w = $SEED_WT0$;
		break;
  #ifdef $SEED1$			
	case 1:
		w = $SEED_WT1$;
		break;
  #endif
  #ifdef $SEED2$
	case 2:
		w = $SEED_WT2$;
		break;
	#endif
	}

	seed.x = w;
	
	switch(idx){
	case 0:
		res = $SEED_C0$;
		break;
  #ifdef $SEED1$			
	case 1:
		res = $SEED_C1$;
		break;
  #endif		
	#ifdef $SEED2$
	case 2:
		res = $SEED_C2$;
		break;
	#endif
	}

	switch(idx){
	case 0:
		a = $SEED_A0$;
		break;
	#ifdef $SEED1$		
	case 1:
		a = $SEED_A1$;
		break;
	#endif
	#ifdef $SEED2$
	case 2:
		a = $SEED_A2$;
		break;
	#endif
	}
	
	res.w = a * seed.y;

  return mix(frame, res, res.w);
}


_EPI_ float4 seed_multi(int idx, float4 frame, float2 z, read_only image2d_t fb, read_only image3d_t aux, __constant float *par, __constant float *internal, __constant float2 *zn, float time){
	// multiseed
  // FULL, LIVE, DEV

	float2 z_z = z;
	
	// compute seed0          
	z = M(zn[10], (z - zn[11]));           
	z = $T_SEED0$;
	z = M(zn[8], (z - zn[9]));
	z = recover2($REDUCE$);
	idx = 0;
	frame = $SEED0$;

	// compute seed1
	#ifdef $SEED1$
	z = z_z;
	z = M(zn[14], (z - zn[15]));           
	z = $T_SEED1$;
	z = M(zn[12], (z - zn[13]));
	z = recover2($REDUCE$);
	idx = 1;
	frame = $SEED1$;
	#endif

	// compute seed2
  #ifdef $SEED2$
	z = z_z;
	z = M(zn[18], (z - zn[19]));           
	z = $T_SEED2$;
	z = M(zn[16], (z - zn[17]));
	z = recover2($REDUCE$);
	idx = 2;
	frame = $SEED2$;
	#endif
	
	return frame;

}




  /*	
_EPI_ float4 seed_poly(int idx, float4 frame, float2 z, read_only image2d_t fb, read_only image3d_t aux, __constant float *par, __constant float *internal, __constant float2 *zn, float time){
  // width, color, alpha, width_trans templated seed family
  // DEV


  float4 res;
  float ep = -0.0000001;
  float seed_wt, seed_a;
  float2 seed_w, seed_w0, seed_w1;
  float4 seed_c;
  float w = $SEED_W$.x;

  w = fmax(fmin(w, 1.0f), ep);

  if(w > 0.0f){   
    w = $SEED_WT$;    
    res = $SEED_C$;    
    res.w = $SEED_A$;
  }else{
    res = (float4)(0.0f, 0.0f, 0.0f, 0.0f);
  }

  float hue = (M(z, z) + 5 * (cos(time / 2) + 0.5) * cosz(z)).x / 5.0;

  return HSVtoRGB((float4)(hue, 1.0, 1.0, 0.5));
}
  */


/*
// refactor later
_EPI_ float4 seed_texture(int idx, float2 z, read_only image2d_t fb, read_only image2d_t aux, __constant float *par, __constant float *internal, __constant float2 *zn, float time){
  // width, color, alpha, width_trans templated seed family
  // DEV

  float4 res;
	float ep = -0.0000001;
  float seed_wt, seed_a;
  float4 seed_w, seed_w0, seed_w1;
  float4 seed_c;
	float4 seed = $SEED_W$;
  float w = seed.x;
	
  w = fmax(fmin(w, 1.0f), ep);

  z = torus_reduce(z);

  if(w > 0.0f){
    w = $SEED_WT$;    
    res = $SEED_C$;    

    z /= w / w; //WTF is this?
    float4 res2 = read_imagef(fb, fb_sampler, (0.5f * z + (float2)(0.5f, 0.5f)));    
    res = (0.2f * res + 0.8f * res2);

    res.w = $SEED_A$;
  }else{
    res = (float4)(0.0f, 0.0f, 0.0f, 0.0f);
  }

  return res;
}
*/

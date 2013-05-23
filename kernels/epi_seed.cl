const sampler_t fb_sampler = CLK_NORMALIZED_COORDS_TRUE | CLK_FILTER_LINEAR | CLK_ADDRESS_CLAMP_TO_EDGE;

// EPIMORPHISM library file
// seed functions

_EPI_ float4 seed_simple(int idx, float2 z, read_only image2d_t fb, read_only image2d_t aux, __constant float *par, __constant float *internal, __constant float2 *zn, float time){
  // width, color, alpha, width_trans templated seed family
  // DEV

  z = grid_reduce(z);

  if(z.x > 0.9 || z.x < -0.9 || z.y > 0.9 || z.y < -0.9)
    return (float4)(1, 1, 0, 1);
  else
    return (float4)(0, 0, 0, 0);

}

_EPI_ float4 seed_multi_wca(int idx, float2 z, read_only image2d_t fb, read_only image2d_t aux, __constant float *par, __constant float *internal, __constant float2 *zn, float time){
  // width, color, alpha, width_trans templated seed family
  // FULL, LIVE, DEV

	float4 res, seed_w, seed_c, seed;
  float ep = -0.0000001;
  float seed_wt, seed_a;
	
	switch(idx){
	case 0:
		seed = $SEED_W0$;
		break;
	case 1:
		seed = $SEED_W1$;
		break;
	case 2:
		seed = $SEED_W2$;
		break;
	}
  float w = seed.x;

  w = fmax(fmin(w, 1.0f), ep);

	
  if(w > 0.0f){
		switch(idx){
		case 0:
			w = $SEED_WT0$;
			break;
		case 1:
			w = $SEED_WT1$;
			break;
		case 2:
			w = $SEED_WT2$;
			break;
		}

		seed.x = w; // hrm, why wasn't this there before?

		switch(idx){
		case 0:
			res = $SEED_C0$;
			break;
		case 1:
			res = $SEED_C1$;
			break;
		case 2:
			res = $SEED_C2$;
			break;
		}

		float a;
		switch(idx){
		case 0:
			a = $SEED_A0$;
			break;
		case 1:
			a = $SEED_A1$;
			break;
		case 2:
			a = $SEED_A2$;
			break;
		}
		if(a > 0)
			res.w = a;
  }else{
    res = (float4)(0.0f, 0.0f, 0.0f, 0.0f);
  }
	

  return res;
}

_EPI_ float4 seed_poly(int idx, float2 z, read_only image2d_t fb, read_only image2d_t aux, __constant float *par, __constant float *internal, __constant float2 *zn, float time){
  // width, color, alpha, width_trans templated seed family
  // DEV

  /*
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

  */

  float hue = (M(z, z) + 5 * (cos(time / 2) + 0.5) * cosz(z)).x / 5.0;

  return HSVtoRGB((float4)(hue, 1.0, 1.0, 0.5));
}


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

_EPI_ float4 seed_multi(int idx, float2 z, read_only image2d_t fb, read_only image2d_t aux, __constant float *par, __constant float *internal, __constant float2 *zn, float time){
	// multiseed
  // FULL, LIVE, DEV
	
	// compute seed          
	z = M(zn[10], (z - zn[11]));           
	z = $T_SEED0$;
	z = M(zn[8], (z - zn[9]));
	z = recover2($REDUCE$);

	return $SEED0$; //seed_wca(0, z, fb, aux, par, internal, zn, time);

}

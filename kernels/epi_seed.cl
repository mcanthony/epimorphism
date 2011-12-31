const sampler_t fb_sampler = CLK_NORMALIZED_COORDS_TRUE | CLK_FILTER_LINEAR | CLK_ADDRESS_CLAMP_TO_EDGE;

// EPIMORPHISM library file
// seed functions

_EPI_ float4 seed_simple(read_only image2d_t fb, read_only image2d_t aux, float2 z, __constant float* internal, __constant float* par, float time){
  // width, color, alpha, width_trans templated seed family
  // DEV

  z = grid_reduce(z);

  if(z.x > 0.9 || z.x < -0.9 || z.y > 0.9 || z.y < -0.9)
    return (float4)(1, 1, 0, 1);
  else
    return (float4)(0, 0, 0, 0);

}


_EPI_ float4 seed_aux(read_only image2d_t fb, read_only image2d_t aux, float2 z, __constant float* internal, __constant float* par, float time){
  // width, color, alpha, width_trans templated seed family
  // DEV

  return convert_float4(read_imagei(aux, fb_sampler, (0.5f * z + (float2)(0.5f, 0.5f)))) / 255.0f;

}


_EPI_ float4 seed_wca(read_only image2d_t fb, read_only image2d_t aux, float2 z, __constant float* internal, __constant float* par, float time){
  // width, color, alpha, width_trans templated seed family
  // FULL, LIVE, DEV

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

  return res;
}

_EPI_ float4 seed_poly(read_only image2d_t fb, read_only image2d_t aux, float2 z, __constant float* internal, __constant float* par, float time){
  // width, color, alpha, width_trans templated seed family
  // FULL, LIVE, DEV

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


_EPI_ float4 seed_texture(read_only image2d_t fb, read_only image2d_t aux, float2 z, __constant float* internal, __constant float* par, float time){
  // width, color, alpha, width_trans templated seed family
  // FULL, LIVE, DEV

  float4 res;
  float ep = -0.0000001;
  float seed_wt, seed_a;
  float2 seed_w, seed_w0, seed_w1;
  float4 seed_c;
  float w = $SEED_W$.x;

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


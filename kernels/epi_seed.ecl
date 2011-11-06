// EPIMORPHISM library file
// seed functions

_EPI_ float4 seed_simple(read_only image2d_t fb, float2 z, __constant float* internal, __constant float* par, float time){
  // width, color, alpha, width_trans templated seed family
  // DEV

  z = grid_reduce(z);

  if(z.x > 0.9 || z.x < -0.9 || z.y > 0.9 || z.y < -0.9)
    return (float4)(1, 1, 0, 1);
  else
    return (float4)(0, 0, 0, 0);

}

_EPI_ float4 seed_wca(read_only image2d_t fb, float2 z, __constant float* internal, __constant float* par, float time){
  // width, color, alpha, width_trans templated seed family
  // FULL, LIVE, DEV

  float4 res;
  float ep = -0.0000001;
  float seed_wt, seed_a;
  float2 seed_w, seed_w0, seed_w1;
  float4 seed_c;
  float w = %SEED_W%.x;

  w = fmax(fmin(w, 1.0f), ep);

  if(w > 0.0f){   
    w = %SEED_WT%;    
    res = %SEED_C%;    
    res.w = %SEED_A%;
  }else{
    res = (float4)(0.0f, 0.0f, 0.0f, 0.0f);
  }

  return res;
}


_EPI_ float4 seed_texture(read_only image2d_t fb, float2 z, __constant float* internal, __constant float* par, float time){
  // width, color, alpha, width_trans templated seed family
  // FULL, LIVE, DEV

  float4 res;
  float ep = -0.0000001;
  float seed_wt, seed_a;
  float2 seed_w, seed_w0, seed_w1;
  float4 seed_c;
  float w = %SEED_W%.x;

  w = fmax(fmin(w, 1.0f), ep);

  z = torus_reduce(z);

  if(w > 0.0f){
    w = %SEED_WT%;    
    res = %SEED_C%;    

    z /= w / w; //WTF is this?
    float4 res2 = read_imagef(fb, sampler, (0.5f * z + (float2)(0.5f, 0.5f)));    
    res = (0.2f * res + 0.8f * res2);

    res.w = %SEED_A%;
  }else{
    res = (float4)(0.0f, 0.0f, 0.0f, 0.0f);
  }

  return res;
}


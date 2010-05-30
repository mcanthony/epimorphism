// EPIMORPH library file
// seed functions

_EPI_ float4 seed_wca(read_only image2d_t fb, float2 z, __constant int* indices, __constant float* internal, __constant float* par, float time, float switch_time){
  // width, color, alpha, width_trans templated seed family
  // FULL, LIVE, DEV

  float intrp_t;

  float4 res;
  float ep = -0.0000001;
  float4 seed_c, seed_c0, seed_c1;
  float seed_wt, seed_wt0, seed_wt1, seed_a, seed_a0, seed_a1;
  float2 seed_w, seed_w0, seed_w1;
  %SEED_W%
  float w = seed_w.x;

  w = fmax(fmin(w, 1.0f), ep);

  if(w > 0.0f){
    %SEED_WT%
    w = seed_wt;
    %SEED_C%
    res = seed_c;
    %SEED_A%
    res.w = seed_a;
  }else{
    res = (float4)(0.0f, 0.0f, 0.0f, 0.0f);
  }

  return res;
}


_EPI_ float4 seed_texture(read_only image2d_t fb, float2 z, __constant int* indices, __constant float* internal, __constant float* par, float time, float switch_time){
  // width, color, alpha, width_trans templated seed family
  // FULL, LIVE, DEV

  float intrp_t;

  float4 res;
  float ep = -0.0000001;
  float4 seed_c, seed_c0, seed_c1;
  float seed_wt, seed_wt0, seed_wt1, seed_a, seed_a0, seed_a1;
  float2 seed_w, seed_w0, seed_w1;
  %SEED_W%
  float w = seed_w.x;

  w = fmax(fmin(w, 1.0f), ep);

  z = torus_reduce(z);

  if(w > 0.0f){
    %SEED_WT%
    w = seed_wt;
    %SEED_C%
    res = seed_c;
    z /= w / w;
    float4 res2 = read_imagef(fb, sampler, (0.5f * z + (float2)(0.5f, 0.5f)));
    
    res = (0.2f * res + 0.8f * res2);

    %SEED_A%
    res.w = seed_a;
  }else{
    res = (float4)(0.0f, 0.0f, 0.0f, 0.0f);
  }

  return res;
}

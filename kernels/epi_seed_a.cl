// EPIMORPH library file
// seed alpha functions for the seed_wca seed function
// SUFFIX (idx, w, res, par)

_EPI_ float no_alpha(int idx, float w, float4 res, __constant float* par){
  // none
  // DEV

  return 1.0;
}

_EPI_ float id_alpha(int idx, float w, float4 res, __constant float* par){
  // id
  // DEV

  return res.w;
}

_EPI_ float solid_alpha(int idx, float w, float4 res, __constant float* par){
  // solid
  // FULL, LIVE, DEV

  return _SEED_COLOR_A(idx) * res.w;
}


_EPI_ float linear_alpha(int idx, float w, float4 res, __constant float* par){
  // linear with w
  // DEV

  return w * _SEED_COLOR_A(idx) * res.w;
}


_EPI_ float circular_alpha(int idx, float w, float4 res, __constant float* par){
  // circular with w
  // LIVE, DEV

  return native_sqrt(1.0f - (1.0f - w) * (1.0f - w)) * _SEED_COLOR_A(idx) * res.w;
}

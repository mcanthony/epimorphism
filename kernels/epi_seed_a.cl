// EPIMORPH library file
// seed alpha functions for the seed_wca seed function

_EPI_ float no_alpha(int idx, float w, __constant float* par){
  // solid
  // DEV

  return 1.0;
}

_EPI_ float id_alpha(int idx, float w, __constant float* par){
  // solid
  // DEV

  return -1.0;
}

_EPI_ float solid_alpha(int idx, float w, __constant float* par){
  // solid
  // FULL, LIVE, DEV

  return _SEED_COLOR_A(idx);
}


_EPI_ float linear_alpha(int idx, float w, __constant float* par){
  // linear with w
  // FULL, LIVE, DEV

  return w * _SEED_COLOR_A(idx);
}


_EPI_ float circular_alpha(int idx, float w, __constant float* par){
  // circular with w
  // FULL, LIVE, DEV

  return native_sqrt(1.0f - (1.0f - w) * (1.0f - w)) * _SEED_COLOR_A(idx);
}

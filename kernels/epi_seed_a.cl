// EPIMORPH library file
// seed alpha functions for the seed_wca seed function


_EPI_ float solid_alpha(float w, __constant float* par){
  // solid
  // FULL, LIVE, DEV

  return _COLOR_A;
}


_EPI_ float linear_alpha(float w, __constant float* par){
  // linear with w
  // FULL, LIVE, DEV

  return w * _COLOR_A;
}


_EPI_ float circular_alpha(float w, __constant float* par){
  // circular with w
  // FULL, LIVE, DEV

  return native_sqrt(1.0f - (1.0f - w) * (1.0f - w)) * _COLOR_A;
}

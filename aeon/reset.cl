// EPIMORPH library file
// reset functions

_EPI_ float4 reset_black(int x, int y, __constant float* par){
  // black reset function
  // FULL, LIVE, DEV

  return (float4)(0.0f, 0.0f, 0.0f, -10000000.0f);
}

_EPI_ float4 reset_hsls(int x, int y, __constant float* par){
  // hsls reset function
  // FULL, LIVE, DEV

  float phi = 2.0f * PI * _COLOR_PHI1;
  float psi = 2.0f * PI * _COLOR_PSI1;

  float4 pt = 2.0f * (_HSLS_RESET_Z - 0.5f) * (float4)(native_cos(psi) * native_cos(phi), native_cos(psi) * native_sin(phi), native_sin(psi), 0.0);
  pt.w = -10000000.0f;

  return HSLstoRGB(pt);
}

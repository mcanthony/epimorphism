// EPIMORPH library file
// seed color functions for the seed_wca seed

_EPI_ float4 simple_color(float2 z, float w, __constant float* par, float time){
  // simple coloring function
  // FULL, LIVE, DEV

  float a = 0.0f;

  if(_SEED_C_TH_EFF != 0 && (z.y != 0.0f || z.x != 0.0f)){
    a = atan2(z.y, z.x) * floor(8.0f * _SEED_C_TH_EFF) / (2.0f * PI);
  }
  //return HSVtoRGB((float4)(time * _SEED_COLOR_SPEED * 10.0f + a, _COLOR_S, w * _COLOR_V * ((1.0f + sin(3.0f * 2.0f * 3.14f * z.x)) / 2.0f) * ((1.0f + cos(3.0f * 2.0f * 3.14f * z.y)) / 2.0f), 0.0f));
  return HSVtoRGB((float4)(time * _SEED_COLOR_SPEED * 10.0f + a, _COLOR_S, w * _COLOR_V, 0.0f));
}

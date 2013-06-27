// EPIMORPH library file
// seed color functions for the seed_wca seed

const sampler_t aux_sampler = CLK_NORMALIZED_COORDS_TRUE | CLK_FILTER_LINEAR | CLK_ADDRESS_MIRRORED_REPEAT;

_EPI_ float4 simple_color(int idx, read_only image3d_t aux, float2 z, float4 seed, __constant float* par, float time){
  // simple coloring function
  // FULL, LIVE, DEV

  float a = 0.0f;

  if(_SEED_C_TH_EFF(idx) != 0 && (z.y != 0.0f || z.x != 0.0f)){
    a = atan2(z.y, z.x) * floor(8.0f * _SEED_C_TH_EFF(idx)) / (2.0f * PI);
  }

  return HSVtoRGB((float4)(time * _SEED_COLOR_SPEED(idx) * 0.1f + a + _SEED_COLOR_DHUE(idx), _SEED_COLOR_S(idx), seed.x * _SEED_COLOR_V(idx), 0.0f));

	//return HSVtoRGB((float4)(time * _SEED_COLOR_SPEED * 0.1f + a, _COLOR_S, w * _COLOR_V * ((1.0f + sin(3.0f * 2.0f * 3.14f * z.x)) / 2.0f) * ((1.0f + cos(3.0f * 2.0f * 3.14f * z.y)) / 2.0f), 0.0f));
}


_EPI_ float4 tex_color(int idx, read_only image3d_t aux, float2 z, float4 seed, __constant float* par, float time){
  // simple coloring function
  // FULL, LIVE, DEV
	float2 w = _SEED_TEX_SC(idx) * seed.zw;
	float seed_c = (idx + _SEED_TEX_IDX(idx) + 0.5) / _NUM_AUX;
	float4 c = (float4)(w.x, w.y, seed_c, 0);
  return convert_float4(read_imagei(aux, aux_sampler, c)) / 255.0f;	
}

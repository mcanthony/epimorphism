// EPIMORPH library file
// seed shape functions for the seed_wca seed function

_EPI_ float trans_w(int idx, float w, __constant float* par){
  // EXCLUDE
  if(w < _SEED_W_MIN(idx) && w > 0.0f)
    w = 1.0f;
  if(_SEED_W_BASE(idx) != 0.0f && w < 0.0f)
    w = _SEED_W_BASE(idx);
  return w;
}

_EPI_ float4 solid(int idx, float2 z, __constant float* par){
  // solid
  // DEV

  z = grid_reduce(z);
  float w = 1.0;
  w = trans_w(idx, w, par);
	return (float4)(w, 1.0, z.x, z.y);
}

_EPI_ float4 fade(int idx, float2 z, __constant float* par){
  // linear l-r gradient
  // DEV

  z = grid_reduce(z);
  float w = (z.x + 1.0f) / 2.0f;
  w = trans_w(idx, w, par);
	return (float4)(w, 1.0, z.x, z.y);
}


_EPI_ float4 wave(int idx, float2 z, __constant float* par){
  // sinousoid
  // DEV

  float _clock = 0.0f;

  z = grid_reduce(z);
  float w = (2.0f + native_sin(2.0f * PI * (z.y + _clock / 10.0f))) / 4.0f;
  w = trans_w(idx, w, par);
	return (float4)(w, 1.0, z.x, z.y);
}


_EPI_ float4 circle(int idx, float2 z, __constant float* par){
  // circle
  // FULL, LIVE, DEV

  z = grid_reduce(z);
  float r = native_sqrt(z.x * z.x + z.y * z.y);
  float w = -0.0000001;
	float wx = atan2pi(z.y, z.x) * 3.0;
	float wy = 0.0;
	if(r > _SEED_CIRCLE_R(idx) - _SEED_W(idx) / 2.0f && r  < _SEED_CIRCLE_R(idx) + _SEED_W(idx) / 2.0f){
    w = (1.0f - 2.0f * fabs(r - _SEED_CIRCLE_R(idx)) / _SEED_W(idx));
		wy = (r - _SEED_CIRCLE_R(idx) - _SEED_W(idx) / 2.0f) / _SEED_W(idx);
	}
  w = trans_w(idx, w, par);
	return (float4)(w, 1.0, wx, wy);	
}


_EPI_ float4 lines_lr(int idx, float2 z, __constant float* par){
  // parallel vertical lines
  // FULL, LIVE, DEV

  z = grid_reduce(z);
  float w = -0.0000001;
	float wx = 0.0;
	float wy = z.y / (0.5 * _SEED_W(idx)) - 0.5;
  if(z.x > (1.0f - _SEED_W(idx))){
    w = (z.x - (1.0f - _SEED_W(idx))) / _SEED_W(idx);
	}
  else if(z.x < -1.0f * (1.0f - _SEED_W(idx))){
    w = (-1.0f * (1.0f - _SEED_W(idx)) - z.x) / _SEED_W(idx);
	}
	wx = w;
  w = trans_w(idx, w, par);
	return (float4)(w, 1.0, wx, wy);	
}

_EPI_ float4 lines_inner(int idx, float2 z, __constant float* par){
  // lines in a cross
  // FULL, LIVE, DEV

  z = grid_reduce(z);
  float w = -0.0000001;
	float wx = (z.x + _SEED_W(idx)) / (2.0 * _SEED_W(idx));
	float wy = (z.y + _SEED_W(idx)) / (2.0 * _SEED_W(idx));
  if(fabs(z.x) < _SEED_W(idx))
    w = (1.0f - fabs(z.x) / _SEED_W(idx));
	if(fabs(z.y) < _SEED_W(idx))
    w = fmax(1.0f - fabs(z.x) / _SEED_W(idx), 1.0f - fabs(z.y) / _SEED_W(idx)); 
  w = trans_w(idx, w, par);
	return (float4)(w, 1.0, wx, wy);	
}

_EPI_ float4 square(int idx, float2 z, __constant float* par){
  // central square
  // FULL, LIVE, DEV

  z = grid_reduce(z);
  float w = -0.0000001;
	float wx = 0.0;
	float wy = 0.0;
  if(z.x < _SEED_W(idx) && z.x > -1.0f * _SEED_W(idx) && z.y < _SEED_W(idx) && z.y > -1.0f * _SEED_W(idx)){
    w = fmin((1.0f - fabs(z.x) / _SEED_W(idx)), (1.0f - fabs(z.y) / _SEED_W(idx)));
		wx = (z.x + _SEED_W(idx)) / (2.0 * _SEED_W(idx));
		wy = (z.y + _SEED_W(idx)) / (2.0 * _SEED_W(idx));
  }
	
  w = trans_w(idx, w, par);
	return (float4)(w, 1.0, wx, wy);	
}

_EPI_ float4 lines_box(int idx, float2 z, __constant float* par){
  // 4 lines in a box
  // FULL, LIVE, DEV

  z = grid_reduce(z);
  float w = -0.0000001;
	float wx = (z.x + _SEED_W(idx)) / (2.0 * _SEED_W(idx));
	float wy = (z.y + _SEED_W(idx)) / (2.0 * _SEED_W(idx));
	if(z.x >= z.y && z.x >= -1.0f * z.y && z.x > (1.0f - _SEED_W(idx))){
		w = (z.x - (1.0f - _SEED_W(idx))) / _SEED_W(idx);
		wy = z.y / (0.5 * _SEED_W(idx)) - 0.5;
	}else if(z.y >= z.x && z.y >= -1.0f * z.x && z.y > (1.0f - _SEED_W(idx))){
		w = (z.y - (1.0f - _SEED_W(idx))) / _SEED_W(idx);
		wy = z.x / (0.5 * _SEED_W(idx)) - 0.5;
	}else if(z.y >= z.x && z.y <= -1.0 * z.x && z.x < -1.0f * (1.0f - _SEED_W(idx))){
		w = (-1.0f * (1.0f - _SEED_W(idx)) - z.x) / _SEED_W(idx);
		wy = z.y / (0.5 * _SEED_W(idx)) - 0.5;
	}else if(z.x >= z.y && z.x <= -1.0 * z.y && z.y < -1.0f * (1.0f - _SEED_W(idx))){
		w = (-1.0f * (1.0f - _SEED_W(idx)) - z.y) / _SEED_W(idx);
		wy = z.x / (0.5 * _SEED_W(idx)) - 0.5;
	}
	wx = w;
  w = trans_w(idx, w, par);
	return (float4)(w, 1.0, wx, wy);	
}


_EPI_ float4 lines_box_stag(int idx, float2 z, __constant float* par){
  // 4 lines in a box, staggered
  // FULL, LIVE, DEV

  z = grid_reduce(z);
  float w = -0.0000001;
	float wx = (z.x + _SEED_W(idx)) / (2.0 * _SEED_W(idx));
	float wy = (z.y + _SEED_W(idx)) / (2.0 * _SEED_W(idx));
  if(z.x > (1.0f - _SEED_W(idx)))
    w = (z.x - (1.0f - _SEED_W(idx))) / _SEED_W(idx);
  if(z.y > (1.0f - _SEED_W(idx)))
    w = (z.y - (1.0f - _SEED_W(idx))) / _SEED_W(idx);
  if(z.x < -1.0f * (1.0f - _SEED_W(idx)))
    w = (-1.0f * (1.0f - _SEED_W(idx)) - z.x) / _SEED_W(idx);
  if(z.y < -1.0f * (1.0f - _SEED_W(idx)) && z.x < (1.0f - _SEED_W(idx)))
    w = (-1.0f * (1.0f - _SEED_W(idx)) - z.y) / _SEED_W(idx);
  w = trans_w(idx, w, par);
	return (float4)(w, 1.0, wx, wy);	
}

// refactor me
_EPI_ float4 anti_grid_fade(int idx, float2 z, __constant float* par){
  // inverse grid, radially shaded
  // FULL, LIVE, DEV

  z = grid_reduce(z);
  float w = -0.0000001;
	float wx = 0.0f;
	float wy = 0.0f;
  z = remf(floor(5.0f * _SEED_GRID_N(idx)) / 2.0f * z, 1.0f);
  if((z.x > 0.5f * (1.0f - _SEED_W(idx)) && z.x < 0.5f * (1.0f + _SEED_W(idx))) && (z.y < 0.5f * (1.0f + _SEED_W(idx)) && z.y > 0.5f * (1.0f - _SEED_W(idx)))){
		wx = 0.5 * (2.0f * z.x - 1.0f) / _SEED_W(idx) + 0.5;
		wy = 0.5 * (2.0f * z.y - 1.0f) / _SEED_W(idx) + 0.5;
    w = min((1.0f - 2.0f * fabs(z.y - 0.5f) / _SEED_W(idx)), (1.0f - 2.0f * fabs(z.x - 0.5f) / _SEED_W(idx)));
	}
  w = trans_w(idx, w, par);
	return (float4)(w, 1.0, wx, wy);	
}


// refactor me
_EPI_ float4 grid_fade(int idx, float2 z, __constant float* par){
  // grid, radially shaded
  // FULL, LIVE, DEV

  z = grid_reduce(z);
  float w = -0.0000001;
	float wx = 0.0f;
	float wy = 0.0f;
  z = remf(floor(5.0f * _SEED_GRID_N(idx)) / 2.0f * z, 1.0f);
  if((z.x > 0.5f * (1.0f - _SEED_W(idx)) && z.x < 0.5f * (1.0f + _SEED_W(idx)))){
		wx = 0.5 * (2.0f * z.x - 1.0f) / _SEED_W(idx) + 0.5;
		wy = 0.5 * (2.0f * z.y - 1.0f) / _SEED_W(idx) + 0.5;
    w = (1.0f - 2.0f * fabs(z.x - 0.5f) / _SEED_W(idx));
	}
  if((z.y < 0.5f * (1.0f + _SEED_W(idx)) && z.y > 0.5f * (1.0f - _SEED_W(idx)))){
		wx = 0.5 * (2.0f * z.x - 1.0f) / _SEED_W(idx) + 0.5;
		wy = 0.5 * (2.0f * z.y - 1.0f) / _SEED_W(idx) + 0.5;
    w = fmax((1.0f - 2.0f * fabs(z.x - 0.5f) / _SEED_W(idx)), (1.0f - 2.0f * fabs(z.y - 0.5f) / _SEED_W(idx)));
	}
  w = trans_w(idx, w, par);
	return (float4)(w, 1.0, wx, wy);	
}

// EPIMORPH library file
// seed shape functions for the seed_wca seed function

_EPI_ float trans_w(float w, __constant float* par){
  // EXCLUDE
  if(w < _SEED_W_MIN && w > 0.0f)
    w = 1.0f;
  if(_SEED_W_BASE != 0.0f && w < 0.0f)
    w = _SEED_W_BASE;
  return w;
}

_EPI_ float4 solid(float2 z, __constant float* par){
  // solid
  // DEV

  z = grid_reduce(z);
  float w = 1.0;
  w = trans_w(w, par);
	return (float4)(w, 1.0, z.x, z.y);
}

_EPI_ float4 fade(float2 z, __constant float* par){
  // linear l-r gradient
  // DEV

  z = grid_reduce(z);
  float w = (z.x + 1.0f) / 2.0f;
  w = trans_w(w, par);
	return (float4)(w, 1.0, z.x, z.y);
}


_EPI_ float4 wave(float2 z, __constant float* par){
  // sinousoid
  // DEV

  float _clock = 0.0f;

  z = grid_reduce(z);
  float w = (2.0f + native_sin(2.0f * PI * (z.y + _clock / 10.0f))) / 4.0f;
  w = trans_w(w, par);
	return (float4)(w, 1.0, z.x, z.y);
}


_EPI_ float4 circle(float2 z, __constant float* par){
  // circle
  // FULL, LIVE, DEV

  z = grid_reduce(z);
  float r = native_sqrt(z.x * z.x + z.y * z.y);
  float w = -0.0000001;
	float wx = atan2pi(z.y, z.x) * 3.0;
	float wy = 0.0;
	if(r > _SEED_CIRCLE_R - _SEED_W / 2.0f && r  < _SEED_CIRCLE_R + _SEED_W / 2.0f){
    w = (1.0f - 2.0f * fabs(r - _SEED_CIRCLE_R) / _SEED_W);
		wy = (r - _SEED_CIRCLE_R - _SEED_W / 2.0f) / (_SEED_W);
	}
  w = trans_w(w, par);
	return (float4)(w, 1.0, wx, wy);	
}


_EPI_ float4 lines_lr(float2 z, __constant float* par){
  // parallel vertical lines
  // FULL, LIVE, DEV

  z = grid_reduce(z);
  float w = -0.0000001;
	float wx = 0.0;
	float wy = z.y * 2.0;
  if(z.x > (1.0f - _SEED_W)){
    w = (z.x - (1.0f - _SEED_W)) / _SEED_W;
		wx = w / 2.0;
	}
  else if(z.x < -1.0f * (1.0f - _SEED_W)){
    w = (-1.0f * (1.0f - _SEED_W) - z.x) / _SEED_W;
		wx = w / 2.0 + 0.5;
	}
  w = trans_w(w, par);
	return (float4)(w, 1.0, wx, wy);	
}

_EPI_ float4 lines_inner(float2 z, __constant float* par){
  // lines in a cross
  // FULL, LIVE, DEV

  z = grid_reduce(z);
  float w = -0.0000001;
	float wx = (z.x + _SEED_W) / (2.0 * _SEED_W);
	float wy = (z.y + _SEED_W) / (2.0 * _SEED_W);
  if(fabs(z.x) < _SEED_W)
    w = (1.0f - fabs(z.x) / _SEED_W);
	if(fabs(z.y) < _SEED_W)
    w = fmax(1.0f - fabs(z.x) / _SEED_W, 1.0f - fabs(z.y) / _SEED_W); 
  w = trans_w(w, par);
	return (float4)(w, 1.0, wx, wy);	
}

_EPI_ float4 square(float2 z, __constant float* par){
  // central square
  // FULL, LIVE, DEV

  z = grid_reduce(z);
  float w = -0.0000001;
	float wx = 0.0;
	float wy = 0.0;
  if(z.x < _SEED_W && z.x > -1.0f * _SEED_W && z.y < _SEED_W && z.y > -1.0f * _SEED_W){
    w = fmin((1.0f - fabs(z.x) / _SEED_W), (1.0f - fabs(z.y) / _SEED_W));
		wx = (z.x + _SEED_W) / (2.0 * _SEED_W);
		wy = (z.y + _SEED_W) / (2.0 * _SEED_W);
  }
	
  w = trans_w(w, par);
	return (float4)(w, 1.0, wx, wy);	
}

_EPI_ float4 lines_box(float2 z, __constant float* par){
  // 4 lines in a box
  // FULL, LIVE, DEV

  z = grid_reduce(z);
  float w = -0.0000001;
	float wx = (z.x + _SEED_W) / (2.0 * _SEED_W);
	float wy = (z.y + _SEED_W) / (2.0 * _SEED_W);
  if(z.x > (1.0f - _SEED_W))
    w =  (z.y < 0.0f ? fmax((z.x - (1.0f - _SEED_W)), (-1.0f * (1.0f - _SEED_W) - z.y)) : max((z.x - (1.0f - _SEED_W)), (z.y - (1.0f - _SEED_W)))) / _SEED_W;
  else if(z.y > (1.0f - _SEED_W))
    w =  (z.x > 0.0f ? (z.y - (1.0f - _SEED_W)) : fmax((z.y - (1.0f - _SEED_W)), -1.0f * (1.0f - _SEED_W) - z.x)) / _SEED_W;
  else if(z.x < -1.0f * (1.0f - _SEED_W))
    w =  (z.y > 0.0f ? (-1.0f * (1.0f - _SEED_W) - z.x) : fmax((-1.0f * (1.0f - _SEED_W) - z.y), -1.0f * (1.0f - _SEED_W) - z.x)) / _SEED_W;
  else if(z.y < -1.0f * (1.0f - _SEED_W))
    w =  (z.x < 0.0f ? (-1.0f * (1.0f - _SEED_W) - z.y) : fmax((-1.0f * (1.0f - _SEED_W) - z.y), (z.x - (1.0f - _SEED_W)))) / _SEED_W;
  w = trans_w(w, par);
	return (float4)(w, 1.0, wx, wy);	
}


_EPI_ float4 lines_box_stag(float2 z, __constant float* par){
  // 4 lines in a box, staggered
  // FULL, LIVE, DEV

  z = grid_reduce(z);
  float w = -0.0000001;
	float wx = 0.0;
	float wy = 0.0;
  if(z.x > (1.0f - _SEED_W))
    w = (z.x - (1.0f - _SEED_W)) / _SEED_W;
  if(z.y > (1.0f - _SEED_W))
    w = (z.y - (1.0f - _SEED_W)) / _SEED_W;
  if(z.x < -1.0f * (1.0f - _SEED_W))
    w = (-1.0f * (1.0f - _SEED_W) - z.x) / _SEED_W;
  if(z.y < -1.0f * (1.0f - _SEED_W) && z.x < (1.0f - _SEED_W))
    w = (-1.0f * (1.0f - _SEED_W) - z.y) / _SEED_W;
  w = trans_w(w, par);
	return (float4)(w, 1.0, wx, wy);	
}

_EPI_ float4 anti_grid_fade(float2 z, __constant float* par){
  // inverse grid, radially shaded
  // FULL, LIVE, DEV

  z = grid_reduce(z);
  float w = -0.0000001;
	float wx = 0.0;
	float wy = 0.0;
  z = remf(floor(5.0f * _SEED_GRID_N) / 2.0f * z, 1.0f);
  if((z.x > 0.5f * (1.0f - _SEED_W) && z.x < 0.5f * (1.0f + _SEED_W)) && (z.y < 0.5f * (1.0f + _SEED_W) && z.y > 0.5f * (1.0f - _SEED_W)))
    w = min((1.0f - 2.0f * fabs(z.y - 0.5f) / _SEED_W), (1.0f - 2.0f * fabs(z.x - 0.5f) / _SEED_W));
  w = trans_w(w, par);
	return (float4)(w, 1.0, wx, wy);	
}


_EPI_ float4 grid_fade(float2 z, __constant float* par){
  // grid, radially shaded
  // FULL, LIVE, DEV

  z = grid_reduce(z);
  float w = -0.0000001;
	float wx = 0.0;
	float wy = 0.0;
  z = remf(floor(5.0f * _SEED_GRID_N) /2.0f * z, 1.0f);
  if((z.x > 0.5f * (1.0f - _SEED_W) && z.x < 0.5f * (1.0f + _SEED_W)))
    w = (1.0f - 2.0f * fabs(z.x - 0.5f) / _SEED_W);
  if((z.y < 0.5f * (1.0f + _SEED_W) && z.y > 0.5f * (1.0f - _SEED_W)))
    w = fmax((1.0f - 2.0f * fabs(z.x - 0.5f) / _SEED_W), (1.0f - 2.0f * fabs(z.y - 0.5f) / _SEED_W));
  w = trans_w(w, par);
	return (float4)(w, 1.0, wx, wy);	
}

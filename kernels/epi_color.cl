// EPIMORPH library file
// coloring functions

_EPI_ float4 bgr_id(float4 v, float2 z_z, __constant float* par, float time){
  // identity
  // FULL, LIVE, DEV
  return v;
}

_EPI_ float4 gbr_id(float4 v, float2 z_z, __constant float* par, float time){
  // identity
  // DEV
  return v.yxzw;
}

_EPI_ float4 rotate_hsv(float4 v, float2 z_z, __constant float* par, float time){
  // hsv rotation
  // DEV
  v = RGBtoHSV(v);

  float l = native_sqrt(z_z.x * z_z.x + z_z.y * z_z.y);
  l = 0.4f * native_log(l);
  //l = (4.0f * _COLOR_LEN_SC + 1.0f) * l / (l + 4.0f * _COLOR_LEN_SC);

  float a = 0.0f;
  if(_COLOR_TH_EFF != 0.0f && (z_z.y != 0.0f || z_z.x != 0.0f)){
    a = atan2(z_z.y, z_z.x) * floor(8.0f * _COLOR_TH_EFF) / (2.0f * PI);
  }

  float th = (_COLOR_DHUE + l + a + time * _COLOR_SPEED_TH * 0.1f);
  v.x += th;

  if(_COLOR_18 < 0.99f){
    v.x = fmod(v.x, 1.0f);
    v.x = (v.x > 0.5f) ? 2.0f * _COLOR_18 * (1.0f - v.x) : 2.0f * v.x * _COLOR_18;
    v.x += _COLOR_19;
  }

  return HSVtoRGB(v);
}


_EPI_ float4 rotate_hsls(float4 v, float2 z, float2 z_z, __constant float* par, float time){
  // complex hsls rotation
  // FULL, LIVE, DEV
  v = RGBtoHSLs(v);

	float vz = v.z;

  //float lz = remf(z_z, 1.0f).x + 1.0f;//time;//z_z.x;//-0.2;//sqrt(z_z.x * z_z.x + z_z.y * z_z.y);
  //float l = recover(2.0 * log(5.0 * lz / (lz + 1.0f)));
  //float l = native_log(lz);

  // compute l
  
  float l = native_sqrt(z.x * z.x + z.y * z.y);
  l = native_divide((4.0f * _COLOR_LEN_SC + 1.0f) * l, (l + 4.0f * _COLOR_LEN_SC));
  l = native_log(l + 1.0f);

  // compute a
  float a = 0.0f;
  if(_COLOR_TH_EFF != 0 && (z.y != 0.0f || z.x != 0.0f)){
    a = atan2(z.y, z.x) * floor(8.0f * _COLOR_TH_EFF) / (2.0f * PI);
  }

  // compute rotation axis
  float phi = 2.0f * PI * _COLOR_PHI1 / 2.0f;
  float psi = 2.0f * PI * _COLOR_PSI1 / 2.0f;
  float4 axis = (float4)(native_cos(psi) * native_cos(phi), native_cos(psi) * native_sin(phi), native_sin(psi), 0.0f);

  // compute rotation 1  
  float4 tmp = (float4)(v.x, v.y, v.z, 0.0f);
  float th = 2.0f * PI * (a + l + time * _COLOR_SPEED_TH  * 0.1f);
  th = remf(CX(th, 0.0f), 2.0f * PI).x;
  tmp = rotate3D(tmp, axis, th);
  
  // compute rotation 2  
  th = 2.0f * PI * _COLOR_DHUE;
  phi += 2.0f * PI * _COLOR_PHI2 / 2.0f;
  psi += 2.0f * PI * _COLOR_PSI2 / 2.0f;
  axis = (float4)(native_cos(psi) * native_cos(phi), native_cos(psi) * native_sin(phi), native_sin(psi), 0.0f);
  tmp = rotate3D(tmp, axis, th);

	tmp.z = vz;//_COLOR_Z_RST * vz + (1.0f - _COLOR_Z_RST) * tmp.z;

  float s = native_sqrt(tmp.x * tmp.x + tmp.y * tmp.y + tmp.z * tmp.z);
  s  = s * (1.0f - _COLOR_BASE_I) + _COLOR_BASE_I;
  phi = 2.0f * PI * _COLOR_BASE_PHI;
  psi = 2.0f * PI * _COLOR_BASE_PSI;
  float4 base = _COLOR_BASE_R * (float4)(native_cos(psi) * native_cos(phi), native_cos(psi) * native_sin(phi), native_sin(psi), 0.0f);
  tmp = s * tmp + (1.0f - s) * base;

  tmp = _COLOR_I * tmp + (1.0f - _COLOR_I) * (float4)(v.x, v.y, v.z, 0.0f);

	/*
	s = tmp.x;
	tmp.x = native_sin(PI * tmp.z);
	tmp.z = native_sin(PI * tmp.y);
  tmp.y = native_cos(PI * s);
	*/
	
  // get result
  //float r = native_sqrt(tmp.x * tmp.x + tmp.y * tmp.y + tmp.z * tmp.z);
  //float r_p = 3.0f * r / (2.0f * r + 1.0f);//0.1f + 0.9f * r;
  //tmp *= (r_p / r);
  v = (float4)(tmp.x, tmp.y, tmp.z, v.w);  
  return HSLstoRGB(v);
}

_EPI_ float4 color1d(float2 v, float2 z, float2 z_z, __constant float* par, float time){
  // identity
  // FULL, LIVE, DEV

	int n = 3;
	float a[3];

	a[0] = a[1] = a[2] = 0.0;

  float l = native_sqrt(z.x * z.x + z.y * z.y);
  l = native_divide((4.0f * _COLOR_LEN_SC + 1.0f) * l, (l + 4.0f * _COLOR_LEN_SC));
  l = native_log(l + 1.0f);

	float th = (_COLOR_DHUE + time * _COLOR_SPEED_TH * 0.1f);

	v.x = v.x + l + th;

	//if(v.x > 1.0)
	//v.x -= 1.0;
	v.x = remf1(v.x, 1.0);	
	
	if(0.0f / n <= v.x && v.x < 1.0f / n)
		a[0] = 1.0f - n * (v.x - 0.0f / n);
	else if(2.0f / n <= v.x && v.x < 3.0f / n)
		a[0] = n * (v.x - 2.0 / n);

	if(1.0f / n <= v.x && v.x < 2.0f / n)
		a[1] = 1.0f - n * (v.x - 1.0f / n);
	else if(0.0f / n <= v.x && v.x < 1.0f / n)
		a[1] = n * (v.x - 0.0 / n);

	if(2.0f / n <= v.x && v.x < 3.0f / n)
		a[2] = 1.0f - n * (v.x - 2.0f / n);
	else if(1.0f / n <= v.x && v.x < 2.0f / n)
		a[2] = n * (v.x - 1.0 / n); 


	float4 colors[3] = {(float4)(0.0, 0.1, 1.0, 0.0), (float4)(0.0, 1.0, 0.3, 0.0), (float4)(1.0, 1.0, 1.0, 0.0)};
		
	float4 color = a[0] * colors[0] + a[1] * colors[1] + a[2] * colors[2];

	color *= v.y;
	color.w = v.x + 0.213;
	
	//float4 color = HSVtoRGB((float4)(v.x, 1.0, 1.0, v.x + 0.113)) * v.y;

	//	color *= v.y;
	//	color.w = v.x + 0.113;
	
  return color;
}



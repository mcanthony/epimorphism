// EPIMORPH library file
// coloring functions

__device__ float4 rgb_id(float4 v, float2 z_z){
  // identity
  // FULL, LIVE, DEV
  return v;
}

__device__ float4 rotate_hsv(float4 v, float2 z_z){
  // hsv rotation
  // FULL, LIVE, DEV

  v = RGBtoHSV(v);

  float l = len(z_z);

  l = logf(l);
  l = 0.4f * l;

  //l = (4.0f * _COLOR_LEN_SC + 1.0f) * l / (l + 4.0f * _COLOR_LEN_SC);

  float a = 0.0f;
  if(_COLOR_TH_EFF != 0.0f && (z_z.y != 0.0f || z_z.x != 0.0f)){
    a = atan2f(z_z.y, z_z.x) * floorf(8.0f * _COLOR_TH_EFF) / (2.0f * PI);
  }

  float th =  (_COLOR_DHUE + l + a + _clock * _COLOR_SPEED_TH * _GLOBAL_SPEED / 10.0f);

  v.x += th;

  if(_COLOR_18 < 0.99f){
    v.x = fmodf(v.x, 1.0f);
    v.x = (v.x > 0.5f) ? 2.0f * _COLOR_18 * (1.0f - v.x) : 2.0f * v.x * _COLOR_18;
    v.x += _COLOR_19;
  }

  return HSVtoRGB(v);
}


__device__ float4 rotate_hsls(float4 v, float2 z_z){
  // complex hsls rotation
  // FULL, LIVE, DEV

  v = RGBtoHSLs(v);

  //float l = recover(2.0 * logf(5.0 * len(z_z) / (len(z_z) + 1.0)));

  // compute l
  float l = len(z_z);
  l = (4.0f * _COLOR_LEN_SC + 1.0f) * l / (l + 4.0f * _COLOR_LEN_SC);
  l = logf(l + 1.0f);

  // compute a
  float a = 0.0f;
  if(_COLOR_TH_EFF != 0 && (z_z.y != 0.0f || z_z.x != 0.0f)){
    a = atan2f(z_z.y, z_z.x) * floorf(8.0f * _COLOR_TH_EFF) / (2.0f * PI);
  }

  // compute rotation axis
  float phi = 2.0f * PI * _COLOR_PHI1 / 2.0f;
  float psi = 2.0f * PI * _COLOR_PSI1 / 2.0f;
  float3 axis = vec3(cosf(psi) * cosf(phi), cosf(psi) * sinf(phi), sinf(psi));


  // compute rotation 1
  float th =  2.0f * PI * (a + l + _clock * _COLOR_SPEED_TH * _GLOBAL_SPEED / 10.0f);
  float3 tmp = vec3(v.x, v.y, v.z);
  tmp = rotate3D(tmp, axis, th);


  // compute rotation 2
  th = 2.0f * PI * _COLOR_DHUE;
  phi += 2.0f * PI * _COLOR_PHI2 / 2.0f;
  psi += 2.0f * PI * _COLOR_PSI2 / 2.0f;
  axis = vec3(cosf(psi) * cosf(phi), cosf(psi) * sinf(phi), sinf(psi));
  tmp = rotate3D(tmp, axis, th);


  float s = sqrt(tmp.x * tmp.x + tmp.y * tmp.y + tmp.z * tmp.z);
  s  = s * (1.0f - _COLOR_BASE_I) + _COLOR_BASE_I;
  phi = 2.0f * PI * _COLOR_BASE_PHI;
  psi = 2.0f * PI * _COLOR_BASE_PSI;
  float3 base = _COLOR_BASE_R * vec3(cosf(psi) * cosf(phi), cosf(psi) * sinf(phi), sinf(psi));
  tmp = s * tmp + (1.0f - s) * base;

  tmp = _COLOR_I * tmp + (1.0f - _COLOR_I) * vec3(v.x, v.y, v.z);



  //s = tmp.x;
  //tmp.x = sinf(PI * tmp.z);
  //tmp.z = sinf(PI * tmp.y);
  //tmp.y = cosf(PI * s);

  // get result

  v = vec4(0.99999f * tmp.x, 0.99999f * tmp.y, 0.99999f * tmp.z, v.w);
  return HSLstoRGB(v);
}

float2 CX(float r, float i){
  return (float2)(r, i);
}

float2 CXP(float r, float i){
  return (float2)(hypot(r,i), atan2(i, r));
}

float2 M(float2 z0, float2 z1){
  return CX(z0.x * z1.x - z0.y * z1.y, z0.x * z1.y + z0.y * z1.x);
}

float2 D(float2 z0, float2 z1){
  float r = dot(z1, z1);
  return CX(native_divide((z0.x * z1.x + z0.y * z1.y), r), native_divide((z0.y * z1.x - z0.x * z1.y), r));
}

float recover(float x){
  if(isnan(x) || isinf(x))
    x = 0.0f;
  return x;
}

float2 recover2(float2 z){
  if(isnan(z.x) || isinf(z.x))
    z.x = 0.0f;
  if(isnan(z.y) || isinf(z.y))
    z.y = 0.0f;
  return z;
}

float4 recover4(float4 z){
  if(isnan(z.x) || isinf(z.x))
    z.x = 0.0f;
  if(isnan(z.y) || isinf(z.y))
    z.y = 0.0f;
  if(isnan(z.z) || isinf(z.z))
    z.z = 0.0f;
  if(isnan(z.w) || isinf(z.w))
    z.w = 0.0f;
  return z;
}

float2 remf(float2 z, float m){
  return z - m * floor(CX(native_divide(z.x, m), native_divide(z.y, m)));
}

float n_pow(float x, float y){
  return exp2(y * native_log2(x));
}

float4 _gamma3(float4 v, float gamma){
  return (float4)(n_pow(v.x, gamma), n_pow(v.y, gamma), n_pow(v.z, gamma), v.w);
}

/*
float4 to_rpp(float4 v){
  float r = native_sqrt(v.x * v.x + v.y * v.y + v.z * v.z);
  float4 polar = (float4)(r, atan2(v.x, v.y), acos(v.z / r), v.w);
  //  if(polar.z < 0.0f)
  //    polar.z += 2.0f * PI;
  return polar;
}

float4 to_xyz(float4 v){
  return (float4)(v.x * native_cos(v.y) * native_sin(v.z), v.x * native_sin(v.y) * native_sin(v.z), v.x * native_cos(v.z), v.w);
}
*/

#define intrp(from, to, time) (time >= 1.0f ? to : mix(from, to, (1.0 + erf(4.0f * time - 2.0f)) / 2.0))


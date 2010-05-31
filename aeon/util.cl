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

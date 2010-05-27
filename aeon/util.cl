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
  return CX((z0.x * z1.x + z0.y * z1.y) / r, (z0.y * z1.x - z0.x * z1.y) / r);
}

float4 color(float r, float g, float b, float a){
  return (float4)(r, g, b, a);
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

float2 remf(float2 z, float m){
  return m * (z / m - floor(z / m));
}


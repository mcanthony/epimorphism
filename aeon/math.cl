float2 sq(float2 z0){
  return M(z0, z0);
}

float2 sinz(float2 z0){
  float s, c;
  s = sincos(z0.x, &c);
  return CX(s * cosh(z0.y), c * sinh(z0.y));
}

float2 cosz(float2 z0){
  float s, c;
  s = sincos(z0.x, &c);
  return CX(c * cosh(z0.y), -1.0f * s * sinh(z0.y));
}

float2 tanz(float2 z0){
  float s, c;
  s = sincos(2.0 * z0.x, &c);
  float r = c + cosh(2.0f * z0.y);
  return CX(s, sinh(2.0f * z0.y)) / r;
}

float2 sinhz(float2 z0){
  float s, c;
  s = sincos(z0.y, &c);
  return CX(sinh(z0.x) * c, cosh(z0.x) * s);
}

float2 coshz(float2 z0){
  float s, c;
  s = sincos(z0.y, &c);
  return CX(cosh(z0.x) * c, sinh(z0.x) * s);
}

float2 tanhz(float2 z0){
  float s, c;
  s = sincos(2.0 * z0.y, &c);
  float r = cosh(2.0f * z0.x) + c;
  return CX(sinh(2.0f * z0.x), s) / r;
}

float2 expz(float2 z0){
  float f = exp(z0.x);
  float s, c;
  s = sincos(z0.y, &c);
  return CX(f * c, f * s);
}

float2 sqrtz(float2 z0){
  return CX(rint(z0.x), rint(z0.y));
}

float2 G(float2 z0){
  return CX((z0.x > 0 ? floor(z0.x) : -1.0f * floor(-1.0f * z0.x)), (z0.y > 0 ? floor(z0.y) : -1.0f * floor(-1.0f * z0.y)));
  // return CX(floor(z0.x), floor(z0.y));
}

float2 F(float2 z0){
  return z0 - G(z0);
}

float2 P(float2 z0, float2 v1){
  return CX(z0.x * v1.x, z0.y * v1.y);
}

//float2 n(float2 z0){
//  return noise2(z0.x + z0.y);
//}

float2 H(float2 z0){
  float2 v1 = CX(0,0);//par[32], par[33]);
  return CX(1.0f - v1.x * z0.x * z0.x + z0.y, v1.y * z0.x);
}

float2 B(float2 z0){
  float K = 0.0;//par[32];
  float pi = PI;
  float mid = z0.x + K * sin( pi * (z0.y + 1) ) / pi - 1;
  return CX(mid, z0.y + mid);
}

float4 rotate3D(float4 v, float4 axis, float th){
  // compute constants
  float c = cos(th);
  float s = sin(th);

  // compute rotation
  float4 res = (float4)(0.0f, 0.0f, 0.0f, 0.0f);
  res.x = (1.0f + (1.0f - c) * (axis.x * axis.x - 1.0f)) * v.x +
          (axis.z * s + (1.0f - c) * axis.x * axis.y) * v.y +
          (-1.0f * axis.y * s + (1.0f - c) * axis.x * axis.z) * v.z;

  res.y = (-1.0f * axis.z * s + (1.0f - c) * axis.x * axis.y) * v.x +
          (1.0f + (1.0f - c) * (axis.y * axis.y - 1.0f)) * v.y +
          (axis.x * s + (1.0f - c) * axis.y * axis.z) * v.z;

  res.z = (axis.y * s + (1.0f - c) * axis.x * axis.z) * v.x +
          (-1.0f * axis.x * s + (1.0f - c) * axis.y * axis.z) * v.y +
          (1.0f + (1.0f - c) * (axis.z * axis.z - 1.0f)) * v.z;

  return res;
}

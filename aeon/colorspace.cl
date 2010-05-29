float4 RGBtoHSV(float4 val){
  float vmin = fmin(fmin(val.x, val.y), val.z);
  float vmax = fmax(fmax(val.x, val.y), val.z);
  float h, s;

  float delta = vmax - vmin;

  if(vmax < 0.001f || delta < 0.001f){
    return (float4)(0.0f, 0.0f, vmax, val.w);
  }else {
    s = native_divide(delta, vmax);
    if(fabs(val.x - vmax) < 0.0001f)
      h = native_divide(( val.y - val.z ), delta);
    else if(fabs(val.y - vmax) < 0.0001f)
      h = 2.0f + native_divide((val.z - val.x), delta);
    else
      h = 4.0f + native_divide((val.x - val.y), delta);
    h /= 6.0f;
    return (float4)(h, s, vmax, val.w);
  }
}

float4 HSVtoRGB(float4 val){
  if(val.y == 0.0f && val.x == 0.0f){//val.y < 0.0001f || val.z < 0.0001f){
    return (float4)(val.z, val.z, val.z, val.w);
  }else{
    float4 res = (float4)(0.0f, 0.0f, 0.0f, val.w);
    val.x = 6.0f * (val.x - floor(val.x));
    float f = val.x - floor(val.x);
    int h = floor(val.x);
    float4 vals = (float4)(1.0f, 1.0f - val.y, 1.0f - val.y * f, 1.0f - val.y * (1.0f - f));
    if(h == 0)
      res = (float4)(vals.x, vals.w, vals.y, 0.0f);
    else if(h == 1)
      res = (float4)(vals.z, vals.x, vals.y, 0.0f);
    else if(h == 2)
      res = (float4)(vals.y, vals.x, vals.w, 0.0f);
    else if(h == 3)
      res = (float4)(vals.y, vals.z, vals.x, 0.0f);
    else if(h == 4)
      res = (float4)(vals.w, vals.y, vals.x, 0.0f);
    else
      res = (float4)(vals.x, vals.y, vals.z, 0.0f);
    res = val.z * res;
    res.w = val.w;
    return res;
  }
}

float4 HSLstoRGB(float4 val){

  float s = native_sqrt(val.x * val.x + val.y * val.y);
  float h;

  if(s == 0.0f){
    h = 0.0f;
  }else{
    h = atan2(val.y, val.x);
  }

  if(h <= 0.0f)
    h += 2.0f * 3.14159f;
  h /= (2.0f * 3.14159f);

  float l = val.z;

  if(s == 0.0f)
    return (float4)((l + 1.0f) / 2.0f, (l + 1.0f) / 2.0f, (l + 1.0f) /  2.0f, val.w);

  float delta = native_divide(s, sqrt(1.0f - l * l));

  if(l > 0)
    delta *= (2.0f - l - 1.0f);
  else
    delta *= (l + 1.0f);

  float v = (l + 1.0f + delta) / 2.0f;
  float min = v - delta;
  s = 1.0f - native_divide(min, v);

  return HSVtoRGB((float4)(h, s, v, val.w));
}

float4 RGBtoHSLs(float4 val){
  float h, s, l;
  float vmin = fmin(fmin(val.x, val.y), val.z);
  float vmax = fmax(fmax(val.x, val.y), val.z);

  float delta = vmax - vmin;

  l = (vmax + vmin) - 1.0f;

  s = delta * native_sqrt(1.0f - l * l);

  if(l == -1.0f || l == 1.0f)
    s = 0.0f;
  else if(l > 0)
    s = native_divide(s, (2.0f - l - 1.0f));
  else if(l <= 0)
    s = native_divide(s, (l + 1.0f));

  if(s == 0.0f){
    h = 0.0f;
  }else {
    if(val.x == vmax)
      h = native_divide((val.y - val.z), delta);            // between yellow & magenta
    else if(val.y == vmax)
      h = 2.0f + native_divide((val.z - val.x), delta);     // between cyan & yellow
    else
      h = 4.0f + native_divide((val.x - val.y), delta);
    h *= PI / 3.0f;
  }

  float4 r = (float4)(s * native_cos(h), s * native_sin(h), 0.999999f * l, val.w);
  
  return r;

}

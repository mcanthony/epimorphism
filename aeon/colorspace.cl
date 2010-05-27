float4 RGBtoHSV(float4 val){
  float vmin = fmin(fmin(val.x, val.y), val.z);
  float vmax = fmax(fmax(val.x, val.y), val.z);
  float h, s;

  float delta = vmax - vmin;

  if(vmax < 0.001f || delta < 0.001f){
    return color(0.0f, 0.0f, vmax, val.w);
  }else {
    s = delta / vmax;
    if(fabs(val.x - vmax) < 0.0001f)
      h = ( val.y - val.z ) / delta;
    else if(fabs(val.y - vmax) < 0.0001f)
      h = 2.0f + ( val.z - val.x ) / delta;
    else
      h = 4.0f + ( val.x - val.y ) / delta;
    h /= 6.0f;
    return color(h, s, vmax, val.w);
  }
}

float4 HSVtoRGB(float4 val){
  if(val.y == 0.0f && val.x == 0.0f){//val.y < 0.0001f || val.z < 0.0001f){
    return color(val.z, val.z, val.z, val.w);
  }else{
    float4 res = color(0.0f, 0.0f, 0.0f, val.w);
    val.x = 6.0f * (val.x - floor(val.x));
    float f = val.x - floor(val.x);
    int h = floor(val.x);
    float4 vals = color(1.0f, 1.0f - val.y, 1.0f - val.y * f, 1.0f - val.y * (1.0f - f));
    if(h == 0)
      res = color(vals.x, vals.w, vals.y, 0.0f);
    else if(h == 1)
      res = color(vals.z, vals.x, vals.y, 0.0f);
    else if(h == 2)
      res = color(vals.y, vals.x, vals.w, 0.0f);
    else if(h == 3)
      res = color(vals.y, vals.z, vals.x, 0.0f);
    else if(h == 4)
      res = color(vals.w, vals.y, vals.x, 0.0f);
    else
      res = color(vals.x, vals.y, vals.z, 0.0f);
    res = val.z * res;
    res.w = val.w;
    return res;
  }
}

float4 HSLstoRGB(float4 val){

  float s = hypot(val.x, val.y);
  float h;

  if(s < 0.0001f){
    h = 0.0f;
  }else{
    h = atan2(val.y, val.x);
  }

  if(h <= 0.0f)
    h += 2.0f * 3.14159f;
  h /= (2.0f * 3.14159f);

  float l = val.z;

  if(s < 0.0001f)
    return color((l + 1.0f) / 2.0f, (l + 1.0f) / 2.0f, (l + 1.0f) / 2.0f, val.w);

  float delta = s / sqrt(1.0f - l * l);

  if(l > 0)
    delta *= (2.0f - l - 1.0f);
  else
    delta *= (l + 1.0f);

  float v = (l + 1.0f + delta) / 2.0f;
  float min = v - delta;
  s = 1.0f - min / v;

  return HSVtoRGB(color(h, s, v, val.w));
}

float4 RGBtoHSLs(float4 val){
  float h, s, l;
  float vmin = fmin(fmin(val.x, val.y), val.z);
  float vmax = fmax(fmax(val.x, val.y), val.z);

  float delta = vmax - vmin;

  l = (vmax + vmin) - 1.0f;

  s = delta * sqrt(1.0f - l * l);

  if(l < -0.9999f || l > 0.9999f)
    s = 0.0f;
  else if(l > 0)
    s /= (2.0f - l - 1.0f);
  else if(l <= 0)
    s /= (l + 1.0f);

  if(s < 0.0001f){
    h = 0.0f;
  }else {
    if(fabs(val.x - vmax) < 0.0001f)
      h = ( val.y - val.z ) / delta;            // between yellow & magenta
    else if(fabs(val.y - vmax) < 0.0001f)
      h = 2.0f + ( val.z - val.x ) / delta;     // between cyan & yellow
    else
      h = 4.0f + ( val.x - val.y ) / delta;
    h *= PI / 3.0f;
  }
  return color(s * cos(h), s * sin(h), l, val.w);

}

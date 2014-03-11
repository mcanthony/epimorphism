float4 RGBtoHSV(float4 val){
	val = clamp(val, 0.0f, 1.0f);
	
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

		if(h < 0.0)
			h += 1.0f;
		
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

float4 HSLtoRGB(float4 val){

  float h = val.x;
	float s = val.y;
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

	val.x = h;
	val.y = s;

	return HSLtoRGB(val);
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

/*
float4 RGBtoXYZ(float4 val){
  float a = val.w;

  
  if(val.x > 0.04045f)
    val.x = pow((val.x + 0.055f) / 1.055f, 2.4f);
  else 
    val.x /= 12.92f;
  if(val.y > 0.04045f)
    val.y = pow((val.y + 0.055f) / 1.055f, 2.4f);
  else
    val.y / 12.92f;
  if(val.z > 0.04045f)
    val.z = pow((val.z + 0.055f) / 1.055f, 2.4f);
  else
    val.z / 12.92f;

  //Observer. = 2°, Illuminant = D65
  float4 xyz;

  xyz.x = val.x * 0.412456f  + val.y * 0.357576f + val.z * 0.180438f;
  xyz.y = val.x * 0.212673f  + val.y * 0.715152f + val.z * 0.072175f;
  xyz.z = val.x * 0.0193339f + val.y * 0.119192f + val.z * 0.950304f;
  xyz.w = a;

  return xyz;
}
*/
/*
float4 XYZtoLAB(float4 val){
  const REF_X:Number = 95.047; // Observer= 2°, Illuminant= D65
  const REF_Y:Number = 100.000; 
  const REF_Z:Number = 108.883; 
  var x:Number = X / REF_X;   
  var y:Number = Y / REF_Y;  
  var z:Number = Z / REF_Z;  
 
  if ( val.x > 0.008856 ) { val.x = pow( x , 1/3 ); }
  else { val.x = ( 7.787 * val.x ) + ( 16/116 ); }
  if ( val.y > 0.008856 ) { val.y = pow( val.y , 1/3 ); }
  else { val.y = ( 7.787 * val.y ) + ( 16/116 ); }
  if ( val.z > 0.008856 ) { val.z = pow( val.z , 1/3 ); }
  else { val.z = ( 7.787 * val.z ) + ( 16/116 ); }
 
  var lab:Object = {l:0, a:0, b:0};
  lab.l = ( 116 * val.y ) - 16;
  lab.a = 500 * ( val.x - val.y );
  lab.b = 200 * ( val.y - val.z );
 
  return lab;
}


  float4 LABtoXYZ(float4 val){
  const REF_X:Number = 95.047; // Observer= 2°, Illuminant= D65
  const REF_Y:Number = 100.000; 
  const REF_Z:Number = 108.883; 
  var y:Number = (l + 16) / 116;
  var x:Number = a / 500 + y;
  var z:Number = val.y - val.z / 200;
 
  if ( pow( val.y , 3 ) > 0.008856 ) { val.y = pow( val.y , 3 ); }
  else { val.y = ( val.y - 16 / 116 ) / 7.787; }
  if ( pow( val.x , 3 ) > 0.008856 ) { val.x = pow( val.x , 3 ); }
  else { val.x = ( val.x - 16 / 116 ) / 7.787; }
  if ( pow( val.z , 3 ) > 0.008856 ) { val.z = pow( val.z , 3 ); }
  else { val.z = ( val.z - 16 / 116 ) / 7.787; }
 
  var xyz:Object = {x:0, y:0, z:0};
  xyz.x = REF_X * x;     
  xyz.y = REF_Y * y; 
  xyz.z = REF_Z * z; 
 
  return xyz;
  }
*/

/*
float4 XYZtoRGB(float4 val){
  //X from 0 to  95.047      (Observer = 2°, Illuminant = D65)
  //Y from 0 to 100.000
  //Z from 0 to 108.883

  float a = val.w;
  float4 rgb;
 
  rgb.x = val.x *   3.24045f + val.y *  -1.53714f + val.z * -0.498532f;
  rgb.y = val.x * -0.969266f + val.y *   1.87601f + val.z * 0.0415561f;
  rgb.z = val.x * 0.0556434f + val.y * -0.204026f + val.z *   1.05723f;
  rgb.w = a;
 
  if(rgb.x > 0.0031308f)
    rgb.x = 1.055f * pow(rgb.x, .41667) - 0.055f;
  else
    rgb.x *= 12.92f;
  if(rgb.y > 0.0031308f)
    rgb.y = 1.055f * pow(rgb.y, .41667) - 0.055f; 
  else
    rgb.y *= 12.92f;
  if(rgb.z > 0.0031308f)
    rgb.z = 1.055f * pow(rgb.z, .41667) - 0.055f;
  else
    rgb.z *= 12.92f;

  return rgb;
}
*/
/*
  float4 RGBtoLAB(float4 val){
  var xyz:Object = ColorUtils.rgb2xyz(R, G, B);
  return ColorUtils.xyz2lab(xyz.x, xyz.y, xyz.z);
  }

  float4 LABtoRGB(float4 val){
  var xyz:Object = ColorUtils.rgb2xyz(R, G, B);
  return ColorUtils.xyz2lab(xyz.x, xyz.y, xyz.z);
  }

*/

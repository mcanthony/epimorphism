float4 cull(float4 v, float4 seed, float4 frame, __constant float* par){
  float new_w;

  
  if(frame.w >= 0.0f)
    new_w = (1.0 - seed.w) * (frame.w + 1.0f);
  else
    if(seed.w < 0.0001f)
      new_w = frame.w;
    else
      new_w = 0.0f;
  frame.w = new_w;
  
  v += seed.w * seed + (1.0 - seed.w) * frame;      
  //if(v.w < 0)
  //  v.w = frame.w;

  int null = (frame.w < 0.0f || v.w < 0.0f);
  if(null)
    v.w = -10000000.0f;
  
  if(_CULL_DEPTH(0) != 0.0f && v.w > 20 * _CULL_DEPTH(0))
    v = (float4)(0.0f, 0.0f, 0.0f, -10000000.0f);
  
  return v;
}

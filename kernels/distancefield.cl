// distancefield

const sampler_t sampler = CLK_NORMALIZED_COORDS_TRUE | CLK_FILTER_LINEAR | CLK_ADDRESS_CLAMP_TO_EDGE;
const sampler_t image_sampler = CLK_NORMALIZED_COORDS_FALSE | CLK_FILTER_NEAREST | CLK_ADDRESS_CLAMP_TO_EDGE;

float df(float3 p, float time) {
  return length(p) - 1.0f;
}


float inter(float3 ro, float3 rd, float time) {
  float t = 0.0f;
  for (float count=0.0f; count<200.0f; count += 1) {
    float3 pos = ro + t * rd;
    float dist = df(pos, time);
    if (dist < 0.0001f){
      return t;
    }

    t += dist;
    if (t > 6.0f) return -1.0f;
  }
  return -1.0f;
}

float3 calcNormal(float3 p, float time) {
  float3 e = (float3)(0.001f, 0.0f, 0.0f);
  float3 n;
  n.x = df(p+e.xyy, time) - df(p-e.xyy, time);
  n.y = df(p+e.yxy, time) - df(p-e.yxy, time);
  n.z = df(p+e.yyx, time) - df(p-e.yyx, time);

  return normalize(n);
}

__kernel __attribute__((reqd_work_group_size(16,16,1)))
void distancefield(__global uchar4* pbo, write_only image2d_t out, read_only image3d_t aux,
	  __constant float *par, __constant float *internal, __constant float2 *zn, float time){
  time /= 4.0f;
  // get p in [0..$KERNEL_DIM]x[0..$KERNEL_DIM]
  const int x = get_global_id(0);
  const int y = get_global_id(1);
  int2 p = (int2)(x, y);

  // get z in [-1..1]x[-1..1]
  float2 z = (float2)(2.0f / $KERNEL_DIM$) * convert_float2(p) + (float2)(1.0f / $KERNEL_DIM$ - 1.0f, 1.0f / $KERNEL_DIM$ - 1.0f);

  float3 ro = (float3)(0.0f, 0.0f, 2.0f);//0.0f, 2.0*sin(time), 2.0f * cos(time));
  float3 rd = normalize((float3)(z.x, z.y, -1.0f));

  float hit = inter(ro, rd, time);

  // generate color(z)
  float4 color;
  if (hit >= 0.0f) {
    float3 col = (float3)(0.0f, 0.0f, 0.0f);

    float3 pos = ro + hit * rd;
    float3 nor = calcNormal(pos, time);
    float3 lig = normalize((float3)(1.0f, 0.8f, 0.6f));

    float amb = 0.5f + 0.5f * nor.y;
    float dif = dot(nor, lig);

    col = amb * (float3)(0.2f, 0.2f, 0.2f);
    col += dif * (float3)(0.8f,0.8f,0.8f);
    color = (float4)(col.x, col.y * (1.0f + z.x) / 2.0, col.z * (1.0f + z.y) / 2.0, 1.0f);
  }else{
    color = HSVtoRGB((float4)(2 * PI * z.x, 1.0f, (z.y + 1.0) / 2.0, 0.0f));
  }

  // write out color
  write_imagef(out, p, color);
  #ifndef $POST_PROCESS$
  pbo[y * $KERNEL_DIM$ + x] = convert_uchar4(255.0f * color.zyxw);
  #endif
}


// optional post processing.  must be enable in app configuration
__kernel __attribute__((reqd_work_group_size(16,16,1)))
void post_process(__global uchar4* pbo, read_only image2d_t out, float time, __constant float* par){

  // get coords
  const int x = get_global_id(0);
  const int y = get_global_id(1);
  int2 p = (int2)(x, y);

  float4 v = read_imagef(out, image_sampler, p);

  float4 color = v;
  pbo[y * $KERNEL_DIM$ + x] = convert_uchar4(255.0f * color.xyzw);
}

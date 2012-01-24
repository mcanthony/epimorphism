// lissajous

const sampler_t sampler = CLK_NORMALIZED_COORDS_TRUE | CLK_FILTER_LINEAR | CLK_ADDRESS_CLAMP_TO_EDGE;
const sampler_t image_sampler = CLK_NORMALIZED_COORDS_FALSE | CLK_FILTER_NEAREST | CLK_ADDRESS_CLAMP_TO_EDGE;

#define TWO_PI 6.28318530717958647693


__kernel __attribute__((reqd_work_group_size(16,16,1))) 
void lissajousglitch(__global uchar4* pbo, write_only image2d_t out, read_only image2d_t aux, 
	  __constant float *par, __constant float *internal, __constant float2 *zn, float time){
  // get p in [0..$KERNEL_DIM]x[0..$KERNEL_DIM]
  const int x = get_global_id(0);
  const int y = get_global_id(1);
  int2 p = (int2)(x, y);

  // get z in [-1..1]x[-1..1]
  float2 z = (float2)(2.0f / $KERNEL_DIM$) * convert_float2(p) + (float2)(1.0f / $KERNEL_DIM$ - 1.0f, 1.0f / $KERNEL_DIM$ - 1.0f);  

  // cant have a variable length list
  int nrParticles = 50;
  float dist[50];

  float glitch_f = 50;  // the larger this is, the more inaccurate the distance calculation will be.
  float scale = 1.0;    // increase to 'zoom' out, decrease for in

  // compute distances
  for(int i = 0; i< nrParticles; i++){
    // pt recomputed for each z.  inefficient.  should be done on the cpu & uploaded once per frame
    float2 pt = (float2)(glitch_f * 0.16 * sin(time/500.0*TWO_PI*(i + 1)),
			 glitch_f * -0.09 * sin(time/500.0*TWO_PI*(2.0 * i + 1)));
    
    float d = distance(pt, glitch_f * scale * z);

    // sorted insert
    int j;
    for (j = i - 1; j >= 0; j--) {
      if (dist[j] <= d)
	break;
      dist[j + 1] = dist[j];
    }
    dist[j + 1] = d;
  }

  float c = (dist[25]/dist[24]>dist[20]/dist[19]);

  // generate color(z)
  // float4 color = (float4)(dist[0] - floor(dist[0]),c,dist[18] - floor(dist[18]),1.0);
  // float4 color = (float4)(dist[0] - floor(dist[0]),dist[25] - floor(dist[25]),dist[18] - floor(dist[18]),1.0);
  float4 color = (float4)(c,c,c,1.0);

  // write out color
  #ifdef $POST_PROCESS$
  write_imagef(out, p, color);   
  #else
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
  pbo[y * $KERNEL_DIM$ + x] = convert_uchar4(255.0 * color.xyzw);
}

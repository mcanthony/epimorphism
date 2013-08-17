// EPIMORPH library file
// complex plane reductions C -> [-1, -1] x [1, 1]
// SUFFIX (z)

_EPI_ float2 no_reduce(float2 z){
  // standard reduction based on the cartesian grid
  // FULL, LIVE, DEV

  return z;
}


_EPI_ float2 grid_reduce(float2 z){
  // standard reduction based on the cartesian grid
  // FULL, LIVE, DEV

  return remf(z + CX(1.0f, 1.0f), 2.0f) - CX(1.0f, 1.0f);
}


_EPI_ float2 torus_reduce(float2 z){
  // reduction based on the reflective torus
  // FULL, LIVE, DEV

  z = z + CX(1.0f, 1.0f);

  z = remf(z, 4.0f);
  if(z.x >= 2.0f)
    z.x = 4.0f - z.x;
  if(z.y >= 2.0f)
    z.y = 4.0f - z.y;

  return z - CX(1.0f, 1.0f);
}


/*
_EPI_ float2 tri_reduce(float2 z){
  // reduction based on the reflective torus
  // FULL, LIVE, DEV

  z = (z + (float2)(1.0f, sqrt(3.0f) / 2.0f)) / 2.0f;

  
  float2 zi = floor((float2)(z.x - z.y * sqrt(3.0f) / 3.0f, z.y * 2.0f * sqrt(3.0f) / 3.0f));
  float2 zr = z - (float2)(zi.x + zi.y / 2.0f, zi.y * sqrt(3.0f) / 2.0f);
  //int a  = (int)remf(((int) (zi.x)), 3.0);
  zi.x -= zi.y;
  int a = (int)(zi.x - 3.0 * floor(zi.x / 3.0f));
  int c = (zr.y > sqrt(3.0f) - zr.x * sqrt(3.0f));
  
  if(c){
    zr.x -= 1.0f;

    zr = -1.0f / 2.0f * (float2)(zr.x + zr.y * sqrt(3.0f), zr.x * sqrt(3.0f) - zr.y);

    zr.x += 1.0f;    
  }
  
  zr = 2.0f * zr - (float2)(1.0f, sqrt(3.0f) / 2.0f);

  zr.y += sqrt(3.0f) / 6.0f;

  if(a == 1){
    zr = 1.0f / 2.0f * (float2)(-1.0f * zr.x - zr.y * sqrt(3.0f), zr.x * sqrt(3.0f) - zr.y);
  }

  if(a == 2){
      zr = 1.0f / 2.0f * (float2)(-1.0f * zr.x + zr.y * sqrt(3.0f), -1.0f * zr.x * sqrt(3.0f) - zr.y);
  }

  zr.y -= sqrt(3.0f) / 6.0f;

  return zr;

}
*/

/*
device__ float2 hex_reduce(float2 z){
  // hex reduce
  // 5 == 5

  z = z * 2.0;

  z.y += 0.5f;
  int n_y = floorf(z.y);
  z.y -= n_y;
  if(abs(n_y) % 2 == 1)
    z.y = 1.0f - z.y;


  z.x *= sqrt(3.0f) / 2.0f;
  z.x += 0.5f;
  int n_x = floorf(z.x);
  z.x -= n_x;

  //if(abs(n_x) % 2 == 1)
  //  z.x = 1.0f - z.x;

  z.x = 2.0f * (z.x) / sqrtf(3.0f);


  if(z.y < z.x * sqrt(3.0f)){
    z.x -= 2.0 / sqrt(3.0f);
  }else if(z.y > -1.0 * z.x * sqrt(3.0f)){
    float tmp = z.x;
    z.x = -0.5 * (z.x + sqrt(3.0f) * z.y);
    z.y = -0.5 * (sqrt(3.0f) * tmp - 1.0 * z.y);
  }


  z.x += 1.0 / sqrt(3.0f);

  z.y -= 0.5;

  return z / 2.0;
}
*/

/*
_EPI_ float2 awesome_reduce(float2 z){
  // hex reduce
  // NA

  z = z * 2.0;

  z.y += 0.5f;
  int n_y = floor(z.y);
  z.y -= n_y;
  if(abs(n_y) % 2 == 1)
    z.y = 1.0f - z.y;

  z.y -= 0.5;

  return z / 2.0;
}
*/

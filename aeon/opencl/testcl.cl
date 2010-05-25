__kernel void test(__global float *c){
  int gid = get_global_size(0);
  c[gid] = gid;
}

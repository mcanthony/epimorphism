__kernel void test( __global float* C){
    // Thread index
    int tx = get_local_id(0);
    int ty = get_local_id(1);

    C[get_global_id(1) * get_global_size(0) + get_global_id(0)] = (float)tx / get_global_size(0);

}

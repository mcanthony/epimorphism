uint rgbToInt(float r, float g, float b)
{
  r = clamp(r, 0.0f, 255.0f);
  g = clamp(g, 0.0f, 255.0f);
  b = clamp(b, 0.0f, 255.0f);
  return (convert_uint(b)<<16) + (convert_uint(g)<<8) + convert_uint(r);
}

__kernel void test(__global uint* g_odata, int kernel_dim, int frame_num)
{
    const int tx = get_local_id(0);
    const int ty = get_local_id(1);
    const int bw = get_local_size(0);
    const int bh = get_local_size(1);
    const int x = get_global_id(0);
    const int y = get_global_id(1);

    g_odata[y * kernel_dim + x] = rgbToInt((int)(255.0 * ((frame_num + x) % kernel_dim) / kernel_dim), (int)(255.0 * ((frame_num + y) % kernel_dim) / kernel_dim), 0);
}

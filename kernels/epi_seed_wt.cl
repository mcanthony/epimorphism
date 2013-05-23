// EPIMORPH library file
// seed width transformation functions fot the seed_wca seed


_EPI_ float wt_id(int idx, float w){
  // identity transform
  // FULL, LIVE, DEV

  return w;
}


_EPI_ float wt_inv(int idx, float w){
  // identity transform
  // LIVE, DEV

  return 1.0f - w;
}


_EPI_ float wt_circular(int idx, float w){
  // circular transform
  // FULL, LIVE, DEV

  return native_sqrt(1.0f - (1.0f - w) * (1.0f - w));
}


_EPI_ float wt_inv_circular(int idx, float w){
  // circular transform
  // LIVE, DEV

  return 1.0f - native_sqrt(1.0f - (1.0f - w) * (1.0f - w));
}

_EPI_ float wt_gauss(int idx, float w){
  // gaussian transform
  // FULL, LIVE, DEV

  return native_exp(-10.0f * (w - 1.0f) * (w - 1.0f));
}

_EPI_ float wt_inv_gauss(int idx, float w){
  // inverse gaussian transform
  // FULL, LIVE, DEV

  return native_exp(-100.0f * w * w);
}

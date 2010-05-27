// EPIMORPH library file
// seed width transformation functions fot the seed_wca seed


_EPI_ float wt_id(float w){
  // identity transform
  // FULL, LIVE, DEV

  return w;
}


_EPI_ float wt_inv(float w){
  // identity transform
  // FULL, LIVE, DEV

  return 1.0f - w;
}


_EPI_ float wt_circular(float w){
  // circular transform
  // FULL, LIVE, DEV

  return native_sqrt(1.0f - (1.0f - w) * (1.0f - w));
}


_EPI_ float wt_inv_circular(float w){
  // circular transform
  // FULL, LIVE, DEV

  return 1.0f - native_sqrt(1.0f - (1.0f - w) * (1.0f - w));
}

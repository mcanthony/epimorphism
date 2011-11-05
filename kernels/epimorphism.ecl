const sampler_t sampler = CLK_NORMALIZED_COORDS_TRUE | CLK_FILTER_LINEAR | CLK_ADDRESS_CLAMP_TO_EDGE;
const sampler_t image_sampler = CLK_NORMALIZED_COORDS_FALSE | CLK_FILTER_NEAREST | CLK_ADDRESS_CLAMP_TO_EDGE;

#define _EPI_
#define KERNEL_DIM %KERNEL_DIM%
#define FRACT %FRACT%
%PAR_NAMES%
%CULL_ENABLED%
%POST_PROCESS%

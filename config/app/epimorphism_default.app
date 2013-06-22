{
 'app': 'epimorphism',
 'name': 'default',
 'state': State('epimorphism', 'default'),

 'keyboard_handler': 'DefaultEpimorphismKeyboard',
 'mouse_handler': 'DefaultEpimorphismMouse',

 'OSC_enabled': False,
 'OSC_handler': 'EpimorphismRD1OSC',
 'OSC_client_address': ('10.0.0.116', 9001),
 'OSC_echo': True,

 'state_intrp_time': 15.0,

 'screen': [800,800,False],
 'kernel_dim': 1536,
 'fract': 2,

 'sources': ['util', 'math', 'colorspace', 'epi_cull', 'epi_reduce', 'epi_reset', 'epi_color', 'epi_seed_c', 'epi_seed_a', 'epi_seed_wt', 'epi_seed_w', 'epi_seed', 'post1', 'epi_kernels'], 
 'kernel': 'epimorphism',
 'lib_prefix': 'epi',
 'feedback_buffer': True
}


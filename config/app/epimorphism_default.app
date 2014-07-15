{
 'app': 'epimorphism',
 'name': 'default',
 'state': State('epimorphism', 'default'),
 'component_level': 'FULL',

 'keyboard_handler': 'DefaultEpimorphismKeyboard',
 'mouse_handler': 'DefaultEpimorphismMouse',

 'OSC_enabled': False,
 'OSC_handler': 'DefaultEpimorphismOSC',
 'OSC_client_address': ('192.168.42.69', 9000),
 'OSC_echo': True,

 'state_intrp_time': 4.0,

 'screen': [800,800,False],
 'kernel_dim': 1280,
 'fract': 3,

 'sources': ['util', 'math', 'colorspace', 'epi_cull', 'epi_reduce', 'epi_reset', 'epi_color', 'epi_seed_c', 'epi_seed_a', 'epi_seed_wt', 'epi_seed_w', 'epi_seed', 'epi_post', 'epi_kernels'],
 'kernel': 'epimorphism',
 'lib_prefix': 'epi',
 'feedback_buffer': True
}

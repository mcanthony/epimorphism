{
 'app': 'epimorphism',
 'name': 'default',
 'state': State('epimorphism', 'default'),

 'keyboard_handler': 'DefaultEpimorphismKeyboard',
 'mouse_handler': 'DefaultEpimorphismMouse',

 'OSC_enabled': True,
 'OSC_handler': 'DefaultEpimorphismOSC',
 'OSC_client_address': ('192.168.200.3', 9000),
 'OSC_echo': True,

 'screen': [800,800,False],
 'kernel_dim': 1536,
 'fract': 3,

 'sources': ['util', 'math', 'colorspace', 'epi_cull', 'epi_reduce', 'epi_reset', 'epi_color', 'epi_seed_c', 'epi_seed_a', 'epi_seed_wt', 'epi_seed_w', 'epi_seed', 'epi_kernels'], 
 'kernel': 'epimorphism',
 'lib_prefix': 'epi',
 'feedback_buffer': True
}
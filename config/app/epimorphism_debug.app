{
 'app': 'epimorphism',
 'name': 'debug',
 'state': State('epimorphism', 'debug'),

 'keyboard_handler': 'DefaultEpimorphismKeyboard',
 'mouse_handler': 'DefaultEpimorphismMouse',

 'OSC_enabled': False,
 'OSC_handler': 'DefaultEpimorphismOSC',
 'OSC_client_address': ('192.168.200.3', 9000),
 'OSC_echo': True,

 'screen': [800,800,False],
 'kernel_dim': 1024,
 'fract': 3,
  'debug_freq': 1,
 'print_timing_info': True,
 

 'sources': ['util', 'math', 'colorspace', 'epi_cull', 'epi_reduce', 'epi_reset', 'epi_color', 'epi_seed_c', 'epi_seed_a', 'epi_seed_wt', 'epi_seed_w', 'epi_seed', 'epi_debug'], 
 'kernel': 'epimorphism',
 'lib_prefix': 'epi',
 'feedback_buffer': True
}
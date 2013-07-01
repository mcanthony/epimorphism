{
 'app': 'epimorphism',
 'name': 'default',
 'state': State('epimorphism', 'default'),

 'keyboard_handler': 'DefaultEpimorphismKeyboard',
 'mouse_handler': 'DefaultEpimorphismMouse',

 'OSC_enabled': False,
 'OSC_handler': 'EpimorphismOSC',
 'OSC_client_address': ('10.0.0.116', 9001),
 'OSC_echo': True,

 'state_intrp_time': 2.0,

 'screen': [800,800,False],
 'kernel_dim': 1280,
 'fract': 3,

 'sources': ['epi_kernels'], 
 'kernel': 'epimorphism',
 'lib_prefix': 'epi',
 'feedback_buffer': True
}


{
 'app': 'epimorphism',
 'name': 'default',
 'state': State('epimorphism', 'default'),

 'keyboard_handler': 'DefaultEpimorphismKeyboard',
 'mouse_handler': 'DefaultEpimorphismMouse',

 'OSC_enabled': False,
 'OSC_handler': 'DefaultEpimorphismOSC',
 'OSC_client_address': ('192.168.200.3', 8000),
 'OSC_echo': True,

 'screen': [800,800,False],
 'kernel_dim': 1536,
 
 'kernel': 'epimorphism',
 'lib_prefix': 'epi',
 'feedback_buffer': True,
 'substitutions': {'FRACT':'3', 'CULL_ENABLED': "#define CULL_ENABLED"}
}
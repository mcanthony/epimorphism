{
 'app': 'interference',
 'name': 'default',
 'state': State('interference', 'default'),

 'keyboard_handler': 'DefaultInterferenceKeyboard',
 'mouse_handler': 'DefaultInterferenceMouse',

 'OSC_enabled': True,
 'OSC_handler': 'DefaultInterferenceOSC',
 'OSC_client_address': ('192.168.200.3', 9000),
 'OSC_echo': True,

 'screen': [800,800,False],
 'kernel_dim': 1536,

 'sources': ['util', 'math', 'colorspace', 'interference', 'post1'], 
 'kernel': 'interference',
 'lib_prefix': 'int',
 'feedback_buffer': True
}
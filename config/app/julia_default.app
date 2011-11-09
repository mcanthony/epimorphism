{
 'app': 'julia',
 'name': 'default',
 'state': State('julia', 'default'),

 'autostart': True,
 'exit': False,
 'freeze': False,
 'console_level': 10,

 'manual_iter': False,
 'next_frame': False,

 'render_video': False,
 'max_video_frames': 10800,
 'video_frame_rate': 30.0,
 'fps_sync': False,
 'record_events': False,

 'component_level': 'FULL',
 'state_intrp_time': 3.0,

 'server': False,

 'kbd_switch_spd' : .25,
 'keyboard_handler': 'DefaultJuliaKeyboard',
 'par_scale': 0.5,

 'mouse_handler': 'DefaultMouse',

 'midi_enabled': False,
 'midi_echo': False,
 'midi_controller': [],
 'midi_speed': 0.5,
 'last_midi_event': 0.0,

 'OSC_enabled': True,
 'OSC_handler': 'DefaultOSCHandler',
 'OSC_input_port': 8000,
 'OSC_client_address': ('192.168.200.3', 9000),
 'OSC_echo': True,

 'screen' : [800,800,False],
 'echo' : True,

 'viewport' : [0.0, 0.0, 1.0],

 'print_timing_info': True,
 'debug_freq': 10.0,
 'kernel_dim': 1536,

 'kernel': 'julia',
 'sources': ['util', 'math', 'colorspace', 'julia'],
 'lib_prefix': 'jul',
 'feedback_buffer': False
}
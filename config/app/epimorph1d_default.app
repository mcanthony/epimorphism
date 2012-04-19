{'app':'epimorph1d',
 'state': State('epimorph1d', 'default'),
 'sources': ['util', 'math', 'colorspace', 'epimorph1d'],
 'kernel': 'epimorph1d',

 'keyboard_handler': 'DefaultEpimorphismKeyboard',
 'mouse_handler': 'DefaultEpimorphismMouse',

 'state_intrp_time': 1.0,

 'screen': [800,800,False],
 'kernel_dim': 1536,
 'fract': 3,

 'sources': ['util', 'math', 'colorspace', 'epi_cull', 'epi_reduce', 'epi_reset', 'epi_color', 'epi_seed_c', 'epi_seed_a', 'epi_seed_wt', 'epi_seed_w', 'epi_seed', 'epimorph1d'], 
 'kernel': 'epimorphism',
 'lib_prefix': 'epi',
 'feedback_buffer': '1'


 }
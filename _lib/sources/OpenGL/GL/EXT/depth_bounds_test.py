'''OpenGL extension EXT.depth_bounds_test

This module customises the behaviour of the 
OpenGL.raw.GL.EXT.depth_bounds_test to provide a more 
Python-friendly API
'''
from OpenGL import platform, constants, constant, arrays
from OpenGL import extensions, wrapper
from OpenGL.GL import glget
import ctypes
from OpenGL.raw.GL.EXT.depth_bounds_test import *
### END AUTOGENERATED SECTION
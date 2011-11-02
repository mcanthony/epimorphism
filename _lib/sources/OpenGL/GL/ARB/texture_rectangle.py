'''OpenGL extension ARB.texture_rectangle

This module customises the behaviour of the 
OpenGL.raw.GL.ARB.texture_rectangle to provide a more 
Python-friendly API
'''
from OpenGL import platform, constants, constant, arrays
from OpenGL import extensions, wrapper
from OpenGL.GL import glget
import ctypes
from OpenGL.raw.GL.ARB.texture_rectangle import *
### END AUTOGENERATED SECTION
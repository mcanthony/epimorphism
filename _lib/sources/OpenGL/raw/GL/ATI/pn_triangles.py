'''OpenGL extension ATI.pn_triangles

Overview (from the spec)
	
	ATI_pn_triangles provides a path for enabling the GL to internally 
	tessellate input geometry into curved patches.  The extension allows the 
	user to tune the amount of tessellation to be performed on each triangle as 
	a global state value.  The intent of PN Triangle tessellation is 
	typically to produce geometry with a smoother silhouette and more organic 
	shape.
	
	The tessellated patch will replace the triangles input into the GL.  
	The GL will generate new vertices in object-space, prior to geometry 
	transformation.  Only the vertices and normals are required to produce 
	proper results, and the rest of the information per vertex is interpolated 
	linearly across the patch.  

The official definition of this extension is available here:
	http://oss.sgi.com/projects/ogl-sample/registry/ATI/pn_triangles.txt

Automatically generated by the get_gl_extensions script, do not edit!
'''
from OpenGL import platform, constants, constant, arrays
from OpenGL import extensions
from OpenGL.GL import glget
import ctypes
EXTENSION_NAME = 'GL_ATI_pn_triangles'
GL_PN_TRIANGLES_ATI = constant.Constant( 'GL_PN_TRIANGLES_ATI', 0x87F0 )
GL_MAX_PN_TRIANGLES_TESSELATION_LEVEL_ATI = constant.Constant( 'GL_MAX_PN_TRIANGLES_TESSELATION_LEVEL_ATI', 0x87F1 )
glget.addGLGetConstant( GL_MAX_PN_TRIANGLES_TESSELATION_LEVEL_ATI, (1,) )
GL_PN_TRIANGLES_POINT_MODE_ATI = constant.Constant( 'GL_PN_TRIANGLES_POINT_MODE_ATI', 0x87F2 )
glget.addGLGetConstant( GL_PN_TRIANGLES_POINT_MODE_ATI, (1,) )
GL_PN_TRIANGLES_NORMAL_MODE_ATI = constant.Constant( 'GL_PN_TRIANGLES_NORMAL_MODE_ATI', 0x87F3 )
glget.addGLGetConstant( GL_PN_TRIANGLES_NORMAL_MODE_ATI, (1,) )
GL_PN_TRIANGLES_TESSELATION_LEVEL_ATI = constant.Constant( 'GL_PN_TRIANGLES_TESSELATION_LEVEL_ATI', 0x87F4 )
glget.addGLGetConstant( GL_PN_TRIANGLES_TESSELATION_LEVEL_ATI, (1,) )
GL_PN_TRIANGLES_POINT_MODE_LINEAR_ATI = constant.Constant( 'GL_PN_TRIANGLES_POINT_MODE_LINEAR_ATI', 0x87F5 )
GL_PN_TRIANGLES_POINT_MODE_CUBIC_ATI = constant.Constant( 'GL_PN_TRIANGLES_POINT_MODE_CUBIC_ATI', 0x87F6 )
GL_PN_TRIANGLES_NORMAL_MODE_LINEAR_ATI = constant.Constant( 'GL_PN_TRIANGLES_NORMAL_MODE_LINEAR_ATI', 0x87F7 )
GL_PN_TRIANGLES_NORMAL_MODE_QUADRATIC_ATI = constant.Constant( 'GL_PN_TRIANGLES_NORMAL_MODE_QUADRATIC_ATI', 0x87F8 )
glPNTrianglesiATI = platform.createExtensionFunction( 
	'glPNTrianglesiATI', dll=platform.GL,
	extension=EXTENSION_NAME,
	resultType=None, 
	argTypes=(constants.GLenum, constants.GLint,),
	doc = 'glPNTrianglesiATI( GLenum(pname), GLint(param) ) -> None',
	argNames = ('pname', 'param',),
)

glPNTrianglesfATI = platform.createExtensionFunction( 
	'glPNTrianglesfATI', dll=platform.GL,
	extension=EXTENSION_NAME,
	resultType=None, 
	argTypes=(constants.GLenum, constants.GLfloat,),
	doc = 'glPNTrianglesfATI( GLenum(pname), GLfloat(param) ) -> None',
	argNames = ('pname', 'param',),
)


def glInitPnTrianglesATI():
	'''Return boolean indicating whether this extension is available'''
	return extensions.hasGLExtension( EXTENSION_NAME )
from distutils.core import setup, Extension

module1 = Extension('opencl_interface',
                    define_macros = [('MAJOR_VERSION', '1'),
                                     ('MINOR_VERSION', '0')],
                    include_dirs = ['/home/gene/epimorphism/opencl'],
                    libraries = ['GL', 'GLU','X11','Xmu','OpenCL', 'glut'],
                    sources = ['opencl.cpp'])

setup (name = 'opencl_interface',
       version = '1.0',
       author = 'Epimorphism',
       ext_modules = [module1])

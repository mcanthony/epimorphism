/*
 * Copyright 1993-2010 NVIDIA Corporation.  All rights reserved.
 *
 * NVIDIA Corporation and its licensors retain all intellectual property and 
 * proprietary rights in and to this software and related documentation. 
 * Any use, reproduction, disclosure, or distribution of this software 
 * and related documentation without an express license agreement from
 * NVIDIA Corporation is strictly prohibited.
 *
 * Please refer to the applicable NVIDIA end user license agreement (EULA) 
 * associated with this source code for terms and conditions that govern 
 * your use of this NVIDIA software.
 * 
 */

// *********************************************************************
// Demo application for postprocessing of OpenGL renderings with OpenCL
// Based on the CUDA postprocessGL sample
// *********************************************************************

#include <Python.h>

#define UNIX

// All OpenCL headers
#if defined (__APPLE__) || defined(MACOSX)
    #include <OpenCL/opencl.h>
#else
    #include <CL/opencl.h>
#endif 

// reminders for build output window and log
#ifdef _WIN32
    #pragma message ("Note: including opencl.h")
#endif


// GLEW and GLUT includes
#include <GL/glew.h>

#ifdef UNIX
	#if defined(__APPLE__) || defined(MACOSX)
	    #include <OpenGL/OpenGL.h>
	    #include <GLUT/glut.h>
	#else
	    #include <GL/glut.h>
	    #include <GL/glx.h>
	#endif
#endif


#if defined (__APPLE__) || defined(MACOSX)
   #define GL_SHARING_EXTENSION "cl_APPLE_gl_sharing"
#else
   #define GL_SHARING_EXTENSION "cl_khr_gl_sharing"
#endif


// constants / global variables
//*****************************************************************************

// CL objects
cl_context cxGPUContext;
cl_command_queue cqCommandQueue;
cl_device_id device;
cl_uint uiNumDevsUsed = 1;          // Number of devices used in this sample 
cl_program cpProgram;
cl_kernel ckKernel;
size_t szGlobalWorkSize[2];
size_t szLocalWorkSize[2];
cl_mem cl_pbos[2] = {0,0};
cl_int ciErrNum;

/*
//*****************************************************************************
void pboRegister()
{    
    // Transfer ownership of buffer from GL to CL
		glFlush();
        clEnqueueAcquireGLObjects(cqCommandQueue,2, cl_pbos, 0, NULL, NULL);

}

//*****************************************************************************
void pboUnregister()
{
        // Transfer ownership of buffer back from CL to GL
        clEnqueueReleaseGLObjects(cqCommandQueue,2, cl_pbos, 0, NULL, NULL);
	clFinish(cqCommandQueue);
}



// Kernel function
//*****************************************************************************
int executeKernel(cl_int radius)
{

    // set global and local work item dimensions
    szLocalWorkSize[0] = 16;
    szLocalWorkSize[1] = 16;
  szGlobalWorkSize[0] = (int)((float)image_width / 16);//shrRoundUp((int)szLocalWorkSize[0], image_width);
  szGlobalWorkSize[1] = (int)((float)image_height / 16);//shrRoundUp((int)szLocalWorkSize[1], image_height);

    //    szGlobalWorkSize[0] = shrRoundUp((int)szLocalWorkSize[0], image_width);
    //szGlobalWorkSize[1] = shrRoundUp((int)szLocalWorkSize[1], image_height);


    ciErrNum |= clEnqueueNDRangeKernel(cqCommandQueue, ckKernel, 2, NULL,
                                      szGlobalWorkSize, szLocalWorkSize, 
                                     0, NULL, NULL);

    oclCheckErrorEX(ciErrNum, CL_SUCCESS, pCleanup);

    return 0;
}

// copy image and process using OpenCL
//*****************************************************************************
void processImage()
{
    // activate destination buffer
    glBindBuffer(GL_PIXEL_PACK_BUFFER_ARB, pbo_source);

    //// read data into pbo. note: use BGRA format for optimal performance
    glReadPixels(0, 0, image_width, image_height, GL_BGRA, GL_UNSIGNED_BYTE, NULL); 


            pboRegister();
            executeKernel(blur_radius);
            pboUnregister();


        // download texture from PBO
        glBindBuffer(GL_PIXEL_UNPACK_BUFFER_ARB, pbo_dest);
        glBindTexture(GL_TEXTURE_2D, tex_screen);
        glTexSubImage2D(GL_TEXTURE_2D, 0, 0, 0, 
                        image_width, image_height, 
                        GL_BGRA, GL_UNSIGNED_BYTE, NULL);


}


// Function to clean up and exit
//*****************************************************************************
void Cleanup(int iExitCode)
{

    if(cqCommandQueue)clReleaseCommandQueue(cqCommandQueue);
    if(cxGPUContext)clReleaseContext(cxGPUContext);
    exit (iExitCode);
}

*/

// Init OpenCL - make this get correct platform & device
//*****************************************************************************
static PyObject *
initCL(PyObject *self, PyObject *args)
{
    cl_platform_id cpPlatform;
    cl_uint uiDevCount;
    cl_device_id *cdDevices;
    cl_uint num_platforms; 
    cl_platform_id* clPlatformIDs;

    // init GL
    int argc = 0;
    char** argv;
    glutInit(&argc, (char**)argv);
    glutCreateWindow("dummy window");

    // get platform
    ciErrNum = clGetPlatformIDs (0, NULL, &num_platforms);
    clPlatformIDs = (cl_platform_id*)malloc(num_platforms * sizeof(cl_platform_id));
    
    if(ciErrNum != CL_SUCCESS) {printf("Error getting # platforms\n"); return Py_BuildValue("i", ciErrNum);}
    ciErrNum = clGetPlatformIDs (num_platforms, clPlatformIDs, NULL);
    
    if(ciErrNum != CL_SUCCESS) {printf("Error getting platform ids\n"); return Py_BuildValue("i", ciErrNum);}
    cpPlatform = clPlatformIDs[0];
    
    // Get the number of GPU devices available to the platform
    ciErrNum = clGetDeviceIDs(cpPlatform, CL_DEVICE_TYPE_GPU, 0, NULL, &uiDevCount);

    if(ciErrNum != CL_SUCCESS) {printf("Error getting # devices\n"); return Py_BuildValue("i", ciErrNum);}

    // Create the device list
    cdDevices = new cl_device_id [uiDevCount];
    ciErrNum = clGetDeviceIDs(cpPlatform, CL_DEVICE_TYPE_GPU, uiDevCount, cdDevices, NULL);
    if(ciErrNum != CL_SUCCESS) {printf("Error getting device list\n"); return Py_BuildValue("i", ciErrNum);}
    
    // Define OS-specific context properties and create the OpenCL context
    #if defined (__APPLE__) || defined (MACOSX)
    CGLContextObj kCGLContext = CGLGetCurrentContext();
    CGLShareGroupObj kCGLShareGroup = CGLGetShareGroup(kCGLContext);
    cl_context_properties props[] = 
      {
	CL_CONTEXT_PROPERTY_USE_CGL_SHAREGROUP_APPLE, (cl_context_properties)kCGLShareGroup, 
	0 
      };
    cxGPUContext = clCreateContext(props, 0,0, NULL, NULL, &ciErrNum);
    #else
    #ifdef UNIX
    cl_context_properties props[] = 
      {
	CL_GL_CONTEXT_KHR, (cl_context_properties)glXGetCurrentContext(), 
	CL_GLX_DISPLAY_KHR, (cl_context_properties)glXGetCurrentDisplay(), 
	CL_CONTEXT_PLATFORM, (cl_context_properties)cpPlatform, 
	0
      };
    cxGPUContext = clCreateContext(props, 1, &cdDevices[0], NULL, NULL, &ciErrNum);
    #else // Win32
    cl_context_properties props[] = 
      {
	CL_GL_CONTEXT_KHR, (cl_context_properties)wglGetCurrentContext(), 
	CL_WGL_HDC_KHR, (cl_context_properties)wglGetCurrentDC(), 
	CL_CONTEXT_PLATFORM, (cl_context_properties)cpPlatform, 
	0
      };
    cxGPUContext = clCreateContext(props, 1, &cdDevices[0], NULL, NULL, &ciErrNum);
    #endif
    #endif

    if(ciErrNum != CL_SUCCESS) {printf("Error creating context\n"); return Py_BuildValue("i", ciErrNum);}

    // create a command-queue
    cqCommandQueue = clCreateCommandQueue(cxGPUContext, cdDevices[0], 0, &ciErrNum);
    if(ciErrNum != CL_SUCCESS) {printf("Error create queue\n"); return Py_BuildValue("i", ciErrNum);}

    return Py_BuildValue("i", CL_SUCCESS);
}

// Init OpenCL - make this get correct platform & device
//*****************************************************************************
static PyObject *
compileKernel(PyObject *self, PyObject *args)
{
  return Py_BuildValue("i", CL_SUCCESS);
}


int main(int argc, const char** argv) 
{
  return 0;
}


// Module initialization
static PyMethodDef OpenCLInterfaceMethods[] = {   
    {"initCL", initCL, METH_VARARGS,
     "Initialize the OpenCL interface."},    
    {"compileKernel", compileKernel, METH_VARARGS,
     "Initialize the OpenCL interface."},    
    {NULL, NULL, 0, NULL}        /* Sentinel */
};


PyMODINIT_FUNC
initopencl_interface(void)
{
    (void) Py_InitModule("opencl_interface", OpenCLInterfaceMethods);
}



# cl_platform_info
PLATFORM_PROFILE     =                   0x0900
PLATFORM_VERSION     =                   0x0901
PLATFORM_NAME        =                   0x0902
PLATFORM_VENDOR      =                   0x0903

# opengl interop
CURRENT_DEVICE_FOR_GL_CONTEXT_KHR =    0x2006
DEVICES_FOR_GL_CONTEXT_KHR =           0x2007
GL_CONTEXT_KHR =                       0x2008
EGL_DISPLAY_KHR =                      0x2009
GLX_DISPLAY_KHR =                      0x200A
WGL_HDC_KHR =                          0x200B
CGL_SHAREGROUP_KHR =                   0x200C

# cl_device_type - bitfield
DEVICE_TYPE_DEFAULT = 1<<0
DEVICE_TYPE_CPU = 1<<1
DEVICE_TYPE_GPU = 1<<2
DEVICE_TYPE_ACCELERATOR = 1<<3
DEVICE_TYPE_ALL = 0xFFFFFFFF

# cl_context_info
CONTEXT_REFERENCE_COUNT = 0x1080
#CONTEXT_NUM_DEVICES     = 0x1081
CONTEXT_DEVICES         = 0x1081
CONTEXT_PROPERTIES      = 0x1083
CONTEXT_PLATFORM        = 0x1084

DEVICE_QUEUE_PROPERTIES = 0x102a
DEVICE_NAME             = 0x102b
DEVICE_VENDOR           = 0x102c
DRIVER_VERSION          = 0x102d
DEVICE_PROFILE          = 0x102e
DEVICE_VERSION          = 0x102f
DEVICE_EXTENSIONS       = 0x1030
DEVICE_PLATFORM         = 0x1031

PLATFORM_NVIDIA         = 0x3001

MEM_READ_WRITE          = 1<<0
MEM_WRITE_ONLY          = 1<<1
MEM_READ_ONLY           = 1<<2
MEM_USE_HOST_PTR        = 1<<3
MEM_ALLOC_HOST_PTR      = 1<<4
MEM_COPY_HOST_PTR       = 1<<5

# cl_command_queue_properties - bitfield
QUEUE_OUT_OF_ORDER_EXEC_MODE_ENABLE      = (1 << 0)
QUEUE_PROFILING_ENABLE                   = (1 << 1)

# OpenCL Version
VERSION_1_0 =                               1

# cl_bool
FALSE =                                     0
TRUE =                                      1

# cl_platform_info
PLATFORM_PROFILE =                          0x0900
PLATFORM_VERSION =                          0x0901
PLATFORM_NAME =                             0x0902
PLATFORM_VENDOR =                           0x0903
PLATFORM_EXTENSIONS =                       0x0904

# cl_device_type - bitfield
DEVICE_TYPE_DEFAULT =                       (1 << 0)
DEVICE_TYPE_CPU =                           (1 << 1)
DEVICE_TYPE_GPU =                           (1 << 2)
DEVICE_TYPE_ACCELERATOR =                   (1 << 3)
DEVICE_TYPE_ALL =                           0xFFFFFFFF

# cl_device_info
DEVICE_TYPE =                               0x1000
DEVICE_VENDOR_ID =                          0x1001
DEVICE_MAX_COMPUTE_UNITS =                  0x1002
DEVICE_MAX_WORK_ITEM_DIMENSIONS =           0x1003
DEVICE_MAX_WORK_GROUP_SIZE =                0x1004
DEVICE_MAX_WORK_ITEM_SIZES =                0x1005
DEVICE_PREFERRED_VECTOR_WIDTH_CHAR =        0x1006
DEVICE_PREFERRED_VECTOR_WIDTH_SHORT =       0x1007
DEVICE_PREFERRED_VECTOR_WIDTH_INT =         0x1008
DEVICE_PREFERRED_VECTOR_WIDTH_LONG =        0x1009
DEVICE_PREFERRED_VECTOR_WIDTH_FLOAT =       0x100A
DEVICE_PREFERRED_VECTOR_WIDTH_DOUBLE =      0x100B
DEVICE_MAX_CLOCK_FREQUENCY =                0x100C
DEVICE_ADDRESS_BITS =                       0x100D
DEVICE_MAX_READ_IMAGE_ARGS =                0x100E
DEVICE_MAX_WRITE_IMAGE_ARGS =               0x100F
DEVICE_MAX_MEM_ALLOC_SIZE =                 0x1010
DEVICE_IMAGE2D_MAX_WIDTH =                  0x1011
DEVICE_IMAGE2D_MAX_HEIGHT =                 0x1012
DEVICE_IMAGE3D_MAX_WIDTH =                  0x1013
DEVICE_IMAGE3D_MAX_HEIGHT =                 0x1014
DEVICE_IMAGE3D_MAX_DEPTH =                  0x1015
DEVICE_IMAGE_SUPPORT =                      0x1016
DEVICE_MAX_PARAMETER_SIZE =                 0x1017
DEVICE_MAX_SAMPLERS =                       0x1018
DEVICE_MEM_BASE_ADDR_ALIGN =                0x1019
DEVICE_MIN_DATA_TYPE_ALIGN_SIZE =           0x101A
DEVICE_SINGLE_FP_CONFIG =                   0x101B
DEVICE_GLOBAL_MEM_CACHE_TYPE =              0x101C
DEVICE_GLOBAL_MEM_CACHELINE_SIZE =          0x101D
DEVICE_GLOBAL_MEM_CACHE_SIZE =              0x101E
DEVICE_GLOBAL_MEM_SIZE =                    0x101F
DEVICE_MAX_CONSTANT_BUFFER_SIZE =           0x1020
DEVICE_MAX_CONSTANT_ARGS =                  0x1021
DEVICE_LOCAL_MEM_TYPE =                     0x1022
DEVICE_LOCAL_MEM_SIZE =                     0x1023
DEVICE_ERROR_CORRECTION_SUPPORT =           0x1024
DEVICE_PROFILING_TIMER_RESOLUTION =         0x1025
DEVICE_ENDIAN_LITTLE =                      0x1026
DEVICE_AVAILABLE =                          0x1027
DEVICE_COMPILER_AVAILABLE =                 0x1028
DEVICE_EXECUTION_CAPABILITIES =             0x1029
DEVICE_QUEUE_PROPERTIES =                   0x102A
DEVICE_NAME =                               0x102B
DEVICE_VENDOR =                             0x102C
DRIVER_VERSION =                            0x102D
DEVICE_PROFILE =                            0x102E
DEVICE_VERSION =                            0x102F
DEVICE_EXTENSIONS =                         0x1030
DEVICE_PLATFORM =                           0x1031
	
# cl_device_fp_config - bitfield
FP_DENORM =                                 (1 << 0)
FP_INF_NAN =                                (1 << 1)
FP_ROUND_TO_NEAREST =                       (1 << 2)
FP_ROUND_TO_ZERO =                          (1 << 3)
FP_ROUND_TO_INF =                           (1 << 4)
FP_FMA =                                    (1 << 5)

# cl_device_mem_cache_type
NONE =                                      0x0
READ_ONLY_CACHE =                           0x1
READ_WRITE_CACHE =                          0x2

# cl_device_local_mem_type
LOCAL =                                     0x1
GLOBAL =                                    0x2

# cl_device_exec_capabilities - bitfield
EXEC_KERNEL =                               (1 << 0)
EXEC_NATIVE_KERNEL =                        (1 << 1)

# cl_command_queue_properties - bitfield
QUEUE_OUT_OF_ORDER_EXEC_MODE_ENABLE =       (1 << 0)
QUEUE_PROFILING_ENABLE =                    (1 << 1)

# cl_context_info
CONTEXT_REFERENCE_COUNT =                   0x1080
CONTEXT_DEVICES =                           0x1081
CONTEXT_PROPERTIES =                        0x1082

# cl_context_properties
CONTEXT_PLATFORM =                          0x1084

# cl_command_queue_info
QUEUE_CONTEXT =                             0x1090
QUEUE_DEVICE =                              0x1091
QUEUE_REFERENCE_COUNT =                     0x1092
QUEUE_PROPERTIES =                          0x1093

# cl_mem_flags - bitfield
MEM_READ_WRITE =                            (1 << 0)
MEM_WRITE_ONLY =                            (1 << 1)
MEM_READ_ONLY =                             (1 << 2)
MEM_USE_HOST_PTR =                          (1 << 3)
MEM_ALLOC_HOST_PTR =                        (1 << 4)
MEM_COPY_HOST_PTR =                         (1 << 5)

# cl_channel_order
R =                                       0x10B0
A =                                       0x10B1
RG =                                        0x10B2
RA =                                        0x10B3
RGB =                                       0x10B4
RGBA =                                      0x10B5
BGRA =                                      0x10B6
ARGB =                                      0x10B7
INTENSITY =                                 0x10B8
LUMINANCE =                                 0x10B9

# cl_channel_type
SNORM_INT8 =                                0x10D0
SNORM_INT16 =                               0x10D1
UNORM_INT8 =                                0x10D2
UNORM_INT16 =                               0x10D3
UNORM_SHORT_565 =                           0x10D4
UNORM_SHORT_555 =                           0x10D5
UNORM_INT_101010 =                          0x10D6
SIGNED_INT8 =                               0x10D7
SIGNED_INT16 =                              0x10D8
SIGNED_INT32 =                              0x10D9
UNSIGNED_INT8 =                             0x10DA
UNSIGNED_INT16 =                            0x10DB
UNSIGNED_INT32 =                            0x10DC
HALF_FLOAT =                                0x10DD
FLOAT =                                     0x10DE

# cl_mem_object_type
MEM_OBJECT_BUFFER =                         0x10F0
MEM_OBJECT_IMAGE2D =                        0x10F1
MEM_OBJECT_IMAGE3D =                        0x10F2

# cl_mem_info
MEM_TYPE =                                  0x1100
MEM_FLAGS =                                 0x1101
MEM_SIZE =                                  0x1102
MEM_HOST_PTR =                              0x1103
MEM_MAP_COUNT =                             0x1104
MEM_REFERENCE_COUNT =                       0x1105
MEM_CONTEXT =                               0x1106

# cl_image_info
IMAGE_FORMAT =                              0x1110
IMAGE_ELEMENT_SIZE =                        0x1111
IMAGE_ROW_PITCH =                           0x1112
IMAGE_SLICE_PITCH =                         0x1113
IMAGE_WIDTH =                               0x1114
IMAGE_HEIGHT =                              0x1115
IMAGE_DEPTH =                               0x1116

# cl_addressing_mode
ADDRESS_NONE =                              0x1130
ADDRESS_CLAMP_TO_EDGE =                     0x1131
ADDRESS_CLAMP =                             0x1132
ADDRESS_REPEAT =                            0x1133

# cl_filter_mode
FILTER_NEAREST =                            0x1140
FILTER_LINEAR =                             0x1141

# cl_sampler_info
SAMPLER_REFERENCE_COUNT =                   0x1150
SAMPLER_CONTEXT =                           0x1151
SAMPLER_NORMALIZED_COORDS =                 0x1152
SAMPLER_ADDRESSING_MODE =                   0x1153
SAMPLER_FILTER_MODE =                       0x1154

# cl_map_flags - bitfield
MAP_READ =                                  (1 << 0)
MAP_WRITE =                                 (1 << 1)

# cl_program_info
PROGRAM_REFERENCE_COUNT =                   0x1160
PROGRAM_CONTEXT =                           0x1161
PROGRAM_NUM_DEVICES =                       0x1162
PROGRAM_DEVICES =                           0x1163
PROGRAM_SOURCE =                            0x1164
PROGRAM_BINARY_SIZES =                      0x1165
PROGRAM_BINARIES =                          0x1166

# cl_program_build_info
PROGRAM_BUILD_STATUS =                      0x1181
PROGRAM_BUILD_OPTIONS =                     0x1182
PROGRAM_BUILD_LOG =                         0x1183

# cl_build_status
BUILD_SUCCESS =                             0
BUILD_NONE =                                -1
BUILD_ERROR =                               -2
BUILD_IN_PROGRESS =                         -3

# cl_kernel_info
KERNEL_FUNCTION_NAME =                      0x1190
KERNEL_NUM_ARGS =                           0x1191
KERNEL_REFERENCE_COUNT =                    0x1192
KERNEL_CONTEXT =                            0x1193
KERNEL_PROGRAM =                            0x1194

# cl_kernel_work_group_info
KERNEL_WORK_GROUP_SIZE =                    0x11B0
KERNEL_COMPILE_WORK_GROUP_SIZE =            0x11B1
KERNEL_LOCAL_MEM_SIZE =                     0x11B2

# cl_event_info
EVENT_COMMAND_QUEUE =                       0x11D0
EVENT_COMMAND_TYPE =                        0x11D1
EVENT_REFERENCE_COUNT =                     0x11D2
EVENT_COMMAND_EXECUTION_STATUS =            0x11D3

# cl_command_type
COMMAND_NDRANGE_KERNEL =                    0x11F0
COMMAND_TASK =                              0x11F1
COMMAND_NATIVE_KERNEL =                     0x11F2
COMMAND_READ_BUFFER =                       0x11F3
COMMAND_WRITE_BUFFER =                      0x11F4
COMMAND_COPY_BUFFER =                       0x11F5
COMMAND_READ_IMAGE =                        0x11F6
COMMAND_WRITE_IMAGE =                       0x11F7
COMMAND_COPY_IMAGE =                        0x11F8
COMMAND_COPY_IMAGE_TO_BUFFER =              0x11F9
COMMAND_COPY_BUFFER_TO_IMAGE =              0x11FA
COMMAND_MAP_BUFFER =                        0x11FB
COMMAND_MAP_IMAGE =                         0x11FC
COMMAND_UNMAP_MEM_OBJECT =                  0x11FD
COMMAND_MARKER =                            0x11FE
COMMAND_ACQUIRE_GL_OBJECTS =                0x11FF
COMMAND_RELEASE_GL_OBJECTS =                0x1200

# command execution status
COMPLETE =                                  0x0
RUNNING =                                   0x1
SUBMITTED =                                 0x2
QUEUED =                                    0x3
  
# cl_profiling_info
PROFILING_COMMAND_QUEUED =                  0x1280
PROFILING_COMMAND_SUBMIT =                  0x1281
PROFILING_COMMAND_START =                   0x1282
PROFILING_COMMAND_END =                     0x1283


ERROR_CODES = {0: 'Success',                
               -1: 'Device not found',
               -2: 'Device not available',
               -3: 'Device compiler not available',
               -4: 'Memory object allocation failure',
               -5: 'Out of resources',
               -6: 'Out of host memory',
               -7: 'Profiling info not available',
               -8: 'Memory copy overlap',
               -9: 'Image format mismatch',
               -10: 'Image format not supported',
               -11: 'Build program failure',
               -12: 'Map failure',
               
               -30: 'Invalid value',
               -31: 'Invalid device type',
               -32: 'Invalid platform',
               -33: 'Invalid device',
               -34: 'Invalid context',
               -35: 'Invalid queue properties',
               -36: 'Invalid command queue',
               -37: 'Invalid host pointer',
               -38: 'Invalid memory object',
               -39: 'Invalid image format description',
               -40: 'Invalid image size',
               -41: 'Invalid sampler',
               -42: 'Invalid binary',
               -43: 'Invalid build options',
               -44: 'Invalid program',
               -45: 'Invalid program executable',
               -46: 'Invalid kernel name',
               -47: 'Invalid kernel definition',
               -48: 'Invalid kernel',
               -49: 'Invalid argument index',
               -50: 'Invalid argument value',
               -51: 'Invalid argument size',
               -52: 'Invalid kernel arguments',
               -53: 'Invalid work dimension',
               -54: 'Invalid work group size',
               -55: 'Invalid work item size',
               -56: 'Invalid global offset',
               -57: 'Invalid event wait list',
               -58: 'Invalid event',
               -59: 'Invalid operation',
               -60: 'Invalid GL object',
               -61: 'Invalid buffer size',
               -62: 'Invalid MIP level'}


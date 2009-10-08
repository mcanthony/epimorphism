/* 0.9.7.2 on Fri Oct  9 09:11:16 2009 */

#define PY_SSIZE_T_CLEAN
#include "Python.h"
#include "structmember.h"
#ifndef PY_LONG_LONG
  #define PY_LONG_LONG LONG_LONG
#endif
#if PY_VERSION_HEX < 0x02050000
  typedef int Py_ssize_t;
  #define PY_SSIZE_T_MAX INT_MAX
  #define PY_SSIZE_T_MIN INT_MIN
  #define PyInt_FromSsize_t(z) PyInt_FromLong(z)
  #define PyInt_AsSsize_t(o)	PyInt_AsLong(o)
#endif
#ifndef WIN32
  #ifndef __stdcall
    #define __stdcall
  #endif
  #ifndef __cdecl
    #define __cdecl
  #endif
#endif
#ifdef __cplusplus
#define __PYX_EXTERN_C extern "C"
#else
#define __PYX_EXTERN_C extern
#endif
#include <math.h>
#include "portmidi.h"
#include "porttime.h"


typedef struct {PyObject **p; char *s;} __Pyx_InternTabEntry; /*proto*/
typedef struct {PyObject **p; char *s; long n;} __Pyx_StringTabEntry; /*proto*/

static PyObject *__pyx_m;
static PyObject *__pyx_b;
static int __pyx_lineno;
static char *__pyx_filename;
static char **__pyx_f;

static PyObject *__Pyx_Import(PyObject *name, PyObject *from_list); /*proto*/

static int __Pyx_PrintItem(PyObject *); /*proto*/
static int __Pyx_PrintNewline(void); /*proto*/

static void __Pyx_Raise(PyObject *type, PyObject *value, PyObject *tb); /*proto*/

static PyObject *__Pyx_GetName(PyObject *dict, PyObject *name); /*proto*/

static PyObject *__Pyx_GetItemInt(PyObject *o, Py_ssize_t i); /*proto*/

static int __Pyx_InternStrings(__Pyx_InternTabEntry *t); /*proto*/

static int __Pyx_InitStrings(__Pyx_StringTabEntry *t); /*proto*/

static void __Pyx_AddTraceback(char *funcname); /*proto*/

/* Declarations from pypm */

struct __pyx_obj_4pypm_Output {
  PyObject_HEAD
  int i;
  PmStream *midi;
  int debug;
};

struct __pyx_obj_4pypm_Input {
  PyObject_HEAD
  PmStream *midi;
  int debug;
  int i;
};



static PyTypeObject *__pyx_ptype_4pypm_Output = 0;
static PyTypeObject *__pyx_ptype_4pypm_Input = 0;
static PyObject *__pyx_k3;
static PyObject *__pyx_k4;


/* Implementation of pypm */

static char __pyx_k1[] = "0.03";

static PyObject *__pyx_n___version__;
static PyObject *__pyx_n_array;
static PyObject *__pyx_n_FILT_ACTIVE;
static PyObject *__pyx_n_FILT_SYSEX;
static PyObject *__pyx_n_FILT_CLOCK;
static PyObject *__pyx_n_FILT_PLAY;
static PyObject *__pyx_n_FILT_F9;
static PyObject *__pyx_n_FILT_TICK;
static PyObject *__pyx_n_FILT_FD;
static PyObject *__pyx_n_FILT_UNDEFINED;
static PyObject *__pyx_n_FILT_RESET;
static PyObject *__pyx_n_FILT_REALTIME;
static PyObject *__pyx_n_FILT_NOTE;
static PyObject *__pyx_n_FILT_CHANNEL_AFTERTOUCH;
static PyObject *__pyx_n_FILT_POLY_AFTERTOUCH;
static PyObject *__pyx_n_FILT_AFTERTOUCH;
static PyObject *__pyx_n_FILT_PROGRAM;
static PyObject *__pyx_n_FILT_CONTROL;
static PyObject *__pyx_n_FILT_PITCHBEND;
static PyObject *__pyx_n_FILT_MTC;
static PyObject *__pyx_n_FILT_SONG_POSITION;
static PyObject *__pyx_n_FILT_SONG_SELECT;
static PyObject *__pyx_n_FILT_TUNE;
static PyObject *__pyx_n_FALSE;
static PyObject *__pyx_n_TRUE;

static PyObject *__pyx_k1p;

static PyObject *__pyx_f_4pypm_Initialize(PyObject *__pyx_self, PyObject *__pyx_args, PyObject *__pyx_kwds); /*proto*/
static char __pyx_doc_4pypm_Initialize[] = "\nInitialize: call this first\n    ";
static PyObject *__pyx_f_4pypm_Initialize(PyObject *__pyx_self, PyObject *__pyx_args, PyObject *__pyx_kwds) {
  PyObject *__pyx_r;
  static char *__pyx_argnames[] = {0};
  if (!PyArg_ParseTupleAndKeywords(__pyx_args, __pyx_kwds, "", __pyx_argnames)) return 0;

  /* "/home/jamie/programming/epimorph/sources/pypm/pypm.pyx":127 */
  Pm_Initialize();

  /* "/home/jamie/programming/epimorph/sources/pypm/pypm.pyx":128 */
  Pt_Start(1,NULL,NULL);

  __pyx_r = Py_None; Py_INCREF(Py_None);
  return __pyx_r;
}

static PyObject *__pyx_f_4pypm_Terminate(PyObject *__pyx_self, PyObject *__pyx_args, PyObject *__pyx_kwds); /*proto*/
static char __pyx_doc_4pypm_Terminate[] = "\nTerminate: call this to clean up Midi streams when done.\nIf you do not call this on Windows machines when you are\ndone with MIDI, your system may crash.\n    ";
static PyObject *__pyx_f_4pypm_Terminate(PyObject *__pyx_self, PyObject *__pyx_args, PyObject *__pyx_kwds) {
  PyObject *__pyx_r;
  static char *__pyx_argnames[] = {0};
  if (!PyArg_ParseTupleAndKeywords(__pyx_args, __pyx_kwds, "", __pyx_argnames)) return 0;
  Pm_Terminate();

  __pyx_r = Py_None; Py_INCREF(Py_None);
  return __pyx_r;
}

static PyObject *__pyx_f_4pypm_GetDefaultInputDeviceID(PyObject *__pyx_self, PyObject *__pyx_args, PyObject *__pyx_kwds); /*proto*/
static PyObject *__pyx_f_4pypm_GetDefaultInputDeviceID(PyObject *__pyx_self, PyObject *__pyx_args, PyObject *__pyx_kwds) {
  PyObject *__pyx_r;
  PyObject *__pyx_1 = 0;
  static char *__pyx_argnames[] = {0};
  if (!PyArg_ParseTupleAndKeywords(__pyx_args, __pyx_kwds, "", __pyx_argnames)) return 0;
  __pyx_1 = PyInt_FromLong(Pm_GetDefaultInputDeviceID()); if (!__pyx_1) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 139; goto __pyx_L1;}
  __pyx_r = __pyx_1;
  __pyx_1 = 0;
  goto __pyx_L0;

  __pyx_r = Py_None; Py_INCREF(Py_None);
  goto __pyx_L0;
  __pyx_L1:;
  Py_XDECREF(__pyx_1);
  __Pyx_AddTraceback("pypm.GetDefaultInputDeviceID");
  __pyx_r = 0;
  __pyx_L0:;
  return __pyx_r;
}

static PyObject *__pyx_f_4pypm_GetDefaultOutputDeviceID(PyObject *__pyx_self, PyObject *__pyx_args, PyObject *__pyx_kwds); /*proto*/
static PyObject *__pyx_f_4pypm_GetDefaultOutputDeviceID(PyObject *__pyx_self, PyObject *__pyx_args, PyObject *__pyx_kwds) {
  PyObject *__pyx_r;
  PyObject *__pyx_1 = 0;
  static char *__pyx_argnames[] = {0};
  if (!PyArg_ParseTupleAndKeywords(__pyx_args, __pyx_kwds, "", __pyx_argnames)) return 0;
  __pyx_1 = PyInt_FromLong(Pm_GetDefaultOutputDeviceID()); if (!__pyx_1) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 142; goto __pyx_L1;}
  __pyx_r = __pyx_1;
  __pyx_1 = 0;
  goto __pyx_L0;

  __pyx_r = Py_None; Py_INCREF(Py_None);
  goto __pyx_L0;
  __pyx_L1:;
  Py_XDECREF(__pyx_1);
  __Pyx_AddTraceback("pypm.GetDefaultOutputDeviceID");
  __pyx_r = 0;
  __pyx_L0:;
  return __pyx_r;
}

static PyObject *__pyx_f_4pypm_CountDevices(PyObject *__pyx_self, PyObject *__pyx_args, PyObject *__pyx_kwds); /*proto*/
static PyObject *__pyx_f_4pypm_CountDevices(PyObject *__pyx_self, PyObject *__pyx_args, PyObject *__pyx_kwds) {
  PyObject *__pyx_r;
  PyObject *__pyx_1 = 0;
  static char *__pyx_argnames[] = {0};
  if (!PyArg_ParseTupleAndKeywords(__pyx_args, __pyx_kwds, "", __pyx_argnames)) return 0;
  __pyx_1 = PyInt_FromLong(Pm_CountDevices()); if (!__pyx_1) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 145; goto __pyx_L1;}
  __pyx_r = __pyx_1;
  __pyx_1 = 0;
  goto __pyx_L0;

  __pyx_r = Py_None; Py_INCREF(Py_None);
  goto __pyx_L0;
  __pyx_L1:;
  Py_XDECREF(__pyx_1);
  __Pyx_AddTraceback("pypm.CountDevices");
  __pyx_r = 0;
  __pyx_L0:;
  return __pyx_r;
}

static PyObject *__pyx_f_4pypm_GetDeviceInfo(PyObject *__pyx_self, PyObject *__pyx_args, PyObject *__pyx_kwds); /*proto*/
static char __pyx_doc_4pypm_GetDeviceInfo[] = "\nGetDeviceInfo(<device number>): returns 5 parameters\n  - underlying MIDI API\n  - device name\n  - TRUE iff input is available\n  - TRUE iff output is available\n  - TRUE iff device stream is already open\n    ";
static PyObject *__pyx_f_4pypm_GetDeviceInfo(PyObject *__pyx_self, PyObject *__pyx_args, PyObject *__pyx_kwds) {
  PyObject *__pyx_v_i = 0;
  PmDeviceInfo *__pyx_v_info;
  PyObject *__pyx_r;
  PmDeviceID __pyx_1;
  int __pyx_2;
  PyObject *__pyx_3 = 0;
  PyObject *__pyx_4 = 0;
  PyObject *__pyx_5 = 0;
  PyObject *__pyx_6 = 0;
  PyObject *__pyx_7 = 0;
  PyObject *__pyx_8 = 0;
  static char *__pyx_argnames[] = {"i",0};
  if (!PyArg_ParseTupleAndKeywords(__pyx_args, __pyx_kwds, "O", __pyx_argnames, &__pyx_v_i)) return 0;
  Py_INCREF(__pyx_v_i);

  /* "/home/jamie/programming/epimorph/sources/pypm/pypm.pyx":157 */
  __pyx_1 = PyInt_AsLong(__pyx_v_i); if (PyErr_Occurred()) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 157; goto __pyx_L1;}
  __pyx_v_info = Pm_GetDeviceInfo(__pyx_1);

  /* "/home/jamie/programming/epimorph/sources/pypm/pypm.pyx":158 */
  __pyx_2 = (__pyx_v_info != NULL);
  if (__pyx_2) {
    __pyx_3 = PyString_FromString(__pyx_v_info->interf); if (!__pyx_3) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 158; goto __pyx_L1;}
    __pyx_4 = PyString_FromString(__pyx_v_info->name); if (!__pyx_4) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 158; goto __pyx_L1;}
    __pyx_5 = PyInt_FromLong(__pyx_v_info->input); if (!__pyx_5) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 158; goto __pyx_L1;}
    __pyx_6 = PyInt_FromLong(__pyx_v_info->output); if (!__pyx_6) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 158; goto __pyx_L1;}
    __pyx_7 = PyInt_FromLong(__pyx_v_info->opened); if (!__pyx_7) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 158; goto __pyx_L1;}
    __pyx_8 = PyTuple_New(5); if (!__pyx_8) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 158; goto __pyx_L1;}
    PyTuple_SET_ITEM(__pyx_8, 0, __pyx_3);
    PyTuple_SET_ITEM(__pyx_8, 1, __pyx_4);
    PyTuple_SET_ITEM(__pyx_8, 2, __pyx_5);
    PyTuple_SET_ITEM(__pyx_8, 3, __pyx_6);
    PyTuple_SET_ITEM(__pyx_8, 4, __pyx_7);
    __pyx_3 = 0;
    __pyx_4 = 0;
    __pyx_5 = 0;
    __pyx_6 = 0;
    __pyx_7 = 0;
    __pyx_r = __pyx_8;
    __pyx_8 = 0;
    goto __pyx_L0;
    goto __pyx_L2;
  }
  /*else*/ {
    __pyx_r = Py_None; Py_INCREF(Py_None);
    goto __pyx_L0;
  }
  __pyx_L2:;

  __pyx_r = Py_None; Py_INCREF(Py_None);
  goto __pyx_L0;
  __pyx_L1:;
  Py_XDECREF(__pyx_3);
  Py_XDECREF(__pyx_4);
  Py_XDECREF(__pyx_5);
  Py_XDECREF(__pyx_6);
  Py_XDECREF(__pyx_7);
  Py_XDECREF(__pyx_8);
  __Pyx_AddTraceback("pypm.GetDeviceInfo");
  __pyx_r = 0;
  __pyx_L0:;
  Py_DECREF(__pyx_v_i);
  return __pyx_r;
}

static PyObject *__pyx_f_4pypm_Time(PyObject *__pyx_self, PyObject *__pyx_args, PyObject *__pyx_kwds); /*proto*/
static char __pyx_doc_4pypm_Time[] = "\nTime() returns the current time in ms\nof the PortMidi timer\n    ";
static PyObject *__pyx_f_4pypm_Time(PyObject *__pyx_self, PyObject *__pyx_args, PyObject *__pyx_kwds) {
  PyObject *__pyx_r;
  PyObject *__pyx_1 = 0;
  static char *__pyx_argnames[] = {0};
  if (!PyArg_ParseTupleAndKeywords(__pyx_args, __pyx_kwds, "", __pyx_argnames)) return 0;
  __pyx_1 = PyInt_FromLong(Pt_Time()); if (!__pyx_1) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 166; goto __pyx_L1;}
  __pyx_r = __pyx_1;
  __pyx_1 = 0;
  goto __pyx_L0;

  __pyx_r = Py_None; Py_INCREF(Py_None);
  goto __pyx_L0;
  __pyx_L1:;
  Py_XDECREF(__pyx_1);
  __Pyx_AddTraceback("pypm.Time");
  __pyx_r = 0;
  __pyx_L0:;
  return __pyx_r;
}

static PyObject *__pyx_f_4pypm_GetErrorText(PyObject *__pyx_self, PyObject *__pyx_args, PyObject *__pyx_kwds); /*proto*/
static char __pyx_doc_4pypm_GetErrorText[] = "\nGetErrorText(<err num>) returns human-readable error\nmessages translated from error numbers\n    ";
static PyObject *__pyx_f_4pypm_GetErrorText(PyObject *__pyx_self, PyObject *__pyx_args, PyObject *__pyx_kwds) {
  PyObject *__pyx_v_err = 0;
  PyObject *__pyx_r;
  PmError __pyx_1;
  PyObject *__pyx_2 = 0;
  static char *__pyx_argnames[] = {"err",0};
  if (!PyArg_ParseTupleAndKeywords(__pyx_args, __pyx_kwds, "O", __pyx_argnames, &__pyx_v_err)) return 0;
  Py_INCREF(__pyx_v_err);
  __pyx_1 = ((PmError)PyInt_AsLong(__pyx_v_err)); if (PyErr_Occurred()) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 173; goto __pyx_L1;}
  __pyx_2 = PyString_FromString(Pm_GetErrorText(__pyx_1)); if (!__pyx_2) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 173; goto __pyx_L1;}
  __pyx_r = __pyx_2;
  __pyx_2 = 0;
  goto __pyx_L0;

  __pyx_r = Py_None; Py_INCREF(Py_None);
  goto __pyx_L0;
  __pyx_L1:;
  Py_XDECREF(__pyx_2);
  __Pyx_AddTraceback("pypm.GetErrorText");
  __pyx_r = 0;
  __pyx_L0:;
  Py_DECREF(__pyx_v_err);
  return __pyx_r;
}

static PyObject *__pyx_f_4pypm_Channel(PyObject *__pyx_self, PyObject *__pyx_args, PyObject *__pyx_kwds); /*proto*/
static char __pyx_doc_4pypm_Channel[] = "\nChannel(<chan>) is used with ChannelMask on input MIDI streams.\nExample: to receive input on channels 1 and 10 on a MIDI\n         stream called MidiIn:\nMidiIn.SetChannelMask(pypm.Channel(1) | pypm.Channel(10))\n\nnote: PyPortMidi Channel function has been altered from\n      the original PortMidi c call to correct for what\n      seems to be a bug --- i.e. channel filters were\n      all numbered from 0 to 15 instead of 1 to 16.\n    ";
static PyObject *__pyx_f_4pypm_Channel(PyObject *__pyx_self, PyObject *__pyx_args, PyObject *__pyx_kwds) {
  PyObject *__pyx_v_chan = 0;
  PyObject *__pyx_r;
  PyObject *__pyx_1 = 0;
  PyObject *__pyx_2 = 0;
  int __pyx_3;
  static char *__pyx_argnames[] = {"chan",0};
  if (!PyArg_ParseTupleAndKeywords(__pyx_args, __pyx_kwds, "O", __pyx_argnames, &__pyx_v_chan)) return 0;
  Py_INCREF(__pyx_v_chan);
  __pyx_1 = PyInt_FromLong(1); if (!__pyx_1) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 187; goto __pyx_L1;}
  __pyx_2 = PyNumber_Subtract(__pyx_v_chan, __pyx_1); if (!__pyx_2) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 187; goto __pyx_L1;}
  Py_DECREF(__pyx_1); __pyx_1 = 0;
  __pyx_3 = PyInt_AsLong(__pyx_2); if (PyErr_Occurred()) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 187; goto __pyx_L1;}
  Py_DECREF(__pyx_2); __pyx_2 = 0;
  __pyx_1 = PyInt_FromLong(Pm_Channel(__pyx_3)); if (!__pyx_1) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 187; goto __pyx_L1;}
  __pyx_r = __pyx_1;
  __pyx_1 = 0;
  goto __pyx_L0;

  __pyx_r = Py_None; Py_INCREF(Py_None);
  goto __pyx_L0;
  __pyx_L1:;
  Py_XDECREF(__pyx_1);
  Py_XDECREF(__pyx_2);
  __Pyx_AddTraceback("pypm.Channel");
  __pyx_r = 0;
  __pyx_L0:;
  Py_DECREF(__pyx_v_chan);
  return __pyx_r;
}

static PyObject *__pyx_k5p;

static char __pyx_k5[] = "Opening Midi Output";

static int __pyx_f_4pypm_6Output___init__(PyObject *__pyx_v_self, PyObject *__pyx_args, PyObject *__pyx_kwds); /*proto*/
static int __pyx_f_4pypm_6Output___init__(PyObject *__pyx_v_self, PyObject *__pyx_args, PyObject *__pyx_kwds) {
  PyObject *__pyx_v_OutputDevice = 0;
  PyObject *__pyx_v_latency = 0;
  PtTimestamp (*__pyx_v_PmPtr)(void);
  PmError __pyx_v_err;
  int __pyx_r;
  int __pyx_1;
  PyObject *__pyx_2 = 0;
  long __pyx_3;
  static char *__pyx_argnames[] = {"OutputDevice","latency",0};
  if (!PyArg_ParseTupleAndKeywords(__pyx_args, __pyx_kwds, "OO", __pyx_argnames, &__pyx_v_OutputDevice, &__pyx_v_latency)) return -1;
  Py_INCREF(__pyx_v_self);
  Py_INCREF(__pyx_v_OutputDevice);
  Py_INCREF(__pyx_v_latency);

  /* "/home/jamie/programming/epimorph/sources/pypm/pypm.pyx":205 */
  __pyx_1 = PyInt_AsLong(__pyx_v_OutputDevice); if (PyErr_Occurred()) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 205; goto __pyx_L1;}
  ((struct __pyx_obj_4pypm_Output *)__pyx_v_self)->i = __pyx_1;

  /* "/home/jamie/programming/epimorph/sources/pypm/pypm.pyx":206 */
  ((struct __pyx_obj_4pypm_Output *)__pyx_v_self)->debug = 0;

  /* "/home/jamie/programming/epimorph/sources/pypm/pypm.pyx":208 */
  __pyx_2 = PyInt_FromLong(0); if (!__pyx_2) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 208; goto __pyx_L1;}
  if (PyObject_Cmp(__pyx_v_latency, __pyx_2, &__pyx_1) < 0) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 208; goto __pyx_L1;}
  __pyx_1 = __pyx_1 == 0;
  Py_DECREF(__pyx_2); __pyx_2 = 0;
  if (__pyx_1) {
    __pyx_v_PmPtr = NULL;
    goto __pyx_L2;
  }
  /*else*/ {
    __pyx_v_PmPtr = (&Pt_Time);
  }
  __pyx_L2:;

  /* "/home/jamie/programming/epimorph/sources/pypm/pypm.pyx":212 */
  __pyx_1 = ((struct __pyx_obj_4pypm_Output *)__pyx_v_self)->debug;
  if (__pyx_1) {
    if (__Pyx_PrintItem(__pyx_k5p) < 0) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 212; goto __pyx_L1;}
    if (__Pyx_PrintNewline() < 0) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 212; goto __pyx_L1;}
    goto __pyx_L3;
  }
  __pyx_L3:;

  /* "/home/jamie/programming/epimorph/sources/pypm/pypm.pyx":213 */
  __pyx_3 = PyInt_AsLong(__pyx_v_latency); if (PyErr_Occurred()) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 213; goto __pyx_L1;}
  __pyx_v_err = Pm_OpenOutput((&((struct __pyx_obj_4pypm_Output *)__pyx_v_self)->midi),((struct __pyx_obj_4pypm_Output *)__pyx_v_self)->i,NULL,0,__pyx_v_PmPtr,NULL,__pyx_3);

  /* "/home/jamie/programming/epimorph/sources/pypm/pypm.pyx":214 */
  __pyx_1 = (__pyx_v_err < 0);
  if (__pyx_1) {
    __pyx_2 = PyString_FromString(Pm_GetErrorText(__pyx_v_err)); if (!__pyx_2) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 214; goto __pyx_L1;}
    __Pyx_Raise(PyExc_Exception, __pyx_2, 0);
    Py_DECREF(__pyx_2); __pyx_2 = 0;
    {__pyx_filename = __pyx_f[0]; __pyx_lineno = 214; goto __pyx_L1;}
    goto __pyx_L4;
  }
  __pyx_L4:;

  __pyx_r = 0;
  goto __pyx_L0;
  __pyx_L1:;
  Py_XDECREF(__pyx_2);
  __Pyx_AddTraceback("pypm.Output.__init__");
  __pyx_r = -1;
  __pyx_L0:;
  Py_DECREF(__pyx_v_self);
  Py_DECREF(__pyx_v_OutputDevice);
  Py_DECREF(__pyx_v_latency);
  return __pyx_r;
}

static PyObject *__pyx_k6p;

static char __pyx_k6[] = "Closing MIDI output stream and destroying instance";

static void __pyx_f_4pypm_6Output___dealloc__(PyObject *__pyx_v_self); /*proto*/
static void __pyx_f_4pypm_6Output___dealloc__(PyObject *__pyx_v_self) {
  PyObject *__pyx_v_err;
  int __pyx_1;
  PyObject *__pyx_2 = 0;
  PmError __pyx_3;
  Py_INCREF(__pyx_v_self);
  __pyx_v_err = Py_None; Py_INCREF(Py_None);

  /* "/home/jamie/programming/epimorph/sources/pypm/pypm.pyx":217 */
  __pyx_1 = ((struct __pyx_obj_4pypm_Output *)__pyx_v_self)->debug;
  if (__pyx_1) {
    if (__Pyx_PrintItem(__pyx_k6p) < 0) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 217; goto __pyx_L1;}
    if (__Pyx_PrintNewline() < 0) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 217; goto __pyx_L1;}
    goto __pyx_L2;
  }
  __pyx_L2:;

  /* "/home/jamie/programming/epimorph/sources/pypm/pypm.pyx":218 */
  __pyx_2 = PyInt_FromLong(Pm_Abort(((struct __pyx_obj_4pypm_Output *)__pyx_v_self)->midi)); if (!__pyx_2) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 218; goto __pyx_L1;}
  Py_DECREF(__pyx_v_err);
  __pyx_v_err = __pyx_2;
  __pyx_2 = 0;

  /* "/home/jamie/programming/epimorph/sources/pypm/pypm.pyx":219 */
  __pyx_2 = PyInt_FromLong(0); if (!__pyx_2) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 219; goto __pyx_L1;}
  if (PyObject_Cmp(__pyx_v_err, __pyx_2, &__pyx_1) < 0) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 219; goto __pyx_L1;}
  __pyx_1 = __pyx_1 < 0;
  Py_DECREF(__pyx_2); __pyx_2 = 0;
  if (__pyx_1) {
    __pyx_3 = ((PmError)PyInt_AsLong(__pyx_v_err)); if (PyErr_Occurred()) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 219; goto __pyx_L1;}
    __pyx_2 = PyString_FromString(Pm_GetErrorText(__pyx_3)); if (!__pyx_2) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 219; goto __pyx_L1;}
    __Pyx_Raise(PyExc_Exception, __pyx_2, 0);
    Py_DECREF(__pyx_2); __pyx_2 = 0;
    {__pyx_filename = __pyx_f[0]; __pyx_lineno = 219; goto __pyx_L1;}
    goto __pyx_L3;
  }
  __pyx_L3:;

  /* "/home/jamie/programming/epimorph/sources/pypm/pypm.pyx":220 */
  __pyx_2 = PyInt_FromLong(Pm_Close(((struct __pyx_obj_4pypm_Output *)__pyx_v_self)->midi)); if (!__pyx_2) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 220; goto __pyx_L1;}
  Py_DECREF(__pyx_v_err);
  __pyx_v_err = __pyx_2;
  __pyx_2 = 0;

  /* "/home/jamie/programming/epimorph/sources/pypm/pypm.pyx":221 */
  __pyx_2 = PyInt_FromLong(0); if (!__pyx_2) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 221; goto __pyx_L1;}
  if (PyObject_Cmp(__pyx_v_err, __pyx_2, &__pyx_1) < 0) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 221; goto __pyx_L1;}
  __pyx_1 = __pyx_1 < 0;
  Py_DECREF(__pyx_2); __pyx_2 = 0;
  if (__pyx_1) {
    __pyx_3 = ((PmError)PyInt_AsLong(__pyx_v_err)); if (PyErr_Occurred()) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 221; goto __pyx_L1;}
    __pyx_2 = PyString_FromString(Pm_GetErrorText(__pyx_3)); if (!__pyx_2) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 221; goto __pyx_L1;}
    __Pyx_Raise(PyExc_Exception, __pyx_2, 0);
    Py_DECREF(__pyx_2); __pyx_2 = 0;
    {__pyx_filename = __pyx_f[0]; __pyx_lineno = 221; goto __pyx_L1;}
    goto __pyx_L4;
  }
  __pyx_L4:;

  goto __pyx_L0;
  __pyx_L1:;
  Py_XDECREF(__pyx_2);
  __Pyx_AddTraceback("pypm.Output.__dealloc__");
  __pyx_L0:;
  Py_DECREF(__pyx_v_err);
  Py_DECREF(__pyx_v_self);
}

static PyObject *__pyx_n_range;

static PyObject *__pyx_k7p;
static PyObject *__pyx_k8p;
static PyObject *__pyx_k9p;
static PyObject *__pyx_k10p;
static PyObject *__pyx_k11p;

static char __pyx_k7[] = "maximum list length is 1024";
static char __pyx_k8[] = " arguments in event list";
static char __pyx_k9[] = " : ";
static char __pyx_k10[] = " : ";
static char __pyx_k11[] = "writing to midi buffer";

static PyObject *__pyx_f_4pypm_6Output_Write(PyObject *__pyx_v_self, PyObject *__pyx_args, PyObject *__pyx_kwds); /*proto*/
static char __pyx_doc_4pypm_6Output_Write[] = "\nWrite(data)\n    output a series of MIDI information in the form of a list:\n         Write([[[status <,data1><,data2><,data3>],timestamp],\n                [[status <,data1><,data2><,data3>],timestamp],...])\n    <data> fields are optional\n    example: choose program change 1 at time 20000 and\n    send note 65 with velocity 100 500 ms later.\n         Write([[[0xc0,0,0],20000],[[0x90,60,100],20500]])\n    notes:\n      1. timestamps will be ignored if latency = 0.\n      2. To get a note to play immediately, send MIDI info with\n         timestamp read from function Time.\n      3. understanding optional data fields:\n           Write([[[0xc0,0,0],20000]]) is equivalent to\n           Write([[[0xc0],20000]])\n        ";
static PyObject *__pyx_f_4pypm_6Output_Write(PyObject *__pyx_v_self, PyObject *__pyx_args, PyObject *__pyx_kwds) {
  PyObject *__pyx_v_data = 0;
  PmEvent __pyx_v_buffer[1024];
  PmError __pyx_v_err;
  int __pyx_v_i;
  PyObject *__pyx_v_loop1;
  PyObject *__pyx_r;
  Py_ssize_t __pyx_1;
  int __pyx_2;
  PyObject *__pyx_3 = 0;
  PyObject *__pyx_4 = 0;
  PyObject *__pyx_5 = 0;
  Py_ssize_t __pyx_6;
  PyObject *__pyx_7 = 0;
  PyObject *__pyx_8 = 0;
  PyObject *__pyx_9 = 0;
  PmMessage __pyx_10;
  PmTimestamp __pyx_11;
  static char *__pyx_argnames[] = {"data",0};
  if (!PyArg_ParseTupleAndKeywords(__pyx_args, __pyx_kwds, "O", __pyx_argnames, &__pyx_v_data)) return 0;
  Py_INCREF(__pyx_v_self);
  Py_INCREF(__pyx_v_data);
  __pyx_v_loop1 = Py_None; Py_INCREF(Py_None);

  /* "/home/jamie/programming/epimorph/sources/pypm/pypm.pyx":245 */
  __pyx_1 = PyObject_Length(__pyx_v_data); if (__pyx_1 == -1) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 245; goto __pyx_L1;}
  __pyx_2 = (__pyx_1 > 1024);
  if (__pyx_2) {
    __Pyx_Raise(PyExc_IndexError, __pyx_k7p, 0);
    {__pyx_filename = __pyx_f[0]; __pyx_lineno = 245; goto __pyx_L1;}
    goto __pyx_L2;
  }
  /*else*/ {
    __pyx_3 = __Pyx_GetName(__pyx_b, __pyx_n_range); if (!__pyx_3) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 247; goto __pyx_L1;}
    __pyx_1 = PyObject_Length(__pyx_v_data); if (__pyx_1 == -1) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 247; goto __pyx_L1;}
    __pyx_4 = PyInt_FromSsize_t(__pyx_1); if (!__pyx_4) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 247; goto __pyx_L1;}
    __pyx_5 = PyTuple_New(1); if (!__pyx_5) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 247; goto __pyx_L1;}
    PyTuple_SET_ITEM(__pyx_5, 0, __pyx_4);
    __pyx_4 = 0;
    __pyx_4 = PyObject_CallObject(__pyx_3, __pyx_5); if (!__pyx_4) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 247; goto __pyx_L1;}
    Py_DECREF(__pyx_3); __pyx_3 = 0;
    Py_DECREF(__pyx_5); __pyx_5 = 0;
    __pyx_3 = PyObject_GetIter(__pyx_4); if (!__pyx_3) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 247; goto __pyx_L1;}
    Py_DECREF(__pyx_4); __pyx_4 = 0;
    for (;;) {
      __pyx_5 = PyIter_Next(__pyx_3);
      if (!__pyx_5) {
        if (PyErr_Occurred()) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 247; goto __pyx_L1;}
        break;
      }
      Py_DECREF(__pyx_v_loop1);
      __pyx_v_loop1 = __pyx_5;
      __pyx_5 = 0;

      /* "/home/jamie/programming/epimorph/sources/pypm/pypm.pyx":248 */
      __pyx_4 = PyObject_GetItem(__pyx_v_data, __pyx_v_loop1); if (!__pyx_4) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 248; goto __pyx_L1;}
      __pyx_5 = __Pyx_GetItemInt(__pyx_4, 0); if (!__pyx_5) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 248; goto __pyx_L1;}
      Py_DECREF(__pyx_4); __pyx_4 = 0;
      __pyx_1 = PyObject_Length(__pyx_5); if (__pyx_1 == -1) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 248; goto __pyx_L1;}
      Py_DECREF(__pyx_5); __pyx_5 = 0;
      __pyx_4 = PyObject_GetItem(__pyx_v_data, __pyx_v_loop1); if (!__pyx_4) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 249; goto __pyx_L1;}
      __pyx_5 = __Pyx_GetItemInt(__pyx_4, 0); if (!__pyx_5) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 249; goto __pyx_L1;}
      Py_DECREF(__pyx_4); __pyx_4 = 0;
      __pyx_6 = PyObject_Length(__pyx_5); if (__pyx_6 == -1) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 249; goto __pyx_L1;}
      Py_DECREF(__pyx_5); __pyx_5 = 0;
      __pyx_2 = ((__pyx_1 > 4) | (__pyx_6 < 1));
      if (__pyx_2) {
        __pyx_4 = PyObject_GetItem(__pyx_v_data, __pyx_v_loop1); if (!__pyx_4) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 250; goto __pyx_L1;}
        __pyx_5 = __Pyx_GetItemInt(__pyx_4, 0); if (!__pyx_5) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 250; goto __pyx_L1;}
        Py_DECREF(__pyx_4); __pyx_4 = 0;
        __pyx_1 = PyObject_Length(__pyx_5); if (__pyx_1 == -1) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 250; goto __pyx_L1;}
        Py_DECREF(__pyx_5); __pyx_5 = 0;
        __pyx_4 = PyInt_FromSsize_t(__pyx_1); if (!__pyx_4) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 250; goto __pyx_L1;}
        __pyx_5 = PyTuple_New(1); if (!__pyx_5) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 250; goto __pyx_L1;}
        PyTuple_SET_ITEM(__pyx_5, 0, __pyx_4);
        __pyx_4 = 0;
        __pyx_4 = PyObject_CallObject(((PyObject *)(&PyString_Type)), __pyx_5); if (!__pyx_4) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 250; goto __pyx_L1;}
        Py_DECREF(__pyx_5); __pyx_5 = 0;
        __pyx_5 = PyNumber_Add(__pyx_4, __pyx_k8p); if (!__pyx_5) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 250; goto __pyx_L1;}
        Py_DECREF(__pyx_4); __pyx_4 = 0;
        __Pyx_Raise(PyExc_IndexError, __pyx_5, 0);
        Py_DECREF(__pyx_5); __pyx_5 = 0;
        {__pyx_filename = __pyx_f[0]; __pyx_lineno = 250; goto __pyx_L1;}
        goto __pyx_L5;
      }
      __pyx_L5:;

      /* "/home/jamie/programming/epimorph/sources/pypm/pypm.pyx":251 */
      __pyx_6 = PyInt_AsSsize_t(__pyx_v_loop1); if (PyErr_Occurred()) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 251; goto __pyx_L1;}
      (__pyx_v_buffer[__pyx_6]).message = 0;

      /* "/home/jamie/programming/epimorph/sources/pypm/pypm.pyx":252 */
      __pyx_4 = __Pyx_GetName(__pyx_b, __pyx_n_range); if (!__pyx_4) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 252; goto __pyx_L1;}
      __pyx_5 = PyObject_GetItem(__pyx_v_data, __pyx_v_loop1); if (!__pyx_5) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 252; goto __pyx_L1;}
      __pyx_7 = __Pyx_GetItemInt(__pyx_5, 0); if (!__pyx_7) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 252; goto __pyx_L1;}
      Py_DECREF(__pyx_5); __pyx_5 = 0;
      __pyx_1 = PyObject_Length(__pyx_7); if (__pyx_1 == -1) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 252; goto __pyx_L1;}
      Py_DECREF(__pyx_7); __pyx_7 = 0;
      __pyx_5 = PyInt_FromSsize_t(__pyx_1); if (!__pyx_5) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 252; goto __pyx_L1;}
      __pyx_7 = PyTuple_New(1); if (!__pyx_7) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 252; goto __pyx_L1;}
      PyTuple_SET_ITEM(__pyx_7, 0, __pyx_5);
      __pyx_5 = 0;
      __pyx_5 = PyObject_CallObject(__pyx_4, __pyx_7); if (!__pyx_5) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 252; goto __pyx_L1;}
      Py_DECREF(__pyx_4); __pyx_4 = 0;
      Py_DECREF(__pyx_7); __pyx_7 = 0;
      __pyx_4 = PyObject_GetIter(__pyx_5); if (!__pyx_4) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 252; goto __pyx_L1;}
      Py_DECREF(__pyx_5); __pyx_5 = 0;
      for (;;) {
        __pyx_7 = PyIter_Next(__pyx_4);
        if (!__pyx_7) {
          if (PyErr_Occurred()) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 252; goto __pyx_L1;}
          break;
        }
        __pyx_2 = PyInt_AsLong(__pyx_7); if (PyErr_Occurred()) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 252; goto __pyx_L1;}
        Py_DECREF(__pyx_7); __pyx_7 = 0;
        __pyx_v_i = __pyx_2;
        __pyx_6 = PyInt_AsSsize_t(__pyx_v_loop1); if (PyErr_Occurred()) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 253; goto __pyx_L1;}
        __pyx_5 = PyInt_FromLong((__pyx_v_buffer[__pyx_6]).message); if (!__pyx_5) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 253; goto __pyx_L1;}
        __pyx_7 = PyObject_GetItem(__pyx_v_data, __pyx_v_loop1); if (!__pyx_7) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 253; goto __pyx_L1;}
        __pyx_8 = __Pyx_GetItemInt(__pyx_7, 0); if (!__pyx_8) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 253; goto __pyx_L1;}
        Py_DECREF(__pyx_7); __pyx_7 = 0;
        __pyx_7 = __Pyx_GetItemInt(__pyx_8, __pyx_v_i); if (!__pyx_7) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 253; goto __pyx_L1;}
        Py_DECREF(__pyx_8); __pyx_8 = 0;
        __pyx_8 = PyInt_FromLong(0xFF); if (!__pyx_8) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 253; goto __pyx_L1;}
        __pyx_9 = PyNumber_And(__pyx_7, __pyx_8); if (!__pyx_9) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 253; goto __pyx_L1;}
        Py_DECREF(__pyx_7); __pyx_7 = 0;
        Py_DECREF(__pyx_8); __pyx_8 = 0;
        __pyx_7 = PyInt_FromLong((8 * __pyx_v_i)); if (!__pyx_7) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 253; goto __pyx_L1;}
        __pyx_8 = PyNumber_Lshift(__pyx_9, __pyx_7); if (!__pyx_8) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 253; goto __pyx_L1;}
        Py_DECREF(__pyx_9); __pyx_9 = 0;
        Py_DECREF(__pyx_7); __pyx_7 = 0;
        __pyx_9 = PyNumber_Add(__pyx_5, __pyx_8); if (!__pyx_9) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 253; goto __pyx_L1;}
        Py_DECREF(__pyx_5); __pyx_5 = 0;
        Py_DECREF(__pyx_8); __pyx_8 = 0;
        __pyx_10 = PyInt_AsLong(__pyx_9); if (PyErr_Occurred()) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 253; goto __pyx_L1;}
        Py_DECREF(__pyx_9); __pyx_9 = 0;
        __pyx_1 = PyInt_AsSsize_t(__pyx_v_loop1); if (PyErr_Occurred()) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 253; goto __pyx_L1;}
        (__pyx_v_buffer[__pyx_1]).message = __pyx_10;
      }
      Py_DECREF(__pyx_4); __pyx_4 = 0;

      /* "/home/jamie/programming/epimorph/sources/pypm/pypm.pyx":254 */
      __pyx_7 = PyObject_GetItem(__pyx_v_data, __pyx_v_loop1); if (!__pyx_7) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 254; goto __pyx_L1;}
      __pyx_5 = __Pyx_GetItemInt(__pyx_7, 1); if (!__pyx_5) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 254; goto __pyx_L1;}
      Py_DECREF(__pyx_7); __pyx_7 = 0;
      __pyx_11 = PyInt_AsLong(__pyx_5); if (PyErr_Occurred()) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 254; goto __pyx_L1;}
      Py_DECREF(__pyx_5); __pyx_5 = 0;
      __pyx_6 = PyInt_AsSsize_t(__pyx_v_loop1); if (PyErr_Occurred()) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 254; goto __pyx_L1;}
      (__pyx_v_buffer[__pyx_6]).timestamp = __pyx_11;

      /* "/home/jamie/programming/epimorph/sources/pypm/pypm.pyx":255 */
      __pyx_2 = ((struct __pyx_obj_4pypm_Output *)__pyx_v_self)->debug;
      if (__pyx_2) {
        if (__Pyx_PrintItem(__pyx_v_loop1) < 0) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 255; goto __pyx_L1;}
        if (__Pyx_PrintItem(__pyx_k9p) < 0) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 255; goto __pyx_L1;}
        __pyx_1 = PyInt_AsSsize_t(__pyx_v_loop1); if (PyErr_Occurred()) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 255; goto __pyx_L1;}
        __pyx_8 = PyInt_FromLong((__pyx_v_buffer[__pyx_1]).message); if (!__pyx_8) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 255; goto __pyx_L1;}
        if (__Pyx_PrintItem(__pyx_8) < 0) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 255; goto __pyx_L1;}
        Py_DECREF(__pyx_8); __pyx_8 = 0;
        if (__Pyx_PrintItem(__pyx_k10p) < 0) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 255; goto __pyx_L1;}
        __pyx_6 = PyInt_AsSsize_t(__pyx_v_loop1); if (PyErr_Occurred()) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 255; goto __pyx_L1;}
        __pyx_9 = PyInt_FromLong((__pyx_v_buffer[__pyx_6]).timestamp); if (!__pyx_9) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 255; goto __pyx_L1;}
        if (__Pyx_PrintItem(__pyx_9) < 0) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 255; goto __pyx_L1;}
        Py_DECREF(__pyx_9); __pyx_9 = 0;
        if (__Pyx_PrintNewline() < 0) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 255; goto __pyx_L1;}
        goto __pyx_L8;
      }
      __pyx_L8:;
    }
    Py_DECREF(__pyx_3); __pyx_3 = 0;
  }
  __pyx_L2:;

  /* "/home/jamie/programming/epimorph/sources/pypm/pypm.pyx":256 */
  __pyx_2 = ((struct __pyx_obj_4pypm_Output *)__pyx_v_self)->debug;
  if (__pyx_2) {
    if (__Pyx_PrintItem(__pyx_k11p) < 0) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 256; goto __pyx_L1;}
    if (__Pyx_PrintNewline() < 0) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 256; goto __pyx_L1;}
    goto __pyx_L9;
  }
  __pyx_L9:;

  /* "/home/jamie/programming/epimorph/sources/pypm/pypm.pyx":257 */
  __pyx_1 = PyObject_Length(__pyx_v_data); if (__pyx_1 == -1) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 257; goto __pyx_L1;}
  __pyx_v_err = Pm_Write(((struct __pyx_obj_4pypm_Output *)__pyx_v_self)->midi,__pyx_v_buffer,__pyx_1);

  /* "/home/jamie/programming/epimorph/sources/pypm/pypm.pyx":258 */
  __pyx_2 = (__pyx_v_err < 0);
  if (__pyx_2) {
    __pyx_4 = PyString_FromString(Pm_GetErrorText(__pyx_v_err)); if (!__pyx_4) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 258; goto __pyx_L1;}
    __Pyx_Raise(PyExc_Exception, __pyx_4, 0);
    Py_DECREF(__pyx_4); __pyx_4 = 0;
    {__pyx_filename = __pyx_f[0]; __pyx_lineno = 258; goto __pyx_L1;}
    goto __pyx_L10;
  }
  __pyx_L10:;

  __pyx_r = Py_None; Py_INCREF(Py_None);
  goto __pyx_L0;
  __pyx_L1:;
  Py_XDECREF(__pyx_3);
  Py_XDECREF(__pyx_4);
  Py_XDECREF(__pyx_5);
  Py_XDECREF(__pyx_7);
  Py_XDECREF(__pyx_8);
  Py_XDECREF(__pyx_9);
  __Pyx_AddTraceback("pypm.Output.Write");
  __pyx_r = 0;
  __pyx_L0:;
  Py_DECREF(__pyx_v_loop1);
  Py_DECREF(__pyx_v_self);
  Py_DECREF(__pyx_v_data);
  return __pyx_r;
}

static PyObject *__pyx_k12p;

static char __pyx_k12[] = "Writing to MIDI buffer";

static PyObject *__pyx_f_4pypm_6Output_WriteShort(PyObject *__pyx_v_self, PyObject *__pyx_args, PyObject *__pyx_kwds); /*proto*/
static char __pyx_doc_4pypm_6Output_WriteShort[] = "\nWriteShort(status <, data1><, data2>)\n     output MIDI information of 3 bytes or less.\n     data fields are optional\n     status byte could be:\n          0xc0 = program change\n          0x90 = note on\n          etc.\n          data bytes are optional and assumed 0 if omitted\n     example: note 65 on with velocity 100\n          WriteShort(0x90,65,100)\n        ";
static PyObject *__pyx_f_4pypm_6Output_WriteShort(PyObject *__pyx_v_self, PyObject *__pyx_args, PyObject *__pyx_kwds) {
  PyObject *__pyx_v_status = 0;
  PyObject *__pyx_v_data1 = 0;
  PyObject *__pyx_v_data2 = 0;
  PmEvent __pyx_v_buffer[1];
  PmError __pyx_v_err;
  PyObject *__pyx_r;
  PyObject *__pyx_1 = 0;
  PyObject *__pyx_2 = 0;
  PyObject *__pyx_3 = 0;
  PyObject *__pyx_4 = 0;
  PmMessage __pyx_5;
  int __pyx_6;
  static char *__pyx_argnames[] = {"status","data1","data2",0};
  __pyx_v_data1 = __pyx_k3;
  __pyx_v_data2 = __pyx_k4;
  if (!PyArg_ParseTupleAndKeywords(__pyx_args, __pyx_kwds, "O|OO", __pyx_argnames, &__pyx_v_status, &__pyx_v_data1, &__pyx_v_data2)) return 0;
  Py_INCREF(__pyx_v_self);
  Py_INCREF(__pyx_v_status);
  Py_INCREF(__pyx_v_data1);
  Py_INCREF(__pyx_v_data2);

  /* "/home/jamie/programming/epimorph/sources/pypm/pypm.pyx":276 */
  (__pyx_v_buffer[0]).timestamp = Pt_Time();

  /* "/home/jamie/programming/epimorph/sources/pypm/pypm.pyx":277 */
  __pyx_1 = PyInt_FromLong(16); if (!__pyx_1) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 277; goto __pyx_L1;}
  __pyx_2 = PyNumber_Lshift(__pyx_v_data2, __pyx_1); if (!__pyx_2) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 277; goto __pyx_L1;}
  Py_DECREF(__pyx_1); __pyx_1 = 0;
  __pyx_1 = PyInt_FromLong(0xFF0000); if (!__pyx_1) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 277; goto __pyx_L1;}
  __pyx_3 = PyNumber_And(__pyx_2, __pyx_1); if (!__pyx_3) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 277; goto __pyx_L1;}
  Py_DECREF(__pyx_2); __pyx_2 = 0;
  Py_DECREF(__pyx_1); __pyx_1 = 0;
  __pyx_2 = PyInt_FromLong(8); if (!__pyx_2) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 277; goto __pyx_L1;}
  __pyx_1 = PyNumber_Lshift(__pyx_v_data1, __pyx_2); if (!__pyx_1) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 277; goto __pyx_L1;}
  Py_DECREF(__pyx_2); __pyx_2 = 0;
  __pyx_2 = PyInt_FromLong(0xFF00); if (!__pyx_2) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 277; goto __pyx_L1;}
  __pyx_4 = PyNumber_And(__pyx_1, __pyx_2); if (!__pyx_4) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 277; goto __pyx_L1;}
  Py_DECREF(__pyx_1); __pyx_1 = 0;
  Py_DECREF(__pyx_2); __pyx_2 = 0;
  __pyx_1 = PyNumber_Or(__pyx_3, __pyx_4); if (!__pyx_1) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 277; goto __pyx_L1;}
  Py_DECREF(__pyx_3); __pyx_3 = 0;
  Py_DECREF(__pyx_4); __pyx_4 = 0;
  __pyx_2 = PyInt_FromLong(0xFF); if (!__pyx_2) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 277; goto __pyx_L1;}
  __pyx_3 = PyNumber_And(__pyx_v_status, __pyx_2); if (!__pyx_3) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 277; goto __pyx_L1;}
  Py_DECREF(__pyx_2); __pyx_2 = 0;
  __pyx_4 = PyNumber_Or(__pyx_1, __pyx_3); if (!__pyx_4) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 277; goto __pyx_L1;}
  Py_DECREF(__pyx_1); __pyx_1 = 0;
  Py_DECREF(__pyx_3); __pyx_3 = 0;
  __pyx_5 = PyInt_AsLong(__pyx_4); if (PyErr_Occurred()) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 277; goto __pyx_L1;}
  Py_DECREF(__pyx_4); __pyx_4 = 0;
  (__pyx_v_buffer[0]).message = __pyx_5;

  /* "/home/jamie/programming/epimorph/sources/pypm/pypm.pyx":278 */
  __pyx_6 = ((struct __pyx_obj_4pypm_Output *)__pyx_v_self)->debug;
  if (__pyx_6) {
    if (__Pyx_PrintItem(__pyx_k12p) < 0) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 278; goto __pyx_L1;}
    if (__Pyx_PrintNewline() < 0) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 278; goto __pyx_L1;}
    goto __pyx_L2;
  }
  __pyx_L2:;

  /* "/home/jamie/programming/epimorph/sources/pypm/pypm.pyx":279 */
  __pyx_v_err = Pm_Write(((struct __pyx_obj_4pypm_Output *)__pyx_v_self)->midi,__pyx_v_buffer,1);

  /* "/home/jamie/programming/epimorph/sources/pypm/pypm.pyx":280 */
  __pyx_6 = (__pyx_v_err < 0);
  if (__pyx_6) {
    __pyx_2 = PyString_FromString(Pm_GetErrorText(__pyx_v_err)); if (!__pyx_2) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 280; goto __pyx_L1;}
    __Pyx_Raise(PyExc_Exception, __pyx_2, 0);
    Py_DECREF(__pyx_2); __pyx_2 = 0;
    {__pyx_filename = __pyx_f[0]; __pyx_lineno = 280; goto __pyx_L1;}
    goto __pyx_L3;
  }
  __pyx_L3:;

  __pyx_r = Py_None; Py_INCREF(Py_None);
  goto __pyx_L0;
  __pyx_L1:;
  Py_XDECREF(__pyx_1);
  Py_XDECREF(__pyx_2);
  Py_XDECREF(__pyx_3);
  Py_XDECREF(__pyx_4);
  __Pyx_AddTraceback("pypm.Output.WriteShort");
  __pyx_r = 0;
  __pyx_L0:;
  Py_DECREF(__pyx_v_self);
  Py_DECREF(__pyx_v_status);
  Py_DECREF(__pyx_v_data1);
  Py_DECREF(__pyx_v_data2);
  return __pyx_r;
}

static PyObject *__pyx_n_B;
static PyObject *__pyx_n_tostring;


static PyObject *__pyx_f_4pypm_6Output_WriteSysEx(PyObject *__pyx_v_self, PyObject *__pyx_args, PyObject *__pyx_kwds); /*proto*/
static char __pyx_doc_4pypm_6Output_WriteSysEx[] = "\n        WriteSysEx(<timestamp>,<msg>)\n        writes a timestamped system-exclusive midi message.\n        <msg> can be a *list* or a *string*\n        example:\n            (assuming y is an input MIDI stream)\n            y.WriteSysEx(0,\'\\xF0\\x7D\\x10\\x11\\x12\\x13\\xF7\')\n                              is equivalent to\n            y.WriteSysEx(pypm.Time,\n            [0xF0, 0x7D, 0x10, 0x11, 0x12, 0x13, 0xF7])\n        ";
static PyObject *__pyx_f_4pypm_6Output_WriteSysEx(PyObject *__pyx_v_self, PyObject *__pyx_args, PyObject *__pyx_kwds) {
  PyObject *__pyx_v_when = 0;
  PyObject *__pyx_v_msg = 0;
  PmError __pyx_v_err;
  char *__pyx_v_cmsg;
  PtTimestamp __pyx_v_CurTime;
  PyObject *__pyx_r;
  PyObject *__pyx_1 = 0;
  PyObject *__pyx_2 = 0;
  int __pyx_3;
  PyObject *__pyx_4 = 0;
  char *__pyx_5;
  PmTimestamp __pyx_6;
  static char *__pyx_argnames[] = {"when","msg",0};
  if (!PyArg_ParseTupleAndKeywords(__pyx_args, __pyx_kwds, "OO", __pyx_argnames, &__pyx_v_when, &__pyx_v_msg)) return 0;
  Py_INCREF(__pyx_v_self);
  Py_INCREF(__pyx_v_when);
  Py_INCREF(__pyx_v_msg);

  /* "/home/jamie/programming/epimorph/sources/pypm/pypm.pyx":298 */
  __pyx_1 = PyTuple_New(1); if (!__pyx_1) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 298; goto __pyx_L1;}
  Py_INCREF(__pyx_v_msg);
  PyTuple_SET_ITEM(__pyx_1, 0, __pyx_v_msg);
  __pyx_2 = PyObject_CallObject(((PyObject *)(&PyType_Type)), __pyx_1); if (!__pyx_2) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 298; goto __pyx_L1;}
  Py_DECREF(__pyx_1); __pyx_1 = 0;
  __pyx_3 = __pyx_2 == ((PyObject *)(&PyList_Type));
  Py_DECREF(__pyx_2); __pyx_2 = 0;
  if (__pyx_3) {
    __pyx_1 = __Pyx_GetName(__pyx_m, __pyx_n_array); if (!__pyx_1) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 299; goto __pyx_L1;}
    __pyx_2 = PyObject_GetAttr(__pyx_1, __pyx_n_array); if (!__pyx_2) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 299; goto __pyx_L1;}
    Py_DECREF(__pyx_1); __pyx_1 = 0;
    __pyx_1 = PyTuple_New(2); if (!__pyx_1) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 299; goto __pyx_L1;}
    Py_INCREF(__pyx_n_B);
    PyTuple_SET_ITEM(__pyx_1, 0, __pyx_n_B);
    Py_INCREF(__pyx_v_msg);
    PyTuple_SET_ITEM(__pyx_1, 1, __pyx_v_msg);
    __pyx_4 = PyObject_CallObject(__pyx_2, __pyx_1); if (!__pyx_4) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 299; goto __pyx_L1;}
    Py_DECREF(__pyx_2); __pyx_2 = 0;
    Py_DECREF(__pyx_1); __pyx_1 = 0;
    __pyx_2 = PyObject_GetAttr(__pyx_4, __pyx_n_tostring); if (!__pyx_2) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 299; goto __pyx_L1;}
    Py_DECREF(__pyx_4); __pyx_4 = 0;
    __pyx_1 = PyObject_CallObject(__pyx_2, 0); if (!__pyx_1) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 299; goto __pyx_L1;}
    Py_DECREF(__pyx_2); __pyx_2 = 0;
    Py_DECREF(__pyx_v_msg);
    __pyx_v_msg = __pyx_1;
    __pyx_1 = 0;
    goto __pyx_L2;
  }
  __pyx_L2:;

  /* "/home/jamie/programming/epimorph/sources/pypm/pypm.pyx":300 */
  __pyx_5 = PyString_AsString(__pyx_v_msg); if (!__pyx_5) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 300; goto __pyx_L1;}
  __pyx_v_cmsg = __pyx_5;

  /* "/home/jamie/programming/epimorph/sources/pypm/pypm.pyx":301 */
  __pyx_v_CurTime = Pt_Time();

  /* "/home/jamie/programming/epimorph/sources/pypm/pypm.pyx":302 */
  __pyx_6 = PyInt_AsLong(__pyx_v_when); if (PyErr_Occurred()) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 302; goto __pyx_L1;}
  __pyx_v_err = Pm_WriteSysEx(((struct __pyx_obj_4pypm_Output *)__pyx_v_self)->midi,__pyx_6,__pyx_v_cmsg);

  /* "/home/jamie/programming/epimorph/sources/pypm/pypm.pyx":303 */
  __pyx_3 = (__pyx_v_err < 0);
  if (__pyx_3) {
    __pyx_4 = PyString_FromString(Pm_GetErrorText(__pyx_v_err)); if (!__pyx_4) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 303; goto __pyx_L1;}
    __Pyx_Raise(PyExc_Exception, __pyx_4, 0);
    Py_DECREF(__pyx_4); __pyx_4 = 0;
    {__pyx_filename = __pyx_f[0]; __pyx_lineno = 303; goto __pyx_L1;}
    goto __pyx_L3;
  }
  __pyx_L3:;

  /* "/home/jamie/programming/epimorph/sources/pypm/pypm.pyx":304 */
  while (1) {
    __pyx_3 = (Pt_Time() == __pyx_v_CurTime);
    if (!__pyx_3) break;
  }

  __pyx_r = Py_None; Py_INCREF(Py_None);
  goto __pyx_L0;
  __pyx_L1:;
  Py_XDECREF(__pyx_1);
  Py_XDECREF(__pyx_2);
  Py_XDECREF(__pyx_4);
  __Pyx_AddTraceback("pypm.Output.WriteSysEx");
  __pyx_r = 0;
  __pyx_L0:;
  Py_DECREF(__pyx_v_self);
  Py_DECREF(__pyx_v_when);
  Py_DECREF(__pyx_v_msg);
  return __pyx_r;
}

static PyObject *__pyx_k14p;

static char __pyx_k14[] = "MIDI input opened.";

static int __pyx_f_4pypm_5Input___init__(PyObject *__pyx_v_self, PyObject *__pyx_args, PyObject *__pyx_kwds); /*proto*/
static int __pyx_f_4pypm_5Input___init__(PyObject *__pyx_v_self, PyObject *__pyx_args, PyObject *__pyx_kwds) {
  PyObject *__pyx_v_InputDevice = 0;
  PmError __pyx_v_err;
  int __pyx_r;
  int __pyx_1;
  PyObject *__pyx_2 = 0;
  static char *__pyx_argnames[] = {"InputDevice",0};
  if (!PyArg_ParseTupleAndKeywords(__pyx_args, __pyx_kwds, "O", __pyx_argnames, &__pyx_v_InputDevice)) return -1;
  Py_INCREF(__pyx_v_self);
  Py_INCREF(__pyx_v_InputDevice);

  /* "/home/jamie/programming/epimorph/sources/pypm/pypm.pyx":319 */
  __pyx_1 = PyInt_AsLong(__pyx_v_InputDevice); if (PyErr_Occurred()) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 319; goto __pyx_L1;}
  ((struct __pyx_obj_4pypm_Input *)__pyx_v_self)->i = __pyx_1;

  /* "/home/jamie/programming/epimorph/sources/pypm/pypm.pyx":320 */
  ((struct __pyx_obj_4pypm_Input *)__pyx_v_self)->debug = 0;

  /* "/home/jamie/programming/epimorph/sources/pypm/pypm.pyx":321 */
  __pyx_v_err = Pm_OpenInput((&((struct __pyx_obj_4pypm_Input *)__pyx_v_self)->midi),((struct __pyx_obj_4pypm_Input *)__pyx_v_self)->i,NULL,100,(&Pt_Time),NULL);

  /* "/home/jamie/programming/epimorph/sources/pypm/pypm.pyx":322 */
  __pyx_1 = (__pyx_v_err < 0);
  if (__pyx_1) {
    __pyx_2 = PyString_FromString(Pm_GetErrorText(__pyx_v_err)); if (!__pyx_2) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 322; goto __pyx_L1;}
    __Pyx_Raise(PyExc_Exception, __pyx_2, 0);
    Py_DECREF(__pyx_2); __pyx_2 = 0;
    {__pyx_filename = __pyx_f[0]; __pyx_lineno = 322; goto __pyx_L1;}
    goto __pyx_L2;
  }
  __pyx_L2:;

  /* "/home/jamie/programming/epimorph/sources/pypm/pypm.pyx":323 */
  __pyx_1 = ((struct __pyx_obj_4pypm_Input *)__pyx_v_self)->debug;
  if (__pyx_1) {
    if (__Pyx_PrintItem(__pyx_k14p) < 0) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 323; goto __pyx_L1;}
    if (__Pyx_PrintNewline() < 0) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 323; goto __pyx_L1;}
    goto __pyx_L3;
  }
  __pyx_L3:;

  __pyx_r = 0;
  goto __pyx_L0;
  __pyx_L1:;
  Py_XDECREF(__pyx_2);
  __Pyx_AddTraceback("pypm.Input.__init__");
  __pyx_r = -1;
  __pyx_L0:;
  Py_DECREF(__pyx_v_self);
  Py_DECREF(__pyx_v_InputDevice);
  return __pyx_r;
}

static PyObject *__pyx_k15p;

static char __pyx_k15[] = "Closing MIDI input stream and destroying instance";

static void __pyx_f_4pypm_5Input___dealloc__(PyObject *__pyx_v_self); /*proto*/
static void __pyx_f_4pypm_5Input___dealloc__(PyObject *__pyx_v_self) {
  PmError __pyx_v_err;
  int __pyx_1;
  PyObject *__pyx_2 = 0;
  Py_INCREF(__pyx_v_self);

  /* "/home/jamie/programming/epimorph/sources/pypm/pypm.pyx":327 */
  __pyx_1 = ((struct __pyx_obj_4pypm_Input *)__pyx_v_self)->debug;
  if (__pyx_1) {
    if (__Pyx_PrintItem(__pyx_k15p) < 0) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 327; goto __pyx_L1;}
    if (__Pyx_PrintNewline() < 0) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 327; goto __pyx_L1;}
    goto __pyx_L2;
  }
  __pyx_L2:;

  /* "/home/jamie/programming/epimorph/sources/pypm/pypm.pyx":328 */
  Pm_Abort(((struct __pyx_obj_4pypm_Input *)__pyx_v_self)->midi);

  /* "/home/jamie/programming/epimorph/sources/pypm/pypm.pyx":329 */
  __pyx_1 = (__pyx_v_err < 0);
  if (__pyx_1) {
    __pyx_2 = PyString_FromString(Pm_GetErrorText(__pyx_v_err)); if (!__pyx_2) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 329; goto __pyx_L1;}
    __Pyx_Raise(PyExc_Exception, __pyx_2, 0);
    Py_DECREF(__pyx_2); __pyx_2 = 0;
    {__pyx_filename = __pyx_f[0]; __pyx_lineno = 329; goto __pyx_L1;}
    goto __pyx_L3;
  }
  __pyx_L3:;

  /* "/home/jamie/programming/epimorph/sources/pypm/pypm.pyx":330 */
  Pm_Close(((struct __pyx_obj_4pypm_Input *)__pyx_v_self)->midi);

  /* "/home/jamie/programming/epimorph/sources/pypm/pypm.pyx":331 */
  __pyx_1 = (__pyx_v_err < 0);
  if (__pyx_1) {
    __pyx_2 = PyString_FromString(Pm_GetErrorText(__pyx_v_err)); if (!__pyx_2) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 331; goto __pyx_L1;}
    __Pyx_Raise(PyExc_Exception, __pyx_2, 0);
    Py_DECREF(__pyx_2); __pyx_2 = 0;
    {__pyx_filename = __pyx_f[0]; __pyx_lineno = 331; goto __pyx_L1;}
    goto __pyx_L4;
  }
  __pyx_L4:;

  goto __pyx_L0;
  __pyx_L1:;
  Py_XDECREF(__pyx_2);
  __Pyx_AddTraceback("pypm.Input.__dealloc__");
  __pyx_L0:;
  Py_DECREF(__pyx_v_self);
}

static PyObject *__pyx_f_4pypm_5Input_SetFilter(PyObject *__pyx_v_self, PyObject *__pyx_args, PyObject *__pyx_kwds); /*proto*/
static char __pyx_doc_4pypm_5Input_SetFilter[] = "\n    SetFilter(<filters>) sets filters on an open input stream\n    to drop selected input types. By default, only active sensing\n    messages are filtered. To prohibit, say, active sensing and\n    sysex messages, call\n    SetFilter(stream, FILT_ACTIVE | FILT_SYSEX);\n\n    Filtering is useful when midi routing or midi thru functionality\n    is being provided by the user application.\n    For example, you may want to exclude timing messages\n    (clock, MTC, start/stop/continue), while allowing note-related\n    messages to pass. Or you may be using a sequencer or drum-machine\n    for MIDI clock information but want to exclude any notes\n    it may play.\n\n    Note: SetFilter empties the buffer after setting the filter,\n    just in case anything got through.\n        ";
static PyObject *__pyx_f_4pypm_5Input_SetFilter(PyObject *__pyx_v_self, PyObject *__pyx_args, PyObject *__pyx_kwds) {
  PyObject *__pyx_v_filters = 0;
  PmEvent __pyx_v_buffer[1];
  PmError __pyx_v_err;
  PyObject *__pyx_r;
  long __pyx_1;
  int __pyx_2;
  PyObject *__pyx_3 = 0;
  static char *__pyx_argnames[] = {"filters",0};
  if (!PyArg_ParseTupleAndKeywords(__pyx_args, __pyx_kwds, "O", __pyx_argnames, &__pyx_v_filters)) return 0;
  Py_INCREF(__pyx_v_self);
  Py_INCREF(__pyx_v_filters);

  /* "/home/jamie/programming/epimorph/sources/pypm/pypm.pyx":355 */
  __pyx_1 = PyInt_AsLong(__pyx_v_filters); if (PyErr_Occurred()) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 355; goto __pyx_L1;}
  Pm_SetFilter(((struct __pyx_obj_4pypm_Input *)__pyx_v_self)->midi,__pyx_1);

  /* "/home/jamie/programming/epimorph/sources/pypm/pypm.pyx":356 */
  __pyx_2 = (__pyx_v_err < 0);
  if (__pyx_2) {
    __pyx_3 = PyString_FromString(Pm_GetErrorText(__pyx_v_err)); if (!__pyx_3) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 356; goto __pyx_L1;}
    __Pyx_Raise(PyExc_Exception, __pyx_3, 0);
    Py_DECREF(__pyx_3); __pyx_3 = 0;
    {__pyx_filename = __pyx_f[0]; __pyx_lineno = 356; goto __pyx_L1;}
    goto __pyx_L2;
  }
  __pyx_L2:;

  /* "/home/jamie/programming/epimorph/sources/pypm/pypm.pyx":357 */
  while (1) {
    __pyx_2 = (Pm_Poll(((struct __pyx_obj_4pypm_Input *)__pyx_v_self)->midi) != pmNoError);
    if (!__pyx_2) break;

    /* "/home/jamie/programming/epimorph/sources/pypm/pypm.pyx":358 */
    __pyx_v_err = Pm_Read(((struct __pyx_obj_4pypm_Input *)__pyx_v_self)->midi,__pyx_v_buffer,1);

    /* "/home/jamie/programming/epimorph/sources/pypm/pypm.pyx":359 */
    __pyx_2 = (__pyx_v_err < 0);
    if (__pyx_2) {
      __pyx_3 = PyString_FromString(Pm_GetErrorText(__pyx_v_err)); if (!__pyx_3) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 359; goto __pyx_L1;}
      __Pyx_Raise(PyExc_Exception, __pyx_3, 0);
      Py_DECREF(__pyx_3); __pyx_3 = 0;
      {__pyx_filename = __pyx_f[0]; __pyx_lineno = 359; goto __pyx_L1;}
      goto __pyx_L5;
    }
    __pyx_L5:;
  }

  __pyx_r = Py_None; Py_INCREF(Py_None);
  goto __pyx_L0;
  __pyx_L1:;
  Py_XDECREF(__pyx_3);
  __Pyx_AddTraceback("pypm.Input.SetFilter");
  __pyx_r = 0;
  __pyx_L0:;
  Py_DECREF(__pyx_v_self);
  Py_DECREF(__pyx_v_filters);
  return __pyx_r;
}

static PyObject *__pyx_f_4pypm_5Input_SetChannelMask(PyObject *__pyx_v_self, PyObject *__pyx_args, PyObject *__pyx_kwds); /*proto*/
static char __pyx_doc_4pypm_5Input_SetChannelMask[] = "\n    SetChannelMask(<mask>) filters incoming messages based on channel.\n    The mask is a 16-bit bitfield corresponding to appropriate channels\n    Channel(<channel>) can assist in calling this function.\n    i.e. to set receive only input on channel 1, call with\n    SetChannelMask(Channel(1))\n    Multiple channels should be OR\'d together, like\n    SetChannelMask(Channel(10) | Channel(11))\n    note: PyPortMidi Channel function has been altered from\n          the original PortMidi c call to correct for what\n          seems to be a bug --- i.e. channel filters were\n          all numbered from 0 to 15 instead of 1 to 16.\n        ";
static PyObject *__pyx_f_4pypm_5Input_SetChannelMask(PyObject *__pyx_v_self, PyObject *__pyx_args, PyObject *__pyx_kwds) {
  PyObject *__pyx_v_mask = 0;
  PmError __pyx_v_err;
  PyObject *__pyx_r;
  int __pyx_1;
  PyObject *__pyx_2 = 0;
  static char *__pyx_argnames[] = {"mask",0};
  if (!PyArg_ParseTupleAndKeywords(__pyx_args, __pyx_kwds, "O", __pyx_argnames, &__pyx_v_mask)) return 0;
  Py_INCREF(__pyx_v_self);
  Py_INCREF(__pyx_v_mask);

  /* "/home/jamie/programming/epimorph/sources/pypm/pypm.pyx":376 */
  __pyx_1 = PyInt_AsLong(__pyx_v_mask); if (PyErr_Occurred()) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 376; goto __pyx_L1;}
  __pyx_v_err = Pm_SetChannelMask(((struct __pyx_obj_4pypm_Input *)__pyx_v_self)->midi,__pyx_1);

  /* "/home/jamie/programming/epimorph/sources/pypm/pypm.pyx":377 */
  __pyx_1 = (__pyx_v_err < 0);
  if (__pyx_1) {
    __pyx_2 = PyString_FromString(Pm_GetErrorText(__pyx_v_err)); if (!__pyx_2) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 377; goto __pyx_L1;}
    __Pyx_Raise(PyExc_Exception, __pyx_2, 0);
    Py_DECREF(__pyx_2); __pyx_2 = 0;
    {__pyx_filename = __pyx_f[0]; __pyx_lineno = 377; goto __pyx_L1;}
    goto __pyx_L2;
  }
  __pyx_L2:;

  __pyx_r = Py_None; Py_INCREF(Py_None);
  goto __pyx_L0;
  __pyx_L1:;
  Py_XDECREF(__pyx_2);
  __Pyx_AddTraceback("pypm.Input.SetChannelMask");
  __pyx_r = 0;
  __pyx_L0:;
  Py_DECREF(__pyx_v_self);
  Py_DECREF(__pyx_v_mask);
  return __pyx_r;
}

static PyObject *__pyx_f_4pypm_5Input_Poll(PyObject *__pyx_v_self, PyObject *__pyx_args, PyObject *__pyx_kwds); /*proto*/
static char __pyx_doc_4pypm_5Input_Poll[] = "\n    Poll tests whether input is available,\n    returning TRUE, FALSE, or an error value.\n        ";
static PyObject *__pyx_f_4pypm_5Input_Poll(PyObject *__pyx_v_self, PyObject *__pyx_args, PyObject *__pyx_kwds) {
  PmError __pyx_v_err;
  PyObject *__pyx_r;
  int __pyx_1;
  PyObject *__pyx_2 = 0;
  static char *__pyx_argnames[] = {0};
  if (!PyArg_ParseTupleAndKeywords(__pyx_args, __pyx_kwds, "", __pyx_argnames)) return 0;
  Py_INCREF(__pyx_v_self);

  /* "/home/jamie/programming/epimorph/sources/pypm/pypm.pyx":385 */
  __pyx_v_err = Pm_Poll(((struct __pyx_obj_4pypm_Input *)__pyx_v_self)->midi);

  /* "/home/jamie/programming/epimorph/sources/pypm/pypm.pyx":386 */
  __pyx_1 = (__pyx_v_err < 0);
  if (__pyx_1) {
    __pyx_2 = PyString_FromString(Pm_GetErrorText(__pyx_v_err)); if (!__pyx_2) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 386; goto __pyx_L1;}
    __Pyx_Raise(PyExc_Exception, __pyx_2, 0);
    Py_DECREF(__pyx_2); __pyx_2 = 0;
    {__pyx_filename = __pyx_f[0]; __pyx_lineno = 386; goto __pyx_L1;}
    goto __pyx_L2;
  }
  __pyx_L2:;

  /* "/home/jamie/programming/epimorph/sources/pypm/pypm.pyx":387 */
  __pyx_2 = PyInt_FromLong(__pyx_v_err); if (!__pyx_2) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 387; goto __pyx_L1;}
  __pyx_r = __pyx_2;
  __pyx_2 = 0;
  goto __pyx_L0;

  __pyx_r = Py_None; Py_INCREF(Py_None);
  goto __pyx_L0;
  __pyx_L1:;
  Py_XDECREF(__pyx_2);
  __Pyx_AddTraceback("pypm.Input.Poll");
  __pyx_r = 0;
  __pyx_L0:;
  Py_DECREF(__pyx_v_self);
  return __pyx_r;
}

static PyObject *__pyx_n_append;

static PyObject *__pyx_k16p;
static PyObject *__pyx_k17p;

static char __pyx_k16[] = "maximum buffer length is 1024";
static char __pyx_k17[] = "minimum buffer length is 1";

static PyObject *__pyx_f_4pypm_5Input_Read(PyObject *__pyx_v_self, PyObject *__pyx_args, PyObject *__pyx_kwds); /*proto*/
static char __pyx_doc_4pypm_5Input_Read[] = "\nRead(length): returns up to <length> midi events stored in\nthe buffer and returns them as a list:\n[[[status,data1,data2,data3],timestamp],\n [[status,data1,data2,data3],timestamp],...]\nexample: Read(50) returns all the events in the buffer,\n         up to 50 events.\n        ";
static PyObject *__pyx_f_4pypm_5Input_Read(PyObject *__pyx_v_self, PyObject *__pyx_args, PyObject *__pyx_kwds) {
  PyObject *__pyx_v_length = 0;
  PmEvent __pyx_v_buffer[1024];
  PyObject *__pyx_v_x;
  PyObject *__pyx_v_NumEvents;
  PyObject *__pyx_v_loop;
  PyObject *__pyx_r;
  PyObject *__pyx_1 = 0;
  int __pyx_2;
  long __pyx_3;
  PmError __pyx_4;
  PyObject *__pyx_5 = 0;
  PyObject *__pyx_6 = 0;
  Py_ssize_t __pyx_7;
  PyObject *__pyx_8 = 0;
  PyObject *__pyx_9 = 0;
  PyObject *__pyx_10 = 0;
  PyObject *__pyx_11 = 0;
  static char *__pyx_argnames[] = {"length",0};
  if (!PyArg_ParseTupleAndKeywords(__pyx_args, __pyx_kwds, "O", __pyx_argnames, &__pyx_v_length)) return 0;
  Py_INCREF(__pyx_v_self);
  Py_INCREF(__pyx_v_length);
  __pyx_v_x = Py_None; Py_INCREF(Py_None);
  __pyx_v_NumEvents = Py_None; Py_INCREF(Py_None);
  __pyx_v_loop = Py_None; Py_INCREF(Py_None);

  /* "/home/jamie/programming/epimorph/sources/pypm/pypm.pyx":399 */
  __pyx_1 = PyList_New(0); if (!__pyx_1) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 399; goto __pyx_L1;}
  Py_DECREF(__pyx_v_x);
  __pyx_v_x = __pyx_1;
  __pyx_1 = 0;

  /* "/home/jamie/programming/epimorph/sources/pypm/pypm.pyx":401 */
  __pyx_1 = PyInt_FromLong(1024); if (!__pyx_1) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 401; goto __pyx_L1;}
  if (PyObject_Cmp(__pyx_v_length, __pyx_1, &__pyx_2) < 0) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 401; goto __pyx_L1;}
  __pyx_2 = __pyx_2 > 0;
  Py_DECREF(__pyx_1); __pyx_1 = 0;
  if (__pyx_2) {
    __Pyx_Raise(PyExc_IndexError, __pyx_k16p, 0);
    {__pyx_filename = __pyx_f[0]; __pyx_lineno = 401; goto __pyx_L1;}
    goto __pyx_L2;
  }
  __pyx_L2:;

  /* "/home/jamie/programming/epimorph/sources/pypm/pypm.pyx":402 */
  __pyx_1 = PyInt_FromLong(1); if (!__pyx_1) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 402; goto __pyx_L1;}
  if (PyObject_Cmp(__pyx_v_length, __pyx_1, &__pyx_2) < 0) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 402; goto __pyx_L1;}
  __pyx_2 = __pyx_2 < 0;
  Py_DECREF(__pyx_1); __pyx_1 = 0;
  if (__pyx_2) {
    __Pyx_Raise(PyExc_IndexError, __pyx_k17p, 0);
    {__pyx_filename = __pyx_f[0]; __pyx_lineno = 402; goto __pyx_L1;}
    goto __pyx_L3;
  }
  __pyx_L3:;

  /* "/home/jamie/programming/epimorph/sources/pypm/pypm.pyx":403 */
  __pyx_3 = PyInt_AsLong(__pyx_v_length); if (PyErr_Occurred()) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 403; goto __pyx_L1;}
  __pyx_1 = PyInt_FromLong(Pm_Read(((struct __pyx_obj_4pypm_Input *)__pyx_v_self)->midi,__pyx_v_buffer,__pyx_3)); if (!__pyx_1) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 403; goto __pyx_L1;}
  Py_DECREF(__pyx_v_NumEvents);
  __pyx_v_NumEvents = __pyx_1;
  __pyx_1 = 0;

  /* "/home/jamie/programming/epimorph/sources/pypm/pypm.pyx":404 */
  __pyx_1 = PyInt_FromLong(0); if (!__pyx_1) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 404; goto __pyx_L1;}
  if (PyObject_Cmp(__pyx_v_NumEvents, __pyx_1, &__pyx_2) < 0) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 404; goto __pyx_L1;}
  __pyx_2 = __pyx_2 < 0;
  Py_DECREF(__pyx_1); __pyx_1 = 0;
  if (__pyx_2) {
    __pyx_4 = ((PmError)PyInt_AsLong(__pyx_v_NumEvents)); if (PyErr_Occurred()) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 404; goto __pyx_L1;}
    __pyx_1 = PyString_FromString(Pm_GetErrorText(__pyx_4)); if (!__pyx_1) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 404; goto __pyx_L1;}
    __Pyx_Raise(PyExc_Exception, __pyx_1, 0);
    Py_DECREF(__pyx_1); __pyx_1 = 0;
    {__pyx_filename = __pyx_f[0]; __pyx_lineno = 404; goto __pyx_L1;}
    goto __pyx_L4;
  }
  __pyx_L4:;

  /* "/home/jamie/programming/epimorph/sources/pypm/pypm.pyx":405 */
  __pyx_1 = PyList_New(0); if (!__pyx_1) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 405; goto __pyx_L1;}
  Py_DECREF(__pyx_v_x);
  __pyx_v_x = __pyx_1;
  __pyx_1 = 0;

  /* "/home/jamie/programming/epimorph/sources/pypm/pypm.pyx":406 */
  __pyx_1 = PyInt_FromLong(1); if (!__pyx_1) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 406; goto __pyx_L1;}
  if (PyObject_Cmp(__pyx_v_NumEvents, __pyx_1, &__pyx_2) < 0) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 406; goto __pyx_L1;}
  __pyx_2 = __pyx_2 >= 0;
  Py_DECREF(__pyx_1); __pyx_1 = 0;
  if (__pyx_2) {
    __pyx_1 = __Pyx_GetName(__pyx_b, __pyx_n_range); if (!__pyx_1) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 407; goto __pyx_L1;}
    __pyx_5 = PyTuple_New(1); if (!__pyx_5) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 407; goto __pyx_L1;}
    Py_INCREF(__pyx_v_NumEvents);
    PyTuple_SET_ITEM(__pyx_5, 0, __pyx_v_NumEvents);
    __pyx_6 = PyObject_CallObject(__pyx_1, __pyx_5); if (!__pyx_6) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 407; goto __pyx_L1;}
    Py_DECREF(__pyx_1); __pyx_1 = 0;
    Py_DECREF(__pyx_5); __pyx_5 = 0;
    __pyx_1 = PyObject_GetIter(__pyx_6); if (!__pyx_1) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 407; goto __pyx_L1;}
    Py_DECREF(__pyx_6); __pyx_6 = 0;
    for (;;) {
      __pyx_5 = PyIter_Next(__pyx_1);
      if (!__pyx_5) {
        if (PyErr_Occurred()) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 407; goto __pyx_L1;}
        break;
      }
      Py_DECREF(__pyx_v_loop);
      __pyx_v_loop = __pyx_5;
      __pyx_5 = 0;
      __pyx_6 = PyObject_GetAttr(__pyx_v_x, __pyx_n_append); if (!__pyx_6) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 408; goto __pyx_L1;}
      __pyx_7 = PyInt_AsSsize_t(__pyx_v_loop); if (PyErr_Occurred()) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 408; goto __pyx_L1;}
      __pyx_5 = PyInt_FromLong(((__pyx_v_buffer[__pyx_7]).message & 0xff)); if (!__pyx_5) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 408; goto __pyx_L1;}
      __pyx_7 = PyInt_AsSsize_t(__pyx_v_loop); if (PyErr_Occurred()) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 408; goto __pyx_L1;}
      __pyx_8 = PyInt_FromLong((((__pyx_v_buffer[__pyx_7]).message >> 8) & 0xFF)); if (!__pyx_8) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 408; goto __pyx_L1;}
      __pyx_7 = PyInt_AsSsize_t(__pyx_v_loop); if (PyErr_Occurred()) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 408; goto __pyx_L1;}
      __pyx_9 = PyInt_FromLong((((__pyx_v_buffer[__pyx_7]).message >> 16) & 0xFF)); if (!__pyx_9) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 408; goto __pyx_L1;}
      __pyx_7 = PyInt_AsSsize_t(__pyx_v_loop); if (PyErr_Occurred()) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 408; goto __pyx_L1;}
      __pyx_10 = PyInt_FromLong((((__pyx_v_buffer[__pyx_7]).message >> 24) & 0xFF)); if (!__pyx_10) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 408; goto __pyx_L1;}
      __pyx_11 = PyList_New(4); if (!__pyx_11) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 408; goto __pyx_L1;}
      PyList_SET_ITEM(__pyx_11, 0, __pyx_5);
      PyList_SET_ITEM(__pyx_11, 1, __pyx_8);
      PyList_SET_ITEM(__pyx_11, 2, __pyx_9);
      PyList_SET_ITEM(__pyx_11, 3, __pyx_10);
      __pyx_5 = 0;
      __pyx_8 = 0;
      __pyx_9 = 0;
      __pyx_10 = 0;
      __pyx_7 = PyInt_AsSsize_t(__pyx_v_loop); if (PyErr_Occurred()) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 408; goto __pyx_L1;}
      __pyx_5 = PyInt_FromLong((__pyx_v_buffer[__pyx_7]).timestamp); if (!__pyx_5) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 408; goto __pyx_L1;}
      __pyx_8 = PyList_New(2); if (!__pyx_8) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 408; goto __pyx_L1;}
      PyList_SET_ITEM(__pyx_8, 0, __pyx_11);
      PyList_SET_ITEM(__pyx_8, 1, __pyx_5);
      __pyx_11 = 0;
      __pyx_5 = 0;
      __pyx_9 = PyTuple_New(1); if (!__pyx_9) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 408; goto __pyx_L1;}
      PyTuple_SET_ITEM(__pyx_9, 0, __pyx_8);
      __pyx_8 = 0;
      __pyx_10 = PyObject_CallObject(__pyx_6, __pyx_9); if (!__pyx_10) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 408; goto __pyx_L1;}
      Py_DECREF(__pyx_6); __pyx_6 = 0;
      Py_DECREF(__pyx_9); __pyx_9 = 0;
      Py_DECREF(__pyx_10); __pyx_10 = 0;
    }
    Py_DECREF(__pyx_1); __pyx_1 = 0;
    goto __pyx_L5;
  }
  __pyx_L5:;

  /* "/home/jamie/programming/epimorph/sources/pypm/pypm.pyx":409 */
  Py_INCREF(__pyx_v_x);
  __pyx_r = __pyx_v_x;
  goto __pyx_L0;

  __pyx_r = Py_None; Py_INCREF(Py_None);
  goto __pyx_L0;
  __pyx_L1:;
  Py_XDECREF(__pyx_1);
  Py_XDECREF(__pyx_5);
  Py_XDECREF(__pyx_6);
  Py_XDECREF(__pyx_8);
  Py_XDECREF(__pyx_9);
  Py_XDECREF(__pyx_10);
  Py_XDECREF(__pyx_11);
  __Pyx_AddTraceback("pypm.Input.Read");
  __pyx_r = 0;
  __pyx_L0:;
  Py_DECREF(__pyx_v_x);
  Py_DECREF(__pyx_v_NumEvents);
  Py_DECREF(__pyx_v_loop);
  Py_DECREF(__pyx_v_self);
  Py_DECREF(__pyx_v_length);
  return __pyx_r;
}

static __Pyx_InternTabEntry __pyx_intern_tab[] = {
  {&__pyx_n_B, "B"},
  {&__pyx_n_FALSE, "FALSE"},
  {&__pyx_n_FILT_ACTIVE, "FILT_ACTIVE"},
  {&__pyx_n_FILT_AFTERTOUCH, "FILT_AFTERTOUCH"},
  {&__pyx_n_FILT_CHANNEL_AFTERTOUCH, "FILT_CHANNEL_AFTERTOUCH"},
  {&__pyx_n_FILT_CLOCK, "FILT_CLOCK"},
  {&__pyx_n_FILT_CONTROL, "FILT_CONTROL"},
  {&__pyx_n_FILT_F9, "FILT_F9"},
  {&__pyx_n_FILT_FD, "FILT_FD"},
  {&__pyx_n_FILT_MTC, "FILT_MTC"},
  {&__pyx_n_FILT_NOTE, "FILT_NOTE"},
  {&__pyx_n_FILT_PITCHBEND, "FILT_PITCHBEND"},
  {&__pyx_n_FILT_PLAY, "FILT_PLAY"},
  {&__pyx_n_FILT_POLY_AFTERTOUCH, "FILT_POLY_AFTERTOUCH"},
  {&__pyx_n_FILT_PROGRAM, "FILT_PROGRAM"},
  {&__pyx_n_FILT_REALTIME, "FILT_REALTIME"},
  {&__pyx_n_FILT_RESET, "FILT_RESET"},
  {&__pyx_n_FILT_SONG_POSITION, "FILT_SONG_POSITION"},
  {&__pyx_n_FILT_SONG_SELECT, "FILT_SONG_SELECT"},
  {&__pyx_n_FILT_SYSEX, "FILT_SYSEX"},
  {&__pyx_n_FILT_TICK, "FILT_TICK"},
  {&__pyx_n_FILT_TUNE, "FILT_TUNE"},
  {&__pyx_n_FILT_UNDEFINED, "FILT_UNDEFINED"},
  {&__pyx_n_TRUE, "TRUE"},
  {&__pyx_n___version__, "__version__"},
  {&__pyx_n_append, "append"},
  {&__pyx_n_array, "array"},
  {&__pyx_n_range, "range"},
  {&__pyx_n_tostring, "tostring"},
  {0, 0}
};

static __Pyx_StringTabEntry __pyx_string_tab[] = {
  {&__pyx_k1p, __pyx_k1, sizeof(__pyx_k1)},
  {&__pyx_k5p, __pyx_k5, sizeof(__pyx_k5)},
  {&__pyx_k6p, __pyx_k6, sizeof(__pyx_k6)},
  {&__pyx_k7p, __pyx_k7, sizeof(__pyx_k7)},
  {&__pyx_k8p, __pyx_k8, sizeof(__pyx_k8)},
  {&__pyx_k9p, __pyx_k9, sizeof(__pyx_k9)},
  {&__pyx_k10p, __pyx_k10, sizeof(__pyx_k10)},
  {&__pyx_k11p, __pyx_k11, sizeof(__pyx_k11)},
  {&__pyx_k12p, __pyx_k12, sizeof(__pyx_k12)},
  {&__pyx_k14p, __pyx_k14, sizeof(__pyx_k14)},
  {&__pyx_k15p, __pyx_k15, sizeof(__pyx_k15)},
  {&__pyx_k16p, __pyx_k16, sizeof(__pyx_k16)},
  {&__pyx_k17p, __pyx_k17, sizeof(__pyx_k17)},
  {0, 0, 0}
};

static PyObject *__pyx_tp_new_4pypm_Output(PyTypeObject *t, PyObject *a, PyObject *k) {
  PyObject *o = (*t->tp_alloc)(t, 0);
  if (!o) return 0;
  return o;
}

static void __pyx_tp_dealloc_4pypm_Output(PyObject *o) {
  {
    PyObject *etype, *eval, *etb;
    PyErr_Fetch(&etype, &eval, &etb);
    ++o->ob_refcnt;
    __pyx_f_4pypm_6Output___dealloc__(o);
    if (PyErr_Occurred()) PyErr_WriteUnraisable(o);
    --o->ob_refcnt;
    PyErr_Restore(etype, eval, etb);
  }
  (*o->ob_type->tp_free)(o);
}

static struct PyMethodDef __pyx_methods_4pypm_Output[] = {
  {"Write", (PyCFunction)__pyx_f_4pypm_6Output_Write, METH_VARARGS|METH_KEYWORDS, __pyx_doc_4pypm_6Output_Write},
  {"WriteShort", (PyCFunction)__pyx_f_4pypm_6Output_WriteShort, METH_VARARGS|METH_KEYWORDS, __pyx_doc_4pypm_6Output_WriteShort},
  {"WriteSysEx", (PyCFunction)__pyx_f_4pypm_6Output_WriteSysEx, METH_VARARGS|METH_KEYWORDS, __pyx_doc_4pypm_6Output_WriteSysEx},
  {0, 0, 0, 0}
};

static PyNumberMethods __pyx_tp_as_number_Output = {
  0, /*nb_add*/
  0, /*nb_subtract*/
  0, /*nb_multiply*/
  0, /*nb_divide*/
  0, /*nb_remainder*/
  0, /*nb_divmod*/
  0, /*nb_power*/
  0, /*nb_negative*/
  0, /*nb_positive*/
  0, /*nb_absolute*/
  0, /*nb_nonzero*/
  0, /*nb_invert*/
  0, /*nb_lshift*/
  0, /*nb_rshift*/
  0, /*nb_and*/
  0, /*nb_xor*/
  0, /*nb_or*/
  0, /*nb_coerce*/
  0, /*nb_int*/
  0, /*nb_long*/
  0, /*nb_float*/
  0, /*nb_oct*/
  0, /*nb_hex*/
  0, /*nb_inplace_add*/
  0, /*nb_inplace_subtract*/
  0, /*nb_inplace_multiply*/
  0, /*nb_inplace_divide*/
  0, /*nb_inplace_remainder*/
  0, /*nb_inplace_power*/
  0, /*nb_inplace_lshift*/
  0, /*nb_inplace_rshift*/
  0, /*nb_inplace_and*/
  0, /*nb_inplace_xor*/
  0, /*nb_inplace_or*/
  0, /*nb_floor_divide*/
  0, /*nb_true_divide*/
  0, /*nb_inplace_floor_divide*/
  0, /*nb_inplace_true_divide*/
  #if Py_TPFLAGS_DEFAULT & Py_TPFLAGS_HAVE_INDEX
  0, /*nb_index*/
  #endif
};

static PySequenceMethods __pyx_tp_as_sequence_Output = {
  0, /*sq_length*/
  0, /*sq_concat*/
  0, /*sq_repeat*/
  0, /*sq_item*/
  0, /*sq_slice*/
  0, /*sq_ass_item*/
  0, /*sq_ass_slice*/
  0, /*sq_contains*/
  0, /*sq_inplace_concat*/
  0, /*sq_inplace_repeat*/
};

static PyMappingMethods __pyx_tp_as_mapping_Output = {
  0, /*mp_length*/
  0, /*mp_subscript*/
  0, /*mp_ass_subscript*/
};

static PyBufferProcs __pyx_tp_as_buffer_Output = {
  0, /*bf_getreadbuffer*/
  0, /*bf_getwritebuffer*/
  0, /*bf_getsegcount*/
  0, /*bf_getcharbuffer*/
};

PyTypeObject __pyx_type_4pypm_Output = {
  PyObject_HEAD_INIT(0)
  0, /*ob_size*/
  "pypm.Output", /*tp_name*/
  sizeof(struct __pyx_obj_4pypm_Output), /*tp_basicsize*/
  0, /*tp_itemsize*/
  __pyx_tp_dealloc_4pypm_Output, /*tp_dealloc*/
  0, /*tp_print*/
  0, /*tp_getattr*/
  0, /*tp_setattr*/
  0, /*tp_compare*/
  0, /*tp_repr*/
  &__pyx_tp_as_number_Output, /*tp_as_number*/
  &__pyx_tp_as_sequence_Output, /*tp_as_sequence*/
  &__pyx_tp_as_mapping_Output, /*tp_as_mapping*/
  0, /*tp_hash*/
  0, /*tp_call*/
  0, /*tp_str*/
  0, /*tp_getattro*/
  0, /*tp_setattro*/
  &__pyx_tp_as_buffer_Output, /*tp_as_buffer*/
  Py_TPFLAGS_DEFAULT|Py_TPFLAGS_CHECKTYPES|Py_TPFLAGS_BASETYPE, /*tp_flags*/
  "\nclass Output:\n    define an output MIDI stream. Takes the form:\n        x = pypm.Output(MidiOutputDevice, latency)\n    latency is in ms.\n    If latency = 0 then timestamps for output are ignored.\n    ", /*tp_doc*/
  0, /*tp_traverse*/
  0, /*tp_clear*/
  0, /*tp_richcompare*/
  0, /*tp_weaklistoffset*/
  0, /*tp_iter*/
  0, /*tp_iternext*/
  __pyx_methods_4pypm_Output, /*tp_methods*/
  0, /*tp_members*/
  0, /*tp_getset*/
  0, /*tp_base*/
  0, /*tp_dict*/
  0, /*tp_descr_get*/
  0, /*tp_descr_set*/
  0, /*tp_dictoffset*/
  __pyx_f_4pypm_6Output___init__, /*tp_init*/
  0, /*tp_alloc*/
  __pyx_tp_new_4pypm_Output, /*tp_new*/
  0, /*tp_free*/
  0, /*tp_is_gc*/
  0, /*tp_bases*/
  0, /*tp_mro*/
  0, /*tp_cache*/
  0, /*tp_subclasses*/
  0, /*tp_weaklist*/
};

static PyObject *__pyx_tp_new_4pypm_Input(PyTypeObject *t, PyObject *a, PyObject *k) {
  PyObject *o = (*t->tp_alloc)(t, 0);
  if (!o) return 0;
  return o;
}

static void __pyx_tp_dealloc_4pypm_Input(PyObject *o) {
  {
    PyObject *etype, *eval, *etb;
    PyErr_Fetch(&etype, &eval, &etb);
    ++o->ob_refcnt;
    __pyx_f_4pypm_5Input___dealloc__(o);
    if (PyErr_Occurred()) PyErr_WriteUnraisable(o);
    --o->ob_refcnt;
    PyErr_Restore(etype, eval, etb);
  }
  (*o->ob_type->tp_free)(o);
}

static struct PyMethodDef __pyx_methods_4pypm_Input[] = {
  {"SetFilter", (PyCFunction)__pyx_f_4pypm_5Input_SetFilter, METH_VARARGS|METH_KEYWORDS, __pyx_doc_4pypm_5Input_SetFilter},
  {"SetChannelMask", (PyCFunction)__pyx_f_4pypm_5Input_SetChannelMask, METH_VARARGS|METH_KEYWORDS, __pyx_doc_4pypm_5Input_SetChannelMask},
  {"Poll", (PyCFunction)__pyx_f_4pypm_5Input_Poll, METH_VARARGS|METH_KEYWORDS, __pyx_doc_4pypm_5Input_Poll},
  {"Read", (PyCFunction)__pyx_f_4pypm_5Input_Read, METH_VARARGS|METH_KEYWORDS, __pyx_doc_4pypm_5Input_Read},
  {0, 0, 0, 0}
};

static PyNumberMethods __pyx_tp_as_number_Input = {
  0, /*nb_add*/
  0, /*nb_subtract*/
  0, /*nb_multiply*/
  0, /*nb_divide*/
  0, /*nb_remainder*/
  0, /*nb_divmod*/
  0, /*nb_power*/
  0, /*nb_negative*/
  0, /*nb_positive*/
  0, /*nb_absolute*/
  0, /*nb_nonzero*/
  0, /*nb_invert*/
  0, /*nb_lshift*/
  0, /*nb_rshift*/
  0, /*nb_and*/
  0, /*nb_xor*/
  0, /*nb_or*/
  0, /*nb_coerce*/
  0, /*nb_int*/
  0, /*nb_long*/
  0, /*nb_float*/
  0, /*nb_oct*/
  0, /*nb_hex*/
  0, /*nb_inplace_add*/
  0, /*nb_inplace_subtract*/
  0, /*nb_inplace_multiply*/
  0, /*nb_inplace_divide*/
  0, /*nb_inplace_remainder*/
  0, /*nb_inplace_power*/
  0, /*nb_inplace_lshift*/
  0, /*nb_inplace_rshift*/
  0, /*nb_inplace_and*/
  0, /*nb_inplace_xor*/
  0, /*nb_inplace_or*/
  0, /*nb_floor_divide*/
  0, /*nb_true_divide*/
  0, /*nb_inplace_floor_divide*/
  0, /*nb_inplace_true_divide*/
  #if Py_TPFLAGS_DEFAULT & Py_TPFLAGS_HAVE_INDEX
  0, /*nb_index*/
  #endif
};

static PySequenceMethods __pyx_tp_as_sequence_Input = {
  0, /*sq_length*/
  0, /*sq_concat*/
  0, /*sq_repeat*/
  0, /*sq_item*/
  0, /*sq_slice*/
  0, /*sq_ass_item*/
  0, /*sq_ass_slice*/
  0, /*sq_contains*/
  0, /*sq_inplace_concat*/
  0, /*sq_inplace_repeat*/
};

static PyMappingMethods __pyx_tp_as_mapping_Input = {
  0, /*mp_length*/
  0, /*mp_subscript*/
  0, /*mp_ass_subscript*/
};

static PyBufferProcs __pyx_tp_as_buffer_Input = {
  0, /*bf_getreadbuffer*/
  0, /*bf_getwritebuffer*/
  0, /*bf_getsegcount*/
  0, /*bf_getcharbuffer*/
};

PyTypeObject __pyx_type_4pypm_Input = {
  PyObject_HEAD_INIT(0)
  0, /*ob_size*/
  "pypm.Input", /*tp_name*/
  sizeof(struct __pyx_obj_4pypm_Input), /*tp_basicsize*/
  0, /*tp_itemsize*/
  __pyx_tp_dealloc_4pypm_Input, /*tp_dealloc*/
  0, /*tp_print*/
  0, /*tp_getattr*/
  0, /*tp_setattr*/
  0, /*tp_compare*/
  0, /*tp_repr*/
  &__pyx_tp_as_number_Input, /*tp_as_number*/
  &__pyx_tp_as_sequence_Input, /*tp_as_sequence*/
  &__pyx_tp_as_mapping_Input, /*tp_as_mapping*/
  0, /*tp_hash*/
  0, /*tp_call*/
  0, /*tp_str*/
  0, /*tp_getattro*/
  0, /*tp_setattro*/
  &__pyx_tp_as_buffer_Input, /*tp_as_buffer*/
  Py_TPFLAGS_DEFAULT|Py_TPFLAGS_CHECKTYPES|Py_TPFLAGS_BASETYPE, /*tp_flags*/
  "\nclass Input:\n    define an input MIDI stream. Takes the form:\n        x = pypm.Input(MidiInputDevice)\n    ", /*tp_doc*/
  0, /*tp_traverse*/
  0, /*tp_clear*/
  0, /*tp_richcompare*/
  0, /*tp_weaklistoffset*/
  0, /*tp_iter*/
  0, /*tp_iternext*/
  __pyx_methods_4pypm_Input, /*tp_methods*/
  0, /*tp_members*/
  0, /*tp_getset*/
  0, /*tp_base*/
  0, /*tp_dict*/
  0, /*tp_descr_get*/
  0, /*tp_descr_set*/
  0, /*tp_dictoffset*/
  __pyx_f_4pypm_5Input___init__, /*tp_init*/
  0, /*tp_alloc*/
  __pyx_tp_new_4pypm_Input, /*tp_new*/
  0, /*tp_free*/
  0, /*tp_is_gc*/
  0, /*tp_bases*/
  0, /*tp_mro*/
  0, /*tp_cache*/
  0, /*tp_subclasses*/
  0, /*tp_weaklist*/
};

static struct PyMethodDef __pyx_methods[] = {
  {"Initialize", (PyCFunction)__pyx_f_4pypm_Initialize, METH_VARARGS|METH_KEYWORDS, __pyx_doc_4pypm_Initialize},
  {"Terminate", (PyCFunction)__pyx_f_4pypm_Terminate, METH_VARARGS|METH_KEYWORDS, __pyx_doc_4pypm_Terminate},
  {"GetDefaultInputDeviceID", (PyCFunction)__pyx_f_4pypm_GetDefaultInputDeviceID, METH_VARARGS|METH_KEYWORDS, 0},
  {"GetDefaultOutputDeviceID", (PyCFunction)__pyx_f_4pypm_GetDefaultOutputDeviceID, METH_VARARGS|METH_KEYWORDS, 0},
  {"CountDevices", (PyCFunction)__pyx_f_4pypm_CountDevices, METH_VARARGS|METH_KEYWORDS, 0},
  {"GetDeviceInfo", (PyCFunction)__pyx_f_4pypm_GetDeviceInfo, METH_VARARGS|METH_KEYWORDS, __pyx_doc_4pypm_GetDeviceInfo},
  {"Time", (PyCFunction)__pyx_f_4pypm_Time, METH_VARARGS|METH_KEYWORDS, __pyx_doc_4pypm_Time},
  {"GetErrorText", (PyCFunction)__pyx_f_4pypm_GetErrorText, METH_VARARGS|METH_KEYWORDS, __pyx_doc_4pypm_GetErrorText},
  {"Channel", (PyCFunction)__pyx_f_4pypm_Channel, METH_VARARGS|METH_KEYWORDS, __pyx_doc_4pypm_Channel},
  {0, 0, 0, 0}
};

static void __pyx_init_filenames(void); /*proto*/

PyMODINIT_FUNC initpypm(void); /*proto*/
PyMODINIT_FUNC initpypm(void) {
  PyObject *__pyx_1 = 0;
  PyObject *__pyx_2 = 0;
  __pyx_init_filenames();
  __pyx_m = Py_InitModule4("pypm", __pyx_methods, 0, 0, PYTHON_API_VERSION);
  if (!__pyx_m) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 7; goto __pyx_L1;};
  Py_INCREF(__pyx_m);
  __pyx_b = PyImport_AddModule("__builtin__");
  if (!__pyx_b) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 7; goto __pyx_L1;};
  if (PyObject_SetAttrString(__pyx_m, "__builtins__", __pyx_b) < 0) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 7; goto __pyx_L1;};
  if (__Pyx_InternStrings(__pyx_intern_tab) < 0) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 7; goto __pyx_L1;};
  if (__Pyx_InitStrings(__pyx_string_tab) < 0) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 7; goto __pyx_L1;};
  if (PyType_Ready(&__pyx_type_4pypm_Output) < 0) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 189; goto __pyx_L1;}
  if (PyObject_SetAttrString(__pyx_m, "Output", (PyObject *)&__pyx_type_4pypm_Output) < 0) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 189; goto __pyx_L1;}
  __pyx_ptype_4pypm_Output = &__pyx_type_4pypm_Output;
  if (PyType_Ready(&__pyx_type_4pypm_Input) < 0) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 307; goto __pyx_L1;}
  if (PyObject_SetAttrString(__pyx_m, "Input", (PyObject *)&__pyx_type_4pypm_Input) < 0) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 307; goto __pyx_L1;}
  __pyx_ptype_4pypm_Input = &__pyx_type_4pypm_Input;

  /* "/home/jamie/programming/epimorph/sources/pypm/pypm.pyx":7 */
  if (PyObject_SetAttr(__pyx_m, __pyx_n___version__, __pyx_k1p) < 0) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 7; goto __pyx_L1;}

  /* "/home/jamie/programming/epimorph/sources/pypm/pypm.pyx":9 */
  __pyx_1 = __Pyx_Import(__pyx_n_array, 0); if (!__pyx_1) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 9; goto __pyx_L1;}
  if (PyObject_SetAttr(__pyx_m, __pyx_n_array, __pyx_1) < 0) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 9; goto __pyx_L1;}
  Py_DECREF(__pyx_1); __pyx_1 = 0;

  /* "/home/jamie/programming/epimorph/sources/pypm/pypm.pyx":99 */
  __pyx_1 = PyInt_FromLong(0x1); if (!__pyx_1) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 99; goto __pyx_L1;}
  if (PyObject_SetAttr(__pyx_m, __pyx_n_FILT_ACTIVE, __pyx_1) < 0) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 99; goto __pyx_L1;}
  Py_DECREF(__pyx_1); __pyx_1 = 0;

  /* "/home/jamie/programming/epimorph/sources/pypm/pypm.pyx":100 */
  __pyx_1 = PyInt_FromLong(0x2); if (!__pyx_1) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 100; goto __pyx_L1;}
  if (PyObject_SetAttr(__pyx_m, __pyx_n_FILT_SYSEX, __pyx_1) < 0) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 100; goto __pyx_L1;}
  Py_DECREF(__pyx_1); __pyx_1 = 0;

  /* "/home/jamie/programming/epimorph/sources/pypm/pypm.pyx":101 */
  __pyx_1 = PyInt_FromLong(0x4); if (!__pyx_1) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 101; goto __pyx_L1;}
  if (PyObject_SetAttr(__pyx_m, __pyx_n_FILT_CLOCK, __pyx_1) < 0) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 101; goto __pyx_L1;}
  Py_DECREF(__pyx_1); __pyx_1 = 0;

  /* "/home/jamie/programming/epimorph/sources/pypm/pypm.pyx":102 */
  __pyx_1 = PyInt_FromLong(0x8); if (!__pyx_1) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 102; goto __pyx_L1;}
  if (PyObject_SetAttr(__pyx_m, __pyx_n_FILT_PLAY, __pyx_1) < 0) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 102; goto __pyx_L1;}
  Py_DECREF(__pyx_1); __pyx_1 = 0;

  /* "/home/jamie/programming/epimorph/sources/pypm/pypm.pyx":103 */
  __pyx_1 = PyInt_FromLong(0x10); if (!__pyx_1) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 103; goto __pyx_L1;}
  if (PyObject_SetAttr(__pyx_m, __pyx_n_FILT_F9, __pyx_1) < 0) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 103; goto __pyx_L1;}
  Py_DECREF(__pyx_1); __pyx_1 = 0;

  /* "/home/jamie/programming/epimorph/sources/pypm/pypm.pyx":104 */
  __pyx_1 = PyInt_FromLong(0x10); if (!__pyx_1) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 104; goto __pyx_L1;}
  if (PyObject_SetAttr(__pyx_m, __pyx_n_FILT_TICK, __pyx_1) < 0) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 104; goto __pyx_L1;}
  Py_DECREF(__pyx_1); __pyx_1 = 0;

  /* "/home/jamie/programming/epimorph/sources/pypm/pypm.pyx":105 */
  __pyx_1 = PyInt_FromLong(0x20); if (!__pyx_1) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 105; goto __pyx_L1;}
  if (PyObject_SetAttr(__pyx_m, __pyx_n_FILT_FD, __pyx_1) < 0) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 105; goto __pyx_L1;}
  Py_DECREF(__pyx_1); __pyx_1 = 0;

  /* "/home/jamie/programming/epimorph/sources/pypm/pypm.pyx":106 */
  __pyx_1 = PyInt_FromLong(0x30); if (!__pyx_1) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 106; goto __pyx_L1;}
  if (PyObject_SetAttr(__pyx_m, __pyx_n_FILT_UNDEFINED, __pyx_1) < 0) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 106; goto __pyx_L1;}
  Py_DECREF(__pyx_1); __pyx_1 = 0;

  /* "/home/jamie/programming/epimorph/sources/pypm/pypm.pyx":107 */
  __pyx_1 = PyInt_FromLong(0x40); if (!__pyx_1) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 107; goto __pyx_L1;}
  if (PyObject_SetAttr(__pyx_m, __pyx_n_FILT_RESET, __pyx_1) < 0) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 107; goto __pyx_L1;}
  Py_DECREF(__pyx_1); __pyx_1 = 0;

  /* "/home/jamie/programming/epimorph/sources/pypm/pypm.pyx":108 */
  __pyx_1 = PyInt_FromLong(0x7F); if (!__pyx_1) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 108; goto __pyx_L1;}
  if (PyObject_SetAttr(__pyx_m, __pyx_n_FILT_REALTIME, __pyx_1) < 0) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 108; goto __pyx_L1;}
  Py_DECREF(__pyx_1); __pyx_1 = 0;

  /* "/home/jamie/programming/epimorph/sources/pypm/pypm.pyx":109 */
  __pyx_1 = PyInt_FromLong(0x80); if (!__pyx_1) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 109; goto __pyx_L1;}
  if (PyObject_SetAttr(__pyx_m, __pyx_n_FILT_NOTE, __pyx_1) < 0) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 109; goto __pyx_L1;}
  Py_DECREF(__pyx_1); __pyx_1 = 0;

  /* "/home/jamie/programming/epimorph/sources/pypm/pypm.pyx":110 */
  __pyx_1 = PyInt_FromLong(0x100); if (!__pyx_1) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 110; goto __pyx_L1;}
  if (PyObject_SetAttr(__pyx_m, __pyx_n_FILT_CHANNEL_AFTERTOUCH, __pyx_1) < 0) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 110; goto __pyx_L1;}
  Py_DECREF(__pyx_1); __pyx_1 = 0;

  /* "/home/jamie/programming/epimorph/sources/pypm/pypm.pyx":111 */
  __pyx_1 = PyInt_FromLong(0x200); if (!__pyx_1) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 111; goto __pyx_L1;}
  if (PyObject_SetAttr(__pyx_m, __pyx_n_FILT_POLY_AFTERTOUCH, __pyx_1) < 0) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 111; goto __pyx_L1;}
  Py_DECREF(__pyx_1); __pyx_1 = 0;

  /* "/home/jamie/programming/epimorph/sources/pypm/pypm.pyx":112 */
  __pyx_1 = PyInt_FromLong(0x300); if (!__pyx_1) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 112; goto __pyx_L1;}
  if (PyObject_SetAttr(__pyx_m, __pyx_n_FILT_AFTERTOUCH, __pyx_1) < 0) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 112; goto __pyx_L1;}
  Py_DECREF(__pyx_1); __pyx_1 = 0;

  /* "/home/jamie/programming/epimorph/sources/pypm/pypm.pyx":113 */
  __pyx_1 = PyInt_FromLong(0x400); if (!__pyx_1) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 113; goto __pyx_L1;}
  if (PyObject_SetAttr(__pyx_m, __pyx_n_FILT_PROGRAM, __pyx_1) < 0) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 113; goto __pyx_L1;}
  Py_DECREF(__pyx_1); __pyx_1 = 0;

  /* "/home/jamie/programming/epimorph/sources/pypm/pypm.pyx":114 */
  __pyx_1 = PyInt_FromLong(0x800); if (!__pyx_1) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 114; goto __pyx_L1;}
  if (PyObject_SetAttr(__pyx_m, __pyx_n_FILT_CONTROL, __pyx_1) < 0) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 114; goto __pyx_L1;}
  Py_DECREF(__pyx_1); __pyx_1 = 0;

  /* "/home/jamie/programming/epimorph/sources/pypm/pypm.pyx":115 */
  __pyx_1 = PyInt_FromLong(0x1000); if (!__pyx_1) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 115; goto __pyx_L1;}
  if (PyObject_SetAttr(__pyx_m, __pyx_n_FILT_PITCHBEND, __pyx_1) < 0) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 115; goto __pyx_L1;}
  Py_DECREF(__pyx_1); __pyx_1 = 0;

  /* "/home/jamie/programming/epimorph/sources/pypm/pypm.pyx":116 */
  __pyx_1 = PyInt_FromLong(0x2000); if (!__pyx_1) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 116; goto __pyx_L1;}
  if (PyObject_SetAttr(__pyx_m, __pyx_n_FILT_MTC, __pyx_1) < 0) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 116; goto __pyx_L1;}
  Py_DECREF(__pyx_1); __pyx_1 = 0;

  /* "/home/jamie/programming/epimorph/sources/pypm/pypm.pyx":117 */
  __pyx_1 = PyInt_FromLong(0x4000); if (!__pyx_1) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 117; goto __pyx_L1;}
  if (PyObject_SetAttr(__pyx_m, __pyx_n_FILT_SONG_POSITION, __pyx_1) < 0) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 117; goto __pyx_L1;}
  Py_DECREF(__pyx_1); __pyx_1 = 0;

  /* "/home/jamie/programming/epimorph/sources/pypm/pypm.pyx":118 */
  __pyx_1 = PyInt_FromLong(0x8000); if (!__pyx_1) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 118; goto __pyx_L1;}
  if (PyObject_SetAttr(__pyx_m, __pyx_n_FILT_SONG_SELECT, __pyx_1) < 0) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 118; goto __pyx_L1;}
  Py_DECREF(__pyx_1); __pyx_1 = 0;

  /* "/home/jamie/programming/epimorph/sources/pypm/pypm.pyx":119 */
  __pyx_1 = PyInt_FromLong(0x10000); if (!__pyx_1) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 119; goto __pyx_L1;}
  if (PyObject_SetAttr(__pyx_m, __pyx_n_FILT_TUNE, __pyx_1) < 0) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 119; goto __pyx_L1;}
  Py_DECREF(__pyx_1); __pyx_1 = 0;

  /* "/home/jamie/programming/epimorph/sources/pypm/pypm.pyx":120 */
  __pyx_1 = PyInt_FromLong(0); if (!__pyx_1) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 120; goto __pyx_L1;}
  if (PyObject_SetAttr(__pyx_m, __pyx_n_FALSE, __pyx_1) < 0) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 120; goto __pyx_L1;}
  Py_DECREF(__pyx_1); __pyx_1 = 0;

  /* "/home/jamie/programming/epimorph/sources/pypm/pypm.pyx":121 */
  __pyx_1 = PyInt_FromLong(1); if (!__pyx_1) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 121; goto __pyx_L1;}
  if (PyObject_SetAttr(__pyx_m, __pyx_n_TRUE, __pyx_1) < 0) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 121; goto __pyx_L1;}
  Py_DECREF(__pyx_1); __pyx_1 = 0;

  /* "/home/jamie/programming/epimorph/sources/pypm/pypm.pyx":260 */
  __pyx_1 = PyInt_FromLong(0); if (!__pyx_1) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 260; goto __pyx_L1;}
  __pyx_k3 = __pyx_1;
  __pyx_1 = 0;
  __pyx_2 = PyInt_FromLong(0); if (!__pyx_2) {__pyx_filename = __pyx_f[0]; __pyx_lineno = 260; goto __pyx_L1;}
  __pyx_k4 = __pyx_2;
  __pyx_2 = 0;

  /* "/home/jamie/programming/epimorph/sources/pypm/pypm.pyx":389 */
  return;
  __pyx_L1:;
  Py_XDECREF(__pyx_1);
  Py_XDECREF(__pyx_2);
  __Pyx_AddTraceback("pypm");
}

static char *__pyx_filenames[] = {
  "pypm.pyx",
};

/* Runtime support code */

static void __pyx_init_filenames(void) {
  __pyx_f = __pyx_filenames;
}

static PyObject *__Pyx_Import(PyObject *name, PyObject *from_list) {
    PyObject *__import__ = 0;
    PyObject *empty_list = 0;
    PyObject *module = 0;
    PyObject *global_dict = 0;
    PyObject *empty_dict = 0;
    PyObject *list;
    __import__ = PyObject_GetAttrString(__pyx_b, "__import__");
    if (!__import__)
        goto bad;
    if (from_list)
        list = from_list;
    else {
        empty_list = PyList_New(0);
        if (!empty_list)
            goto bad;
        list = empty_list;
    }
    global_dict = PyModule_GetDict(__pyx_m);
    if (!global_dict)
        goto bad;
    empty_dict = PyDict_New();
    if (!empty_dict)
        goto bad;
    module = PyObject_CallFunction(__import__, "OOOO",
        name, global_dict, empty_dict, list);
bad:
    Py_XDECREF(empty_list);
    Py_XDECREF(__import__);
    Py_XDECREF(empty_dict);
    return module;
}

static PyObject *__Pyx_GetStdout(void) {
    PyObject *f = PySys_GetObject("stdout");
    if (!f) {
        PyErr_SetString(PyExc_RuntimeError, "lost sys.stdout");
    }
    return f;
}

static int __Pyx_PrintItem(PyObject *v) {
    PyObject *f;
    
    if (!(f = __Pyx_GetStdout()))
        return -1;
    if (PyFile_SoftSpace(f, 1)) {
        if (PyFile_WriteString(" ", f) < 0)
            return -1;
    }
    if (PyFile_WriteObject(v, f, Py_PRINT_RAW) < 0)
        return -1;
    if (PyString_Check(v)) {
        char *s = PyString_AsString(v);
        Py_ssize_t len = PyString_Size(v);
        if (len > 0 &&
            isspace(Py_CHARMASK(s[len-1])) &&
            s[len-1] != ' ')
                PyFile_SoftSpace(f, 0);
    }
    return 0;
}

static int __Pyx_PrintNewline(void) {
    PyObject *f;
    
    if (!(f = __Pyx_GetStdout()))
        return -1;
    if (PyFile_WriteString("\n", f) < 0)
        return -1;
    PyFile_SoftSpace(f, 0);
    return 0;
}

static void __Pyx_Raise(PyObject *type, PyObject *value, PyObject *tb) {
    Py_XINCREF(type);
    Py_XINCREF(value);
    Py_XINCREF(tb);
    /* First, check the traceback argument, replacing None with NULL. */
    if (tb == Py_None) {
        Py_DECREF(tb);
        tb = 0;
    }
    else if (tb != NULL && !PyTraceBack_Check(tb)) {
        PyErr_SetString(PyExc_TypeError,
            "raise: arg 3 must be a traceback or None");
        goto raise_error;
    }
    /* Next, replace a missing value with None */
    if (value == NULL) {
        value = Py_None;
        Py_INCREF(value);
    }
    #if PY_VERSION_HEX < 0x02050000
    if (!PyClass_Check(type))
    #else
    if (!PyType_Check(type))
    #endif
    {
        /* Raising an instance.  The value should be a dummy. */
        if (value != Py_None) {
            PyErr_SetString(PyExc_TypeError,
                "instance exception may not have a separate value");
            goto raise_error;
        }
        /* Normalize to raise <class>, <instance> */
        Py_DECREF(value);
        value = type;
        #if PY_VERSION_HEX < 0x02050000
            if (PyInstance_Check(type)) {
                type = (PyObject*) ((PyInstanceObject*)type)->in_class;
                Py_INCREF(type);
            }
            else {
                PyErr_SetString(PyExc_TypeError,
                    "raise: exception must be an old-style class or instance");
                goto raise_error;
            }
        #else
            type = (PyObject*) type->ob_type;
            Py_INCREF(type);
            if (!PyType_IsSubtype((PyTypeObject *)type, (PyTypeObject *)PyExc_BaseException)) {
                PyErr_SetString(PyExc_TypeError,
                    "raise: exception class must be a subclass of BaseException");
                goto raise_error;
            }
        #endif
    }
    PyErr_Restore(type, value, tb);
    return;
raise_error:
    Py_XDECREF(value);
    Py_XDECREF(type);
    Py_XDECREF(tb);
    return;
}

static PyObject *__Pyx_GetName(PyObject *dict, PyObject *name) {
    PyObject *result;
    result = PyObject_GetAttr(dict, name);
    if (!result)
        PyErr_SetObject(PyExc_NameError, name);
    return result;
}

static PyObject *__Pyx_GetItemInt(PyObject *o, Py_ssize_t i) {
    PyTypeObject *t = o->ob_type;
    PyObject *r;
    if (t->tp_as_sequence && t->tp_as_sequence->sq_item)
        r = PySequence_GetItem(o, i);
    else {
        PyObject *j = PyInt_FromLong(i);
        if (!j)
            return 0;
        r = PyObject_GetItem(o, j);
        Py_DECREF(j);
    }
    return r;
}

static int __Pyx_InternStrings(__Pyx_InternTabEntry *t) {
    while (t->p) {
        *t->p = PyString_InternFromString(t->s);
        if (!*t->p)
            return -1;
        ++t;
    }
    return 0;
}

static int __Pyx_InitStrings(__Pyx_StringTabEntry *t) {
    while (t->p) {
        *t->p = PyString_FromStringAndSize(t->s, t->n - 1);
        if (!*t->p)
            return -1;
        ++t;
    }
    return 0;
}

#include "compile.h"
#include "frameobject.h"
#include "traceback.h"

static void __Pyx_AddTraceback(char *funcname) {
    PyObject *py_srcfile = 0;
    PyObject *py_funcname = 0;
    PyObject *py_globals = 0;
    PyObject *empty_tuple = 0;
    PyObject *empty_string = 0;
    PyCodeObject *py_code = 0;
    PyFrameObject *py_frame = 0;
    
    py_srcfile = PyString_FromString(__pyx_filename);
    if (!py_srcfile) goto bad;
    py_funcname = PyString_FromString(funcname);
    if (!py_funcname) goto bad;
    py_globals = PyModule_GetDict(__pyx_m);
    if (!py_globals) goto bad;
    empty_tuple = PyTuple_New(0);
    if (!empty_tuple) goto bad;
    empty_string = PyString_FromString("");
    if (!empty_string) goto bad;
    py_code = PyCode_New(
        0,            /*int argcount,*/
        0,            /*int nlocals,*/
        0,            /*int stacksize,*/
        0,            /*int flags,*/
        empty_string, /*PyObject *code,*/
        empty_tuple,  /*PyObject *consts,*/
        empty_tuple,  /*PyObject *names,*/
        empty_tuple,  /*PyObject *varnames,*/
        empty_tuple,  /*PyObject *freevars,*/
        empty_tuple,  /*PyObject *cellvars,*/
        py_srcfile,   /*PyObject *filename,*/
        py_funcname,  /*PyObject *name,*/
        __pyx_lineno,   /*int firstlineno,*/
        empty_string  /*PyObject *lnotab*/
    );
    if (!py_code) goto bad;
    py_frame = PyFrame_New(
        PyThreadState_Get(), /*PyThreadState *tstate,*/
        py_code,             /*PyCodeObject *code,*/
        py_globals,          /*PyObject *globals,*/
        0                    /*PyObject *locals*/
    );
    if (!py_frame) goto bad;
    py_frame->f_lineno = __pyx_lineno;
    PyTraceBack_Here(py_frame);
bad:
    Py_XDECREF(py_srcfile);
    Py_XDECREF(py_funcname);
    Py_XDECREF(empty_tuple);
    Py_XDECREF(empty_string);
    Py_XDECREF(py_code);
    Py_XDECREF(py_frame);
}

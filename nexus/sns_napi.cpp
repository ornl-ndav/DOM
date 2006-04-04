// python
#include <Python.h>
// nexus
#include <napi.h>
// C++
#include <iostream>

// look in dv/danse/packages/nexus/module

static void NeXusFile_privateclose(void *file)
{
  NXhandle handle=static_cast<NXhandle>(file);
  NXclose(&handle);
  return;
}

static PyObject * NeXusFile_open(PyObject *, PyObject *args)
{
  // set default access method
  int access=NXACC_READ;
  char *filename;

  // get the arguments out
  if(!PyArg_ParseTuple(args,"s|i",&filename,&access))
    return NULL;

  std::cout << "open(" << filename << "," << access << ")" << std::endl;

  // open the file
  NXhandle handle;
  if(NXopen(filename,(NXaccess)access,&handle)!=NX_OK){
    PyErr_SetString(PyExc_IOError,"Could not open file");
    return NULL;
  }

  // convert the handle to python
  return PyCObject_FromVoidPtr(handle,NeXusFile_privateclose);
}
//NXmakegroup(handle,name,class) // NEEDS IMPLEMENTATION

//NXopengroup(handle,name,class) // NEEDS IMPLEMENTATION
static PyObject *NeXusFile_opengroup(PyObject *, PyObject *args)
{
  // get the arguments
  char *name;
  char *nxclass;
  PyObject *pyhandle;
  if(!PyArg_ParseTuple(args,"Oss",&pyhandle,&name,&nxclass))
    return NULL;
  NXhandle handle=static_cast<NXhandle>(PyCObject_AsVoidPtr(pyhandle));

  // do the work
  if(NXopengroup(handle,name,nxclass)!=NX_OK){
    PyErr_SetString(PyExc_IOError,"opengroup failed");
    return NULL;
  }

  Py_INCREF(Py_None);
  return Py_None;
}

//NXclosegroup(handle) // NEEDS IMPLEMENTATION
static PyObject *NeXusFile_closegroup(PyObject *, PyObject *args)
{
  // get the arguments
  PyObject *pyhandle;
  if(!PyArg_ParseTuple(args,"O",&pyhandle))
    return NULL;
  NXhandle handle=static_cast<NXhandle>(PyCObject_AsVoidPtr(pyhandle));

  // do the work
  if(NXclosegroup(handle)!=NX_OK){
    PyErr_SetString(PyExc_IOError,"closegroup failed");
    return NULL;
  }

  Py_INCREF(Py_None);
  return Py_None;
}

//NXopenpath(handle,path) // NEEDS IMPLEMENTATION

//NXopengrouppath(handle,path) // NEEDS IMPLEMENTATION

//NXmakedata(handle,name,type,rank,dimensions[]) // NEEDS IMPLEMENTATION

//NXcompmakedata(handle,name,type,rank,dimensions[],compression) // NEEDS IMPLEMENTATION

//NXopendata(handle,name) // NEEDS IMPLEMENTATION

//NXcompress(handle,compression) // NEEDS IMPLEMENTATION

//NXclosedata(handle) // NEEDS IMPLEMENTATION

//NXgetdata(handle,data) // NEEDS IMPLEMENTATION

//NXgetslab(handle,data,start[],size[]) // NEEDS IMPLEMENTATION

//NXgetattr(handle,name,value,length,type) // NEEDS IMPLEMENTATION

//NXputdata(handle,data) // NEEDS IMPLEMENTATION

//NXputslab(handle,data,start[],size[]) // NEEDS IMPLEMENTATION

//NXputattr(handle,name,value,length,type) // NEEDS IMPLEMENTATION

//NXflush(handle) // NEEDS IMPLEMENTATION

//NXgetinfo(handle,rank,dimension[],type) // NEEDS IMPLEMENTATION

//NXgetgroupinfo(handle,item_number,name,class) // NEEDS IMPLEMENTATION

//NXinitgroupdir(handle) // NEEDS IMPLEMENTATION

//NXgetnextenty(handle,name,class,type) // NEEDS IMPLEMENTATION

//NXgetattrinfo(handle,num_attrs) // NEEDS IMPLEMENTATION

//NXinitattrdir(handle) // NEEDS IMPLEMENTATION

//NXgetnextattr(handle,name,length,type) // NEEDS IMPLEMENTATION

//NXgetgroupID(handle,link_id) // NEEDS IMPLEMENTATION

//NXgetdataID(handle,link_id) // NEEDS IMPLEMENTATION

//NXmakelink(handle,link_id) // NEEDS IMPLEMENTATION

//NXmalloc(data,rank,dimesinos[],type) // NEEDS IMPLEMENTATION

//NXfree(data) // NEEDS IMPLEMENTATION

static PyMethodDef NeXusFile_methods[]={
  {"open",      (PyCFunction)NeXusFile_open, METH_VARARGS,
   "Open the file"},
  {"opengroup", (PyCFunction)NeXusFile_opengroup, METH_VARARGS,
   "Open the group specified by the name and class"},
  {"closegroup",(PyCFunction)NeXusFile_closegroup,METH_VARARGS,
   "Close the currently open group"},
  {NULL,NULL}
};

PyMODINIT_FUNC initsns_napi(void)
{
  // reference to the module
  PyObject *m;
  m=Py_InitModule3("sns_napi",NeXusFile_methods,"sns_napi, hacked in a couple of days");
  if(m==NULL)
    return;

  // get module dictionary for adding constants
  PyObject *d;
  d=PyModule_GetDict(m);

  // temporary variable for building constants
  PyObject *tmp;

  // add file access constants
  tmp=Py_BuildValue("i",NXACC_READ);
  PyDict_SetItemString(d,"ACC_READ",tmp);
  Py_DECREF(tmp);
  tmp=Py_BuildValue("i",NXACC_RDWR);
  PyDict_SetItemString(d,"ACC_RDWR",tmp);
  Py_DECREF(tmp);
  tmp=Py_BuildValue("i",NXACC_CREATE);
  PyDict_SetItemString(d,"ACC_CREATE",tmp);
  Py_DECREF(tmp);
  tmp=Py_BuildValue("i",NXACC_CREATE4);
  PyDict_SetItemString(d,"ACC_CREATE4",tmp);
  Py_DECREF(tmp);
  tmp=Py_BuildValue("i",NXACC_CREATE5);
  PyDict_SetItemString(d,"ACC_CREATE5",tmp);
  Py_DECREF(tmp);
  tmp=Py_BuildValue("i",NXACC_CREATEXML);
  PyDict_SetItemString(d,"ACC_CREATEXML",tmp);
  Py_DECREF(tmp);
  tmp=Py_BuildValue("i",NXACC_NOSTRIP);
  PyDict_SetItemString(d,"ACC_NOSTRIP",tmp);
  Py_DECREF(tmp);
}

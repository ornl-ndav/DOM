// python
#include <Python.h>
// nexus
#include <napi.h>
// C++
#include <iostream>

static int GROUP_STRING_LEN=80;

static void NeXusFile_privateclose(void *file)
{
  NXhandle handle=static_cast<NXhandle>(file);
  NXclose(&handle);
  return;
}

static PyObject * NeXusFile_convertscalar(void *value, int type, int index)
{
  PyObject * result=Py_None;
  if(type==NX_FLOAT32){
    result=PyFloat_FromDouble(static_cast<double>((static_cast<float*>(value))[index]));
  }else if(type==NX_FLOAT64){
    result=PyFloat_FromDouble(static_cast<double>((static_cast<double*>(value))[index]));
  }else if(type==NX_INT8){
    result=PyInt_FromLong(static_cast<long>((static_cast<unsigned char*>(value))[index]));
  }else if(type==NX_UINT8){
    result=PyInt_FromLong(static_cast<long>((static_cast<unsigned char*>(value))[index]));
  }else if(type==NX_INT16){
    result=PyInt_FromLong(static_cast<long>((static_cast<short int*>(value))[index]));
  }else if(type==NX_UINT16){
    result=PyInt_FromLong(static_cast<long>((static_cast<unsigned short*>(value))[index]));
  }else if(type==NX_INT32){
    result=PyInt_FromLong(static_cast<long>((static_cast<int*>(value))[index]));
  }else if(type==NX_UINT32){
    result=PyInt_FromLong(static_cast<long>((static_cast<unsigned int*>(value))[index]));
  }else{
    return NULL;
  }
  Py_INCREF(result);
  return result;
}

static PyObject * NeXusFile_convertobj(void * value,int type, int length)
{
  // for character arrays return a string
  if(type==NX_CHAR){
    PyObject * result=Py_None;
    result=Py_BuildValue("s",static_cast<char *>(value));
    Py_INCREF(result);
    return result;
  }

  // for everything else return a list
  PyObject * result=PyList_New(length);
  for( int i=0 ; i<length ; i++ )
    {
      PyObject *inner=NeXusFile_convertscalar(value,type,i);
      if(inner==NULL){
        PyErr_SetString(PyExc_RuntimeError,"Failure in convertscalar");
        return NULL;
      }
      PyList_SET_ITEM(result,i,inner);
    }
  Py_INCREF(result);
  return result;
}

//NXopen(filename,access)
static PyObject * NeXusFile_open(PyObject *, PyObject *args)
{
  // set default access method
  int access=NXACC_READ;
  char *filename;

  // get the arguments out
  if(!PyArg_ParseTuple(args,"s|i",&filename,&access))
    return NULL;

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
static PyObject *NeXusFile_makegroup(PyObject *, PyObject *args)
{
  PyErr_SetString(PyExc_NotImplementedError,"Writing is not implemented");
  return NULL;
}

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
static PyObject *NeXusFile_openpath(PyObject *, PyObject *args)
{
  // get the arguments
  char *path;
  PyObject *pyhandle;
  if(!PyArg_ParseTuple(args,"Os",&pyhandle,&path))
    return NULL;
  NXhandle handle=static_cast<NXhandle>(PyCObject_AsVoidPtr(pyhandle));

  // do the work
  if(NXopenpath(handle,path)!=NX_OK){
    PyErr_SetString(PyExc_IOError,"openpath failed");
    return NULL;
  }

  Py_INCREF(Py_None);
  return Py_None;
}

//NXopengrouppath(handle,path) // NEEDS IMPLEMENTATION
static PyObject *NeXusFile_opengrouppath(PyObject *, PyObject *args)
{
  // get the arguments
  char *path;
  PyObject *pyhandle;
  if(!PyArg_ParseTuple(args,"Os",&pyhandle,&path))
    return NULL;
  NXhandle handle=static_cast<NXhandle>(PyCObject_AsVoidPtr(pyhandle));

  // do the work
  if(NXopengrouppath(handle,path)!=NX_OK){
    PyErr_SetString(PyExc_IOError,"opengrouppath failed");
    return NULL;
  }

  Py_INCREF(Py_None);
  return Py_None;
}

//NXmakedata(handle,name,type,rank,dimensions[]) // NEEDS IMPLEMENTATION
static PyObject *NeXusFile_makedata(PyObject *, PyObject *args)
{
  PyErr_SetString(PyExc_NotImplementedError,"Writing is not implemented");
  return NULL;
}

//NXcompmakedata(handle,name,type,rank,dimensions[],compression) // NEEDS IMPLEMENTATION
static PyObject *NeXusFile_compmakedata(PyObject *, PyObject *args)
{
  PyErr_SetString(PyExc_NotImplementedError,"Writing is not implemented");
  return NULL;
}

//NXopendata(handle,name) // NEEDS IMPLEMENTATION
static PyObject *NeXusFile_opendata(PyObject *, PyObject *args)
{
  // get the arguments
  char *name;
  PyObject *pyhandle;
  if(!PyArg_ParseTuple(args,"Os",&pyhandle,&name))
    return NULL;
  NXhandle handle=static_cast<NXhandle>(PyCObject_AsVoidPtr(pyhandle));

  // do the work
  if(NXopendata(handle,name)!=NX_OK){
    PyErr_SetString(PyExc_IOError,"opendata failed");
    return NULL;
  }

  Py_INCREF(Py_None);
  return Py_None;
}

//NXcompress(handle,compression) // NEEDS IMPLEMENTATION
static PyObject *NeXusFile_compress(PyObject *, PyObject *args)
{
  PyErr_SetString(PyExc_NotImplementedError,"Writing is not implemented");
  return NULL;
}

//NXclosedata(handle) // NEEDS IMPLEMENTATION
static PyObject *NeXusFile_closedata(PyObject *, PyObject *args)
{
  // get the arguments
  PyObject *pyhandle;
  if(!PyArg_ParseTuple(args,"O",&pyhandle))
    return NULL;
  NXhandle handle=static_cast<NXhandle>(PyCObject_AsVoidPtr(pyhandle));

  // do the work
  if(NXclosedata(handle)!=NX_OK){
    PyErr_SetString(PyExc_IOError,"opendata failed");
    return NULL;
  }

  Py_INCREF(Py_None);
  return Py_None;
}

//NXgetdata(handle,data) // NEEDS IMPLEMENTATION
static PyObject *NeXusFile_getdata(PyObject *, PyObject *args)
{
  Py_INCREF(Py_None);
  return Py_None;
}

//NXgetslab(handle,data,start[],size[]) // NEEDS IMPLEMENTATION
static PyObject *NeXusFile_getslab(PyObject *, PyObject *args)
{
  Py_INCREF(Py_None);
  return Py_None;
}

//NXgetattr(handle,name,value,length,type) // NEEDS IMPLEMENTATION
static PyObject *NeXusFile_getattr(PyObject *, PyObject *args)
{
  // get the arguments
  char *name;
  PyObject *pyhandle;
  if(!PyArg_ParseTuple(args,"Os",&pyhandle,&name))
    return NULL;
  NXhandle handle=static_cast<NXhandle>(PyCObject_AsVoidPtr(pyhandle));

  // get ready to look for the attribute
  if(NXinitattrdir(handle)!=NX_OK){
    PyErr_SetString(PyExc_IOError,"In getattr: initattrdir failed");
    return NULL;
  }
  int num_attr;
  if(NXgetattrinfo(handle,&num_attr)!=NX_OK){
    PyErr_SetString(PyExc_IOError,"In getattr: getattrinfo failed");
    return NULL;
  }
  char attr_name[GROUP_STRING_LEN];
  int attr_type;
  int attr_len;

  // look for the attribute
  bool found=false;
  for( int i=0 ; i<num_attr ; i++ ){
    if(NXgetnextattr(handle,attr_name,&attr_len,&attr_type)!=NX_OK){
      PyErr_SetString(PyExc_IOError,"In getattr: getattrinfo failed");
      return NULL;
    }
    if(strcmp(name,attr_name)==0){
      found=true;
      break;
    }
  }

  // get the value
  int attr_dims[1]={attr_len+1};
  void *attr_value;
  if(NXmalloc(&attr_value,1,attr_dims,attr_type)!=NX_OK){
      PyErr_SetString(PyExc_IOError,"In getattr: malloc failed");
      return NULL;
  }
  if(NXgetattr(handle,attr_name,attr_value,attr_dims,&attr_type)!=NX_OK){
      PyErr_SetString(PyExc_IOError,"In getattr: getattr failed");
      return NULL;
  }
  PyObject *result=NeXusFile_convertobj(attr_value,attr_type,attr_len);
  if(NXfree(&attr_value)!=NX_OK){
      PyErr_SetString(PyExc_IOError,"In getattr: free failed");
      return NULL;
  }
  if((attr_type!=NX_CHAR)&&(attr_len==1)){
    PyObject *my_result=PyList_GetItem(result,0);
    Py_DECREF(result);
    result=my_result;
    Py_INCREF(result);
  }

  return result;
}

//NXputdata(handle,data) // NEEDS IMPLEMENTATION
static PyObject *NeXusFile_putdata(PyObject *, PyObject *args)
{
  PyErr_SetString(PyExc_NotImplementedError,"Writing is not implemented");
  return NULL;
}

//NXputslab(handle,data,start[],size[]) // NEEDS IMPLEMENTATION
static PyObject *NeXusFile_putslab(PyObject *, PyObject *args)
{
  PyErr_SetString(PyExc_NotImplementedError,"Writing is not implemented");
  return NULL;
}

//NXputattr(handle,name,value,length,type) // NEEDS IMPLEMENTATION
static PyObject *NeXusFile_putattr(PyObject *, PyObject *args)
{
  PyErr_SetString(PyExc_NotImplementedError,"Writing is not implemented");
  return NULL;
}

//NXflush(handle) // NEEDS IMPLEMENTATION
static PyObject *NeXusFile_flush(PyObject *, PyObject *args)
{
  Py_INCREF(Py_None);
  return Py_None;
}

//NXgetinfo(handle,rank,dimension[],type) // NEEDS IMPLEMENTATION
static PyObject *NeXusFile_getinfo(PyObject *, PyObject *args)
{
  Py_INCREF(Py_None);
  return Py_None;
}

//NXgetgroupinfo(handle,item_number,name,class) // NEEDS IMPLEMENTATION
static PyObject *NeXusFile_getgroupinfo(PyObject *, PyObject *args)
{
  Py_INCREF(Py_None);
  return Py_None;
}

//NXinitgroupdir(handle) // NEEDS IMPLEMENTATION
static PyObject *NeXusFile_initgroupdir(PyObject *, PyObject *args)
{
  Py_INCREF(Py_None);
  return Py_None;
}

//NXgetnextentry(handle,name,class,type) // NEEDS IMPLEMENTATION
static PyObject *NeXusFile_getnextentry(PyObject *, PyObject *args)
{
  Py_INCREF(Py_None);
  return Py_None;
}

//NXgetattrinfo(handle,num_attrs) // NEEDS IMPLEMENTATION
static PyObject *NeXusFile_getattrinfo(PyObject *, PyObject *args)
{
  Py_INCREF(Py_None);
  return Py_None;
}

//NXinitattrdir(handle) // NEEDS IMPLEMENTATION
static PyObject *NeXusFile_initattrdir(PyObject *, PyObject *args)
{
  Py_INCREF(Py_None);
  return Py_None;
}

//NXgetnextattr(handle,name,length,type) // NEEDS IMPLEMENTATION
static PyObject *NeXusFile_getnextattr(PyObject *, PyObject *args)
{
  Py_INCREF(Py_None);
  return Py_None;
}

//NXgetgroupID(handle,link_id) // NEEDS IMPLEMENTATION
static PyObject *NeXusFile_getgroupID(PyObject *, PyObject *args)
{
  Py_INCREF(Py_None);
  return Py_None;
}

//NXgetdataID(handle,link_id) // NEEDS IMPLEMENTATION
static PyObject *NeXusFile_getdataID(PyObject *, PyObject *args)
{
  Py_INCREF(Py_None);
  return Py_None;
}

//NXmakelink(handle,link_id) // NEEDS IMPLEMENTATION
static PyObject *NeXusFile_makelink(PyObject *, PyObject *args)
{
  PyErr_SetString(PyExc_NotImplementedError,"Writing is not implemented");
  return NULL;
}

//NXmalloc(data,rank,dimesinos[],type) // NEEDS IMPLEMENTATION
static PyObject *NeXusFile_malloc(PyObject *, PyObject *args)
{
  PyErr_SetString(PyExc_NotImplementedError,"Should be unnecessary");
  return NULL;
}

//NXfree(data) // NEEDS IMPLEMENTATION
static PyObject *NeXusFile_free(PyObject *, PyObject *args)
{
  PyErr_SetString(PyExc_NotImplementedError,"Should be unnecessary");
  return NULL;
}

static PyMethodDef NeXusFile_methods[]={
  {"open",         (PyCFunction)NeXusFile_open, METH_VARARGS,
   "Default access is read"},
  {"makegroup",    (PyCFunction)NeXusFile_makegroup, METH_VARARGS,
   ""},
  {"opengroup",    (PyCFunction)NeXusFile_opengroup, METH_VARARGS,
   ""},
  {"closegroup",   (PyCFunction)NeXusFile_closegroup,METH_VARARGS,
   ""},
  {"openpath",     (PyCFunction)NeXusFile_openpath, METH_VARARGS,
   ""},
  {"opengrouppath",(PyCFunction)NeXusFile_opengrouppath, METH_VARARGS,
   ""},
  {"makedata",     (PyCFunction)NeXusFile_makedata, METH_VARARGS,
   ""},
  {"compmakedata", (PyCFunction)NeXusFile_compmakedata, METH_VARARGS,
   ""},
  {"opendata",     (PyCFunction)NeXusFile_opendata, METH_VARARGS,
   ""},
  {"compress",     (PyCFunction)NeXusFile_compress, METH_VARARGS,
   ""},
  {"closedata",    (PyCFunction)NeXusFile_closedata, METH_VARARGS,
   ""},
  {"getdata",      (PyCFunction)NeXusFile_getdata, METH_VARARGS,
   ""},
  {"getslab",      (PyCFunction)NeXusFile_getslab, METH_VARARGS,
   ""},
  {"getattr",      (PyCFunction)NeXusFile_getattr, METH_VARARGS,
   ""},
  {"putdata",      (PyCFunction)NeXusFile_putdata, METH_VARARGS,
   ""},
  {"putslab",      (PyCFunction)NeXusFile_putslab, METH_VARARGS,
   ""},
  {"putattr",      (PyCFunction)NeXusFile_putattr, METH_VARARGS,
   ""},
  {"flush",        (PyCFunction)NeXusFile_flush, METH_VARARGS,
   ""},
  {"getinfo",      (PyCFunction)NeXusFile_getinfo, METH_VARARGS,
   ""},
  {"getgroupinfo", (PyCFunction)NeXusFile_getgroupinfo, METH_VARARGS,
   ""},
  {"initgroupdir", (PyCFunction)NeXusFile_initgroupdir, METH_VARARGS,
   ""},
  {"getnextentry", (PyCFunction)NeXusFile_getnextentry, METH_VARARGS,
   ""},
  {"getattrinfo",  (PyCFunction)NeXusFile_getattrinfo, METH_VARARGS,
   ""},
  {"initattrdir",  (PyCFunction)NeXusFile_initattrdir, METH_VARARGS,
   ""},
  {"getnextattr",  (PyCFunction)NeXusFile_getnextattr, METH_VARARGS,
   ""},
  {"getgroupID",   (PyCFunction)NeXusFile_getgroupID, METH_VARARGS,
   ""},
  {"getdataID",    (PyCFunction)NeXusFile_getdataID, METH_VARARGS,
   ""},
  {"makelink",     (PyCFunction)NeXusFile_makelink, METH_VARARGS,
   ""},
  {"malloc",       (PyCFunction)NeXusFile_malloc, METH_VARARGS,
   ""},
  {"free",         (PyCFunction)NeXusFile_free, METH_VARARGS,
   ""},
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

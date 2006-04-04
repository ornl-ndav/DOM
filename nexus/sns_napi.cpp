// python
#include <Python.h>
#include <structmember.h>
// nexus
#include <napi.h>
// C++
#include <iostream>

typedef struct{
  PyObject_HEAD
  NXhandle *handle;
  PyObject *filename;
}NeXusFile;

static int NeXusFile_init(NeXusFile *self, PyObject *args, PyObject *kwds)
{
  // set default access method
  int access=NXACC_READ;

  // get the arguments out
  if(!PyArg_ParseTuple(args,"S|i",&(self->filename),&access))
    return -1;
  Py_INCREF(self->filename);

  // open the file
  self->handle=new NXhandle;
  char *filename=PyString_AS_STRING(self->filename);
  if(NXopen(filename,(NXaccess)access,(self->handle))!=NX_OK){
    PyErr_SetString(PyExc_IOError,"Could not open file");
    delete (self->handle);
    Py_XDECREF(self->filename);
    return -1;
  }

  // return that things went well
  return 0;
}

static int NeXusFile_dealloc(NeXusFile *self)
{
  std::cerr << "deallocate" << std::endl;
  // assume this will work
  int result=0;

  // try to close the file
  if(NXclose((self->handle))!=NX_OK){
    PyErr_SetString(PyExc_IOError,"Could not close file");
    result=-1;
  }

  // delete the file handle and decrement the reference count of filename
  delete (self->handle);
  Py_XDECREF(self->filename);

  return result;
}

//NXmakegroup(handle,name,class) // NEEDS IMPLEMENTATION

//NXopengroup(handle,name,class) // NEEDS IMPLEMENTATION
static PyObject *NeXusFile_opengroup(NeXusFile *self, PyObject *args)
{
  // get the arguments
  char *name;
  char *nxclass;
  if(!PyArg_ParseTuple(args,"ss",&name,&nxclass))
    return NULL;

  std::cout << "***** " << name << " " << nxclass << " " << self->handle << std::endl;

  if(NXopengroup(&(self->handle),name,nxclass)!=NX_OK){
    std::cout << "bye there" << std::endl;
    PyErr_SetString(PyExc_IOError,"opengroup failed");
    return NULL;
  }
  std::cout << "hi there" << std::endl;

  Py_INCREF(Py_None);
  return Py_None;
}

//NXclosegroup(handle) // NEEDS IMPLEMENTATION

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

static PyMemberDef NeXusFile_members[]={
  {"filename",T_OBJECT_EX,offsetof(NeXusFile,filename),0,"filename"},
  {NULL,NULL},
};

static PyMethodDef NeXusFile_methods[]={
  {"opengroup", (PyCFunction)NeXusFile_opengroup, METH_VARARGS,
   "Open the group specified by the name and class"},
  {NULL,NULL}
};

static char NeXusFile_doc[] = "hi there.";

static PyTypeObject NeXusFileType={
  PyObject_HEAD_INIT(NULL)
  0,				/* ob_size        */
  "sns_napi.NeXusFile",		/* tp_name        */
  sizeof(NeXusFile),		/* tp_basicsize   */
  0,				/* tp_itemsize    */
  (destructor)NeXusFile_dealloc,/* tp_dealloc     */
  0,				/* tp_print       */
  0,				/* tp_getattr     */
  0,				/* tp_setattr     */
  0,				/* tp_compare     */
  0,				/* tp_repr        */
  0,				/* tp_as_number   */
  0,				/* tp_as_sequence */
  0,				/* tp_as_mapping  */
  0,				/* tp_hash        */
  0,				/* tp_call        */
  0,				/* tp_str         */
  0,				/* tp_getattro    */
  0,				/* tp_setattro    */
  0,				/* tp_as_buffer   */
  Py_TPFLAGS_DEFAULT,		/* tp_flags       */
  NeXusFile_doc,                /* tp_doc         */
  0,				/* tp_traverse       */
  0,				/* tp_clear          */
  0,				/* tp_richcompare    */
  0,				/* tp_weaklistoffset */
  0,				/* tp_iter           */
  0,				/* tp_iternext       */
  NeXusFile_methods,   		/* tp_methods        */
  NeXusFile_members,	        /* tp_members        */
  0,				/* tp_getset         */
  0,				/* tp_base           */
  0,				/* tp_dict           */
  0,				/* tp_descr_get      */
  0,				/* tp_descr_set      */
  0,				/* tp_dictoffset     */
  (initproc)NeXusFile_init,	/* tp_init           */
  0,                            /* tp_alloc          */
  0,                            /* tp_new            */
};

PyMODINIT_FUNC initsns_napi(void)
{
  // reference to the module
  PyObject *m;

  NeXusFileType.tp_new = PyType_GenericNew;
  if(PyType_Ready(&NeXusFileType)<0)
    return;

  m=Py_InitModule3("sns_napi",NULL,"sns_napi, hacked in a couple of days");
  if(m==NULL)
    return;

  Py_INCREF(&NeXusFileType);
  PyModule_AddObject(m,"NeXusFile",(PyObject *)&NeXusFileType);

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

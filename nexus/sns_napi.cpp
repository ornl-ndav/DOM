// python
#include <Python.h>
// nexus
#include <napi.h>
// C++
#include <iostream>

static int GROUP_STRING_LEN=80;
static PyObject *module;
static void NeXusFile_privateclose(void *file)
{
  NXhandle handle=static_cast<NXhandle>(file);
  NXclose(&handle);
  return;
}

static PyObject * NeXusFile_copysequence(PyObject *, PyObject *args)
{
  PyObject *source;
  PyObject *target;

  // Parse the objects
  if(!PyArg_ParseTuple(args,"OO",&source,&target))
    return NULL;

  // copy the values
  PyObject *item;
  int size=PySequence_Size(source);
  for( long i=0 ; i<size ; i++ ){
    item=PySequence_GetItem(source,i);
    PySequence_SetItem(target,i,item);
  }

  // return target
  Py_INCREF(target);
  return target;
}

static PyObject * NeXusFile_type_to_string(int type)
{
  if(type==NX_CHAR){
    return PyString_FromString("CHAR");
  }else if(type==NX_FLOAT32){
    return PyString_FromString("FLOAT32");
  }else if(type==NX_FLOAT64){
    return PyString_FromString("FLOAT64");
  }else if(type==NX_INT8){
    return PyString_FromString("INT8");
  }else if(type==NX_UINT8){
    return PyString_FromString("UINT8");
  }else if(type==NX_INT16){
    return PyString_FromString("INT16");
  }else if(type==NX_UINT16){
    return PyString_FromString("UINT16");
  }else if(type==NX_INT32){
    return PyString_FromString("INT32");
  }else if(type==NX_UINT8){
    return PyString_FromString("UINT32");
  }else{
    Py_INCREF(Py_None);
    return Py_None;
  }
}

static PyObject * NeXusFile_convertscalar(void *value, int type, long index)
{
  static PyObject * result=NULL;
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
  return result;
}

static PyObject * NeXusFile_convertobj(void * value,int type, long length,PyObject *result=Py_None)
{
  // for character arrays return a string
  if(type==NX_CHAR){
    Py_DECREF(result);
    result=Py_BuildValue("s",static_cast<char *>(value));
    Py_INCREF(result);
    return result;
  }

  bool use_abstract=true;
  if(result==Py_None){
    Py_DECREF(result);
    result=PyList_New(0); // new reference
    use_abstract=false;
  }

  /*
  // import nessi_list
  std::cout << "01:" << std::endl;
  PyObject *nessi_list_module;
  nessi_list_module=PyImport_AddModule("nessi_list");
  std::cout << "02:" << nessi_list_module << std::endl;
  if((nessi_list_module==NULL)||(nessi_list_module==Py_None))
    nessi_list_module=PyImport_ImportModule("nessi_list");
  std::cout << "03:" << nessi_list_module << std::endl;

  // get the NessiList object
  PyObject *nessi_list_class=PyObject_GetAttrString(nessi_list_module,
                                                  "NessiList");
  std::cout << "04:" << nessi_list_module << std::endl;
  // create a new instance
  PyObject *nessi_list_inst=PyInstance_New(nessi_list_class, Py_None, Py_None);
  Py_DECREF(nessi_list_inst);
  std::cout << "05:" << nessi_list_module << std::endl;
  */

  /*
  //Instance objects
  /PyObject * PyInstance_New(PyObject *class, PyObject *arg, PyObject *kw);
  */

  // fill the result
  PyObject *inner;
  for( long i=0 ; i<length ; i++ )
    {
      PyObject *inner=NeXusFile_convertscalar(value,type,i); // new reference
      if(inner==NULL){
        PyErr_SetString(PyExc_RuntimeError,"Failure in convertscalar");
        Py_DECREF(result);
        Py_XDECREF(inner);
        return NULL;
      }
      if(use_abstract){
        PyObject *status=PyObject_CallMethod(result,"append","(O)",inner); // new reference
        Py_DECREF(status);
        Py_DECREF(inner);
      }else{
        PyList_Append(result,inner);
        Py_DECREF(inner);
      }
    }
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

char * NeXusFile_makegroup_doc=
  "makegroup(handle,name,class)";

//NXmakegroup(handle,name,class) // NEEDS IMPLEMENTATION
static PyObject *NeXusFile_makegroup(PyObject *, PyObject *args)
{
  PyErr_SetString(PyExc_NotImplementedError,"Writing is not implemented");
  return NULL;
}

//NXopengroup(handle,name,class)
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

//NXclosegroup(handle)
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

//NXopenpath(handle,path)
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

//NXopengrouppath(handle,path) 
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

//NXopendata(handle,name)
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

//NXclosedata(handle)
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

//NXgetdata(handle,data)
static PyObject *NeXusFile_getdata(PyObject *, PyObject *args)
{
  // get the arguments
  PyObject *pyhandle;
  PyObject *pydata=Py_None;
  if(!PyArg_ParseTuple(args,"O|O",&pyhandle,&pydata))
    return NULL;
  Py_INCREF(pyhandle);
  Py_INCREF(pydata);

  NXhandle handle=static_cast<NXhandle>(PyCObject_AsVoidPtr(pyhandle));
  Py_DECREF(pyhandle);

  // find out about the data we are about to read
  int rank=0;
  int type=0;
  int dims[NX_MAXRANK];
  if(NXgetinfo(handle,&rank,dims,&type)!=NX_OK){
    PyErr_SetString(PyExc_IOError,"In getdata: getinfo failed");
    return NULL;
  }

  std::cout << "01:" << std::endl;
  sleep(5);

  //allocate memory for the data
  void *data;
  if(NXmalloc(&data,rank,dims,type)!=NX_OK){
    PyErr_SetString(PyExc_IOError,"In getdata: malloc failed");
    return NULL;
  }

  // get the data
  if(NXgetdata(handle,data)!=NX_OK){
    PyErr_SetString(PyExc_IOError,"In getdata: getdata failed");
    return NULL;
  }

  // calculate the total length of the data as a 1D array
  long tot_len=1;
  for( int i=0 ; i<rank ; i++ ){
    if(dims[i]>0)
      tot_len*=dims[i];
  }
  
  std::cout << "02:" << std::endl;
  sleep(5);

  // convert the data into a list
  PyObject *result=NeXusFile_convertobj(data,type,tot_len,pydata);

  // free up the allocated memory
  if(NXfree(&data)!=NX_OK){
    PyErr_SetString(PyExc_IOError,"In getdata: free failed");
    return NULL;
  }

  std::cout << "03:" << std::endl;
  sleep(5);

  // return the result
  return result;
}

static bool PyObject_to_intarray(PyObject *pyobj, int *array)
{
  int size=PySequence_Size(pyobj);
  for( int i=0 ; i<size ; i++ ){
    PyObject *item=PySequence_GetItem(pyobj,i);
    if(item==NULL){
      PyErr_SetString(PyExc_RuntimeError,
                  "conversion to array failed");
      return false;
    }
    array[i]=static_cast<int>(PyInt_AsLong(item));
  }

  return true;
}

//NXgetslab(handle,data,start[],size[])
static PyObject *NeXusFile_getslab(PyObject *, PyObject *args)
{
  // get the arguments
  PyObject *pyhandle;
  PyObject *pystart;
  PyObject *pysize;
  PyObject *pydata=Py_None;
  if(!PyArg_ParseTuple(args,"OOO|O",&pyhandle,&pystart,&pysize,&pydata))
    return NULL;
  Py_INCREF(pyhandle);
  Py_INCREF(pystart);
  Py_INCREF(pysize);
  Py_INCREF(pydata);

    // turn the arguments into something useful
  NXhandle handle=static_cast<NXhandle>(PyCObject_AsVoidPtr(pyhandle));
  Py_DECREF(pyhandle);
  int start[NX_MAXRANK];
  int size[NX_MAXRANK];
  if(!PyObject_to_intarray(pystart,start))
    return NULL;
  if(!PyObject_to_intarray(pysize,size))
    return NULL;
  Py_DECREF(pystart);
  Py_DECREF(pysize);

  // find out about the data we are about to read
  int rank=0;
  int type=0;
  int dims[NX_MAXRANK];
  if(NXgetinfo(handle,&rank,dims,&type)!=NX_OK){
    PyErr_SetString(PyExc_IOError,"In getslab: getinfo failed");
    return NULL;
  }

  //allocate memory for the data
  void *data;
  if(NXmalloc(&data,rank,size,type)!=NX_OK){
    PyErr_SetString(PyExc_IOError,"In getslab: malloc failed");
    NXfree(&data);
    return NULL;
  }

  // get the data
  if(NXgetslab(handle,data,start,size)!=NX_OK){
    PyErr_SetString(PyExc_IOError,"In getslab: getslab failed");
    NXfree(&data);
    return NULL;
  }

  // calculate the total length of the data as a 1D array
  long tot_len=1;
  for( int i=0 ; i<rank ; i++ ){
    if(size[i]>0)
      tot_len*=size[i];
  }
  
  // convert the data into a list
  PyObject *result=NeXusFile_convertobj(data,type,tot_len,pydata);

  // free up the allocated memory
  if(NXfree(&data)!=NX_OK){
    PyErr_SetString(PyExc_IOError,"In getslab: free failed");
    Py_XDECREF(result);
    return NULL;
  }

  // return the result
  return result;
}

//NXgetattr(handle,name,value,length,type)
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

//NXflush(handle)
static PyObject *NeXusFile_flush(PyObject *, PyObject *args)
{
  // get the arguments
  PyObject *pyhandle;
  if(!PyArg_ParseTuple(args,"O",&pyhandle))
    return NULL;
  NXhandle handle=static_cast<NXhandle>(PyCObject_AsVoidPtr(pyhandle));

  // find out about the data we are about to read
  if(NXflush(&handle)!=NX_OK){
    PyErr_SetString(PyExc_IOError,"flush failed");
    return NULL;
  }

  Py_INCREF(Py_None);
  return Py_None;
}

//NXgetinfo(handle,rank,dimension[],type) // NEEDS IMPLEMENTATION
static PyObject *NeXusFile_getinfo(PyObject *, PyObject *args)
{
  // get the arguments
  PyObject *pyhandle;
  if(!PyArg_ParseTuple(args,"O",&pyhandle))
    return NULL;
  NXhandle handle=static_cast<NXhandle>(PyCObject_AsVoidPtr(pyhandle));

  // find out about the data we are about to read
  int rank;
  int dims[NX_MAXRANK];
  int type;
  if(NXgetinfo(handle,&rank,dims,&type)!=NX_OK){
    PyErr_SetString(PyExc_IOError,"getinfo failed");
    return NULL;
  }

  // convert the dimensions to a tuple
  PyObject * pydims=PyTuple_New(rank);
  for( int i=0 ; i<rank ; i++ )
    PyTuple_SetItem(pydims,i,PyInt_FromLong(static_cast<long>(dims[i])));

  // convert the type to a string
  PyObject * pytype=NeXusFile_type_to_string(type);

  // return the result
  PyObject *result=Py_BuildValue("OO",pydims,pytype);
  Py_INCREF(result);
  return result;
}

//NXgetgroupinfo(handle,item_number,name,class) // NEEDS IMPLEMENTATION
static PyObject *NeXusFile_getgroupinfo(PyObject *, PyObject *args)
{
  Py_INCREF(Py_None);
  return Py_None;
}

//NXinitgroupdir(handle)
static PyObject *NeXusFile_initgroupdir(PyObject *, PyObject *args)
{
  // get the arguments
  PyObject *pyhandle;
  if(!PyArg_ParseTuple(args,"O",&pyhandle))
    return NULL;
  NXhandle handle=static_cast<NXhandle>(PyCObject_AsVoidPtr(pyhandle));

  // do the work
  if(NXinitgroupdir(handle)!=NX_OK){
    PyErr_SetString(PyExc_IOError,"initgroupdir failed");
    return NULL;
  }

  Py_INCREF(Py_None);
  return Py_None;
}

//NXgetnextentry(handle,name,class,type)
static PyObject *NeXusFile_getnextentry(PyObject *, PyObject *args)
{
  // get the arguments
  PyObject *pyhandle;
  if(!PyArg_ParseTuple(args,"O",&pyhandle))
    return NULL;
  NXhandle handle=static_cast<NXhandle>(PyCObject_AsVoidPtr(pyhandle));

  // do the work
  char name[GROUP_STRING_LEN];
  char nxclass[GROUP_STRING_LEN];
  int type;
  if(NXgetnextentry(handle,name,nxclass,&type)!=NX_OK){
    return Py_BuildValue("(OOi)",Py_None,Py_None,-1);
  }

  PyObject *result=PyTuple_New(3);
  PyTuple_SET_ITEM(result,0,PyString_FromString(name));
  PyTuple_SET_ITEM(result,1,PyString_FromString(nxclass));
  PyTuple_SET_ITEM(result,2,PyLong_FromLong(static_cast<long>(type)));

  Py_INCREF(result);
  return result;
}

//NXgetattrinfo(handle,num_attrs)
static PyObject *NeXusFile_getattrinfo(PyObject *, PyObject *args)
{
  // get the arguments
  PyObject *pyhandle;
  if(!PyArg_ParseTuple(args,"O",&pyhandle))
    return NULL;
  NXhandle handle=static_cast<NXhandle>(PyCObject_AsVoidPtr(pyhandle));

  // do the work
  int num_attr;
  if(NXgetattrinfo(handle,&num_attr)!=NX_OK){
    PyErr_SetString(PyExc_IOError,"getnumattr failed");
    return NULL;
  }

  PyObject *result=PyInt_FromLong(num_attr);
  Py_INCREF(result);
  return result;
}

//NXinitattrdir(handle)
static PyObject *NeXusFile_initattrdir(PyObject *, PyObject *args)
{
  // get the arguments
  PyObject *pyhandle;
  if(!PyArg_ParseTuple(args,"O",&pyhandle))
    return NULL;
  NXhandle handle=static_cast<NXhandle>(PyCObject_AsVoidPtr(pyhandle));

  // do the work
  if(NXinitattrdir(handle)!=NX_OK){
    PyErr_SetString(PyExc_IOError,"initattrdir failed");
    return NULL;
  }

  Py_INCREF(Py_None);
  return Py_None;
}

//NXgetnextattr(handle,name,length,type)
static PyObject *NeXusFile_getnextattr(PyObject *, PyObject *args)
{
  // get the arguments
  PyObject *pyhandle;
  if(!PyArg_ParseTuple(args,"O",&pyhandle))
    return NULL;
  NXhandle handle=static_cast<NXhandle>(PyCObject_AsVoidPtr(pyhandle));

  // get the information about the attribute
  char attr_name[GROUP_STRING_LEN];
  int attr_type;
  int attr_len;
  if(NXgetnextattr(handle,attr_name,&attr_len,&attr_type)!=NX_OK){
    return Py_BuildValue("(OO)",Py_None,Py_None);
  }
  PyObject *name=PyString_FromString(attr_name);
  Py_INCREF(name);

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
  PyObject *value=NeXusFile_convertobj(attr_value,attr_type,attr_len);
  if(NXfree(&attr_value)!=NX_OK){
      PyErr_SetString(PyExc_IOError,"In getattr: free failed");
      return NULL;
  }
  if((attr_type!=NX_CHAR)&&(attr_len==1)){
    PyObject *my_value=PyList_GetItem(value,0);
    Py_DECREF(value);
    value=my_value;
    Py_INCREF(value);
  }

  PyObject *result=PyTuple_New(2);
  PyTuple_SET_ITEM(result,0,name);
  PyTuple_SET_ITEM(result,1,value);
  Py_INCREF(result);
  return result;
}

static void NeXusFile_destroylink(void *link)
{
  NXlink *napilink=static_cast<NXlink *>(link);
  delete napilink;
  return;
}

//NXgetgroupID(handle,link_id) // NEEDS IMPLEMENTATION
static PyObject *NeXusFile_getgroupID(PyObject *, PyObject *args)
{
  // get the arguments
  PyObject *pyhandle;
  if(!PyArg_ParseTuple(args,"O",&pyhandle))
    return NULL;
  NXhandle handle=static_cast<NXhandle>(PyCObject_AsVoidPtr(pyhandle));

  // get the information about the attribute
  NXlink *link=new NXlink;
  if(NXgetgroupID(handle,link)!=NX_OK){
    PyErr_SetString(PyExc_IOError,"getgroupID failed");
    return NULL;
  }

  // convert the link to python
  return PyCObject_FromVoidPtr(link,NeXusFile_destroylink);
}

//NXgetdataID(handle,link_id) // NEEDS IMPLEMENTATION
static PyObject *NeXusFile_getdataID(PyObject *, PyObject *args)
{
  // get the arguments
  PyObject *pyhandle;
  if(!PyArg_ParseTuple(args,"O",&pyhandle))
    return NULL;
  NXhandle handle=static_cast<NXhandle>(PyCObject_AsVoidPtr(pyhandle));

  // get the information about the attribute
  NXlink *link=new NXlink;
  if(NXgetdataID(handle,link)!=NX_OK){
    PyErr_SetString(PyExc_IOError,"getdataID failed");
    return NULL;
  }

  // convert the link to python
  return PyCObject_FromVoidPtr(link,NeXusFile_destroylink);
}

//NXmakelink(handle,link_id) // NEEDS IMPLEMENTATION
static PyObject *NeXusFile_makelink(PyObject *, PyObject *args)
{
  PyErr_SetString(PyExc_NotImplementedError,"Writing is not implemented");
  return NULL;
}

static PyMethodDef NeXusFile_methods[]={
  {"open",         (PyCFunction)NeXusFile_open, METH_VARARGS,
   "Default access is read"},
  {"makegroup",    (PyCFunction)NeXusFile_makegroup, METH_VARARGS,
   NeXusFile_makegroup_doc},
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
  {"getnumattr",   (PyCFunction)NeXusFile_getattrinfo, METH_VARARGS,
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
  {"copysequence", (PyCFunction)NeXusFile_copysequence, METH_VARARGS,
   "copysequence(source,target) - the target must already be sized properly"},
  {NULL,NULL}
};

PyMODINIT_FUNC initsns_napi(void)
{
  // reference to the module
  module=Py_InitModule3("sns_napi",NeXusFile_methods,
                        "sns_napi, hacked in a couple of days");
  if(module==NULL)
    return;

  // get module dictionary for adding constants
  PyObject *d;
  d=PyModule_GetDict(module);

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

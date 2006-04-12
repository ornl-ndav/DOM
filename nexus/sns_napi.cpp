// python
#include <Python.h>
// nexus
#include <napi.h>
// C++
#include <iostream>
// NessiVector
#include <vector>
#include <stdexcept>
#include <string>

enum res_type {FLOAT,INT,PYTHON};

static int GROUP_STRING_LEN=80;
static PyObject *module;
static void NeXusFile_privateclose(void *file)
{
  NXhandle handle=static_cast<NXhandle>(file);
  NXclose(&handle);
  return;
}

/*
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
*/

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

static int NeXusFile_convertscalar2int(void *value, int type, long index)
{
  if(type==NX_FLOAT32){
    return static_cast<int>((static_cast<float*>(value))[index]);
  }else if(type==NX_FLOAT64){
    return static_cast<int>((static_cast<double*>(value))[index]);
  }else if(type==NX_INT8){
    return static_cast<int>((static_cast<unsigned char*>(value))[index]);
  }else if(type==NX_UINT8){
    return static_cast<int>((static_cast<unsigned char*>(value))[index]);
  }else if(type==NX_INT16){
    return static_cast<int>((static_cast<short int*>(value))[index]);
  }else if(type==NX_UINT16){
    return static_cast<int>((static_cast<unsigned short*>(value))[index]);
  }else if(type==NX_INT32){
    return static_cast<int>((static_cast<int*>(value))[index]);
  }else if(type==NX_UINT32){
    return static_cast<int>((static_cast<unsigned int*>(value))[index]);
  }
  throw std::invalid_argument("Do not understand type");
}

static double NeXusFile_convertscalar2double(void *value, int type, long index)
{
  if(type==NX_FLOAT32){
    return static_cast<double>((static_cast<float*>(value))[index]);
  }else if(type==NX_FLOAT64){
    return static_cast<double>((static_cast<double*>(value))[index]);
  }else if(type==NX_INT8){
    return static_cast<double>((static_cast<unsigned char*>(value))[index]);
  }else if(type==NX_UINT8){
    return static_cast<double>((static_cast<unsigned char*>(value))[index]);
  }else if(type==NX_INT16){
    return static_cast<double>((static_cast<short int*>(value))[index]);
  }else if(type==NX_UINT16){
    return static_cast<double>((static_cast<unsigned short*>(value))[index]);
  }else if(type==NX_INT32){
    return static_cast<double>((static_cast<int*>(value))[index]);
  }else if(type==NX_UINT32){
    return static_cast<double>((static_cast<unsigned int*>(value))[index]);
  }
  throw std::invalid_argument("Do not understand type");
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

static PyObject * NeXusFile_convertobj2(void *value,int type, long length,res_type result_type){
  if(result_type==FLOAT){
    std::vector<double> *result=new std::vector<double>();
    for( int i=0 ; i<length ; i++ )
      result->push_back(NeXusFile_convertscalar2double(value,type,i));
    PyObject *pyresult=PyCObject_FromVoidPtr(result,NULL);
    return pyresult;
  }else{
    std::vector<int> *result=new std::vector<int>();
    for( int i=0 ; i<length ; i++ )
      result->push_back(NeXusFile_convertscalar2int(value,type,i));
    PyObject *pyresult=PyCObject_FromVoidPtr(result,NULL);
    return pyresult;
  }
}

static PyObject * NeXusFile_convertobj(void * value,int type, long length,res_type result_type=PYTHON)
{
  PyObject *result;
  // for character arrays return a string
  if(type==NX_CHAR){
    result=Py_BuildValue("s",static_cast<char *>(value));
    Py_INCREF(result);
    return result;
  }

  // for scalars return python primatives
  if(length==0){
    Py_INCREF(Py_None);
    return Py_None;
  }
  if(length==1){
    result=NeXusFile_convertscalar(value,type,0);
    return result;
  }

  if(result_type==PYTHON){
    result=PyList_New(0); // new reference

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
        PyList_Append(result,inner);
        Py_DECREF(inner);
      }
  }

  return NeXusFile_convertobj2(value,type,length,result_type);
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

static res_type get_res_type(PyObject *pytype){
  if(pytype==NULL || pytype==Py_None)
    return FLOAT;

  PyObject *str_pytype=PyObject_Str(pytype);


  std::string float_type("f");
  std::string int_type("i");
  std::string python_type("p");
  /*  PyObject *float_type=PyString_FromString("f");
  PyObject *int_type=PyString_FromString("i");
  PyObject *python_type=PyString_FromString("p");
  */

  char *cctype=PyString_AsString(pytype);
  std::string ctype(cctype);

  if(float_type==ctype)
    return FLOAT;
  if(int_type==ctype)
    return INT;
  if(python_type==ctype)
    return PYTHON;

  throw std::invalid_argument("Do not understand type");
}

char * NeXusFile_getdata_doc=
  "getdata(handle,type='f')";

//NXgetdata(handle,data)
static PyObject *NeXusFile_getdata(PyObject *, PyObject *args)
{
  // get the arguments
  PyObject *pyhandle;
  PyObject *pytype=Py_None;
  if(!PyArg_ParseTuple(args,"O|O",&pyhandle,&pytype))
    return NULL;

  NXhandle handle=static_cast<NXhandle>(PyCObject_AsVoidPtr(pyhandle));
  res_type result_type=get_res_type(pytype);

  // find out about the data we are about to read
  int rank=0;
  int type=0;
  int dims[NX_MAXRANK];
  if(NXgetinfo(handle,&rank,dims,&type)!=NX_OK){
    PyErr_SetString(PyExc_IOError,"In getdata: getinfo failed");
    return NULL;
  }

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
  
  // convert the data into a list
  PyObject *result=NeXusFile_convertobj(data,type,tot_len,result_type);

  // free up the allocated memory
  if(NXfree(&data)!=NX_OK){
    PyErr_SetString(PyExc_IOError,"In getdata: free failed");
    return NULL;
  }

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

char * NeXusFile_getslab_doc=
  "getslab(handle,start,size,type='f')";

//NXgetslab(handle,data,start[],size[])
static PyObject *NeXusFile_getslab(PyObject *, PyObject *args)
{
  // get the arguments
  PyObject *pyhandle;
  PyObject *pystart;
  PyObject *pysize;
  PyObject *pytype=Py_None;
  if(!PyArg_ParseTuple(args,"OOO|O",&pyhandle,&pystart,&pysize,&pytype))
    return NULL;
  res_type result_type=get_res_type(pytype);

    // turn the arguments into something useful
  NXhandle handle=static_cast<NXhandle>(PyCObject_AsVoidPtr(pyhandle));
  int start[NX_MAXRANK];
  int size[NX_MAXRANK];
  if(!PyObject_to_intarray(pystart,start))
    return NULL;
  if(!PyObject_to_intarray(pysize,size))
    return NULL;

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
  PyObject *result=NeXusFile_convertobj(data,type,tot_len,result_type);

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

  if(!found){
    PyErr_SetString(PyExc_RuntimeError,"Could not find attribute");
    return NULL;
  }

  // get the value
  int attr_dims[]={attr_len+1};
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
   NeXusFile_getdata_doc},
  {"getslab",      (PyCFunction)NeXusFile_getslab, METH_VARARGS,
   NeXusFile_getslab_doc},
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
  /*
  {"copysequence", (PyCFunction)NeXusFile_copysequence, METH_VARARGS,
   "copysequence(source,target) - the target must already be sized properly"},
  */
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

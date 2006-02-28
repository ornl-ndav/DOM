import nxpython
import enum

class NeXusError(SystemError):
    pass

class NeXusFile:
    # numeric types
    SDS_TYPES=enum.Enum()
    SDS_TYPES.set("CHAR",   nxpython.NX_CHAR)
    SDS_TYPES.set("INT8",   nxpython.NX_INT8)
    SDS_TYPES.set("INT16",  nxpython.NX_INT16)
    SDS_TYPES.set("INT32",  nxpython.NX_INT32)
    SDS_TYPES.set("UINT8",  nxpython.NX_UINT8)
    SDS_TYPES.set("UINT16", nxpython.NX_UINT16)
    SDS_TYPES.set("UINT32", nxpython.NX_UINT32)
    SDS_TYPES.set("FLOAT32",nxpython.NX_FLOAT32)
    SDS_TYPES.set("FLOAT64",nxpython.NX_FLOAT64)

    # access methods
    ACCESS=enum.Enum()
    ACCESS.set("READ",     nxpython.NXACC_READ)
    ACCESS.set("RDWR",     nxpython.NXACC_RDWR)
    ACCESS.set("CREATE",   nxpython.NXACC_CREATE)
    ACCESS.set("CREATE4",  nxpython.NXACC_CREATE4)
    ACCESS.set("CREATE5",  nxpython.NXACC_CREATE5)
    ACCESS.set("CREATEXML",6)   # nxpython.NXACC_CREATEXML)
    ACCESS.set("NOSTRIP",  128) # nxpython.NXACC_NOSTRIP)

    # status reports from functions
    STATUS=enum.Enum()
    STATUS.set("OK",   1)
    STATUS.set("ERROR",0)
    STATUS.set("EOD",  -1)

    # compression algorithms to use
    COMPRESS=enum.Enum()
    COMPRESS.set("NONE",100) # nxpython.NX_COMP_NONE)
    COMPRESS.set("LZW", 200) # nxpython.NX_COMP_LZW)
    COMPRESS.set("RLE", 300) # nxpython.NX_COMP_RLE)
    COMPRESS.set("HUF", 400) # nxpython.NX_COMP_HUF)

    # ----- python stuff
    def __init__(self,filename,access=nxpython.NXACC_READ):
        self.__HANDLE__=nxpython.nx_open(filename,access)
        if(self.__HANDLE__==None):
            raise SystemError,"Failed to read file: %s" % filename
        self.__filename    = filename
        self.__group_level = 0
        self.__in_data     = False

    def __del__(self):
        self.close()

    def filename(self):
        return self.__filename

    # ----- napi stuff
    def close(self): 
        if(self.__HANDLE__!=None):
            nxpython.nx_close(self.__HANDLE__)
            self.__HANDLE__=None

    def flush(self):
        nxpython.nx_flush(self.__HANDLE__)

    def makegroup(self,name,type):
        result=nxpython.nx_makegroup(self.__HANDLE__,name,type)
        if(result!=self.STATUS.OK):
            raise NeXusError,"makegroup(%s,%s) FAILED[%d]" % (name,type,result)

    def opengroup(self,name,type):
        result=nxpython.nx_opengroup(self.__HANDLE__,name,type)
        if(result!=self.STATUS.OK):
            raise NeXusError,"opengroup(%s,%s) FAILED[%d]" % (name,type,result)

    def openpath(self,path):
        result=nxpython.nx_openpath(self.__HANDLE__,path)
        if(result!=self.STATUS.OK):
            raise NeXusError,"openpath(%s) FAILED[%d]" % (path,result)
        
    def opengrouppath(self,path):
        result=nxpython.nx_opengrouppath(self.__HANDLE__,path)
        if(result!=self.STATUS.OK):
            raise NeXusError,"opengrouppath(%s) FAILED[%d]" % (path,result)
        
    def closegroup(self):
        result=nxpython.nx_closegroup(self.__HANDLE__)
        if(result!=self.STATUS.OK):
            raise NeXusError,"closegroup() FAILED[%d]" % (result)

    def makedata(self,name,type,dims):
        # convert the information to c-natives
        (rank,c_dims)=self.dims_to_cdims(dims)
        # create the data
        result=nxpython.nx_makedata(self.__HANDLE__,name,rank,type,c_dims)
        #cleanup
        self.delete_sds(c_dims)
        #return the result
        if(result!=self.STATUS.OK):
            raise NeXusError,"makedata(%s,%d,%s) FAILED[%d]" % (name,type,str(dims),result)

    def compmakedata(self,name,type,dims,c_buffer):
        raise NotImplementedError

#    def compress(self): # not exposed through swig
#        raise NotImplementedError

    def opendata(self,name):
        result=nxpython.nx_opendata(self.__HANDLE__,name)
        if(result!=self.STATUS.OK):
            raise NeXusError,"opendata(%s) FAILED[%d]" % (name,result)

    def closedata(self):
        result=nxpython.nx_closedata(self.__HANDLE__)
        if(result!=self.STATUS.OK):
            raise NeXusError,"closedata() FAILED[%d]" % (result)

    def putdata(self,c_ptr):
        result=nxpython.nx_putdata(self.__HANDLE__,c_ptr)
        if(result!=self.STATUS.OK):
            raise NeXusError,"putdata() FAILED[%d]" % (result)

    def putslab(self,c_ptr,dims):
        (rank,c_dims)=self.dims_to_cdims(dims)
        result=nxpython.nx_putslab(self.__HANDLE__,c_ptr,c_dims)
        self.delete_sds(c_dims)
        if(result!=self.STATUS.OK):
            raise NeXusError,"putslab() FAILED[%d]" % (result)

    def getdata(self):
        result=nxpython.nx_getdata(self.__HANDLE__)
        if(result==None):
            raise NeXusError,"getdata() FAILED"
        return result

    def getslab(self,dims,size):
        # convert the information to c-natives
        (rank,c_size)=dims_to_cdims(size)
        (rank,c_dims)=dims_to_cdims(dims)
        # get the data
        result=nxpython.nx_get_slab(self.__HANDLE__,c_dims,c_size)
        # cleanup
        self.delete_sds(c_dims)
        self.delete_sds(c_size)
        #return the result
        if(result==None):
            raise NeXusError,"getslab() FAILED"
        return result

    def putattr(self,name,c_ptr):
        result=nxpython.nx_putattr(self.__HANDLE__,name,c_ptr)
        if(result!=self.STATUS.OK):
            raise NeXusError,"putattr(%s,c_ptr) FAILED[%d]" % (name)

    def getdataID(self):
        result=nxpython.nx_getdataID(self.__HANDLE__)
        if(result!=self.STATUS.OK):
            raise NeXusError,"getdataID() FAILED[%d]"

    def makelink(self,link):
        result=nxpython.nx_makelink(self.__HANDLE__,link)
        if(result!=self.STATUS.OK):
            raise NeXusError,"makelink() FAILED[%d]"

    def opensourcegroup(self):
        result=nxpython.nx_opensourcegroup(self.__HANDLE__)
        if(result!=self.STATUS.OK):
            raise NeXusError,"opensourcegroup() FAILED[%d]"

    def getinfo(self):
        # getinfo
        info=nxpython.nx_getinfo(self.__HANDLE__)
        # create exception if this doesn't make sense
        if(info==None):
            raise NeXusError,"getinfo() FAILED"
        type=self.get_sds_type(info)
        # get the dimensions
        rank=self.get_sds_rank(info)
        rank=(self.get_sds_dim(rank,info))[0]
        dims=[]
        for i in range(rank):
            dims.append(self.get_sds_value(info,self.SDS_TYPES.INT32,i))
        dims=dims[2:]

        # return the result
        return (type,dims)

    def getnextentry(self):
        SEPARATOR=":"
        info=nxpython.nx_getnextentry(self.__HANDLE__,SEPARATOR)
        if(info==None):
            return (None,None)
        result=info.split(SEPARATOR)
        try:
            result.index("CDF0.0")
            return (result[0],"CDF0.0")
        except ValueError:
            (name,type,number)=result
            return (name,type)

    def getnextattr(self):
        SEPARATOR=":"
        # find out about the attribute
        info=nxpython.nx_getnextattr(self.__HANDLE__,SEPARATOR)
        if(info==None):
            return (None,None)
        (name,length,type)=info.split(SEPARATOR)
        type=self.SDS_TYPES.key(int(type))

        return (name,self.getattr(name,type,length))

    def getattr(self,name,type,length):
        i_type=self.SDS_TYPES.val(type)
        i_length=int(length)
        value=nxpython.nx_getattr(self.__HANDLE__,name,i_type,i_length)
        if(value==None):
            raise NeXusError,"getattr(%s,%s,%d) FAILED" % (name,type,length)
        if(i_type==self.SDS_TYPES.CHAR):
            return nxpython.get_nxds_text(value)

        result=[]
        for i in range(i_length):
            result.append(self.get_sds_value(value,type,i))
        if len(result)==1:
            result=result[0]
        return result

    def getgroupID(self):
        result=nxpython.nx_getgroupID(self.__HANDLE__)
        if(result!=self.STATUS.OK):
            raise NeXusError,"getgroupID() FAILED[%d]"

#    def sameID(self): # not exposed through swig
#        raise NotImplementedError

    def initgroupdir(self):
        result=nxpython.nx_initgroupdir(self.__HANDLE__)
        if(result!=self.STATUS.OK):
            raise NeXusError,"initgroupdir() FAILED[%d]" % result

    def initattrdir(self):
        result=nxpython.nx_initattrdir(self.__HANDLE__)
        if(result!=self.STATUS.OK):
            raise NeXusError,"initattrdir() FAILED[%d]" % result

#    def setnumberformat(self): # not exposed through swig
#        raise NotImplementedError

##### These two functions appear in napi.h, but should NEVER be
##### brought into the python layer
#extern  NXstatus  NXmalloc(void** data, int rank, int dimensions[], int datatype);
#extern  NXstatus  NXfree(void** data);

    # ----- nxdataset.i (c <-> python) stuff
    def create_sds(self,type,dims):
        args=[type]
        try:
            args.extend(dims)
        except TypeError:
            args.append(dims)
        return apply(nxpython.create_nxds,args)

    def create_text_sds(self,value):
        return nxpython.create_text_nxds(value)

    def delete_sds(self,c_ptr):
        nxpython.drop_nxds(c_ptr)

    def get_sds_rank(self,c_ptr):
        return nxpython.get_nxds_rank(c_ptr)

    def get_sds_type(self,c_ptr):
        type=nxpython.get_nxds_type(c_ptr)
        return self.SDS_TYPES.key(type)

    def get_sds_dim(self,rank,c_ptr):
        result=[]
        for i in range(rank):
            result.append(nxpython.get_nxds_dim(c_ptr,i))
        return result

    def get_sds_value(self,c_ptr,type,index):
        args=[c_ptr]
        try:
            args.extend(index)
        except TypeError:
            args.append(index)
        value=apply(nxpython.get_nxds_value,args)
        if(type==self.SDS_TYPES.FLOAT32 or type==self.SDS_TYPES.FLOAT64):
            return value
        else:
            return int(value)

    def get_sds_text(self,c_ptr):
        return nxpython.get_nxds_text(c_ptr)

    def put_sds_value(self,c_ptr,value,index):
        args=[c_ptr,value]
        try:
            args.extend(index)
        except TypeError:
            args.append(index)
        result=apply(nxpython.put_nxds_value,args)
        if result!=self.STATUS.OK:
            raise NeXusError,"put_sds_value(?,%s,%s) FAILED[%d]" % (str(value),str(index))

    # ----- utility functions
    def dims_to_cdims(self,dims):
        """The result of this needs to be freed using delete_sds(self,c_ptr)"""
        # convert the information to c-natives
        rank=len(dims)
        c_dims=self.create_sds(self.SDS_TYPES.INT8,rank)
        for (it,pos) in map(None,dims,range(rank)):
            self.put_sds_value(c_dims,it,pos)
        # return the void pointer
        return (rank,c_dims)

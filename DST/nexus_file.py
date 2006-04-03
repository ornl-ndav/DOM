import nexus
import enum

class NeXusError(SystemError):
    pass

class NeXusFile:
    # numeric types
    SDS_TYPES=enum.Enum()
    SDS_TYPES.set("CHAR",   nexus.NX_CHAR)
    SDS_TYPES.set("INT8",   nexus.NX_INT8)
    SDS_TYPES.set("INT16",  nexus.NX_INT16)
    SDS_TYPES.set("INT32",  nexus.NX_INT32)
    SDS_TYPES.set("UINT8",  nexus.NX_UINT8)
    SDS_TYPES.set("UINT16", nexus.NX_UINT16)
    SDS_TYPES.set("UINT32", nexus.NX_UINT32)
    SDS_TYPES.set("FLOAT32",nexus.NX_FLOAT32)
    SDS_TYPES.set("FLOAT64",nexus.NX_FLOAT64)

    # access methods
    ACCESS=enum.Enum()
    ACCESS.set("READ",     nexus.NXACC_READ)
    ACCESS.set("RDWR",     nexus.NXACC_RDWR)
    ACCESS.set("CREATE",   nexus.NXACC_CREATE)
    ACCESS.set("CREATE4",  nexus.NXACC_CREATE4)
    ACCESS.set("CREATE5",  nexus.NXACC_CREATE5)
    ACCESS.set("CREATEXML",6)   # nexus.NXACC_CREATEXML)
    ACCESS.set("NOSTRIP",  128) # nexus.NXACC_NOSTRIP)

    # status reports from functions
    STATUS=enum.Enum()
    STATUS.set("OK",   1)
    STATUS.set("ERROR",0)
    STATUS.set("EOD",  -1)

    # compression algorithms to use
    COMPRESS=enum.Enum()
    COMPRESS.set("NONE",100) # nexus.NX_COMP_NONE)
    COMPRESS.set("LZW", 200) # nexus.NX_COMP_LZW)
    COMPRESS.set("RLE", 300) # nexus.NX_COMP_RLE)
    COMPRESS.set("HUF", 400) # nexus.NX_COMP_HUF)

    # ----- python stuff
    def __init__(self,filename,access=nexus.NXACC_READ):
        status,self.__HANDLE__=nexus.NXopen(filename,access)
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
            nexus.NXclose(self.__HANDLE__)
            self.__HANDLE__=None

    def flush(self):
        nexus.NXflush(self.__HANDLE__)

    def makegroup(self,name,type):
        result=nexus.NXmakegroup(self.__HANDLE__,name,type)
        if(result!=self.STATUS.OK):
            raise NeXusError,"makegroup(%s,%s) FAILED[%d]" % (name,type,result)

    def opengroup(self,name,type):
        result=nexus.NXopengroup(self.__HANDLE__,name,type)
        if(result!=self.STATUS.OK):
            raise NeXusError,"opengroup(%s,%s) FAILED[%d]" % (name,type,result)

    def openpath(self,path):
        result=nexus.NXopenpath(self.__HANDLE__,path)
        if(result!=self.STATUS.OK):
            raise NeXusError,"openpath(%s) FAILED[%d]" % (path,result)
        
    def opengrouppath(self,path):
        result=nexus.NXopengrouppath(self.__HANDLE__,path)
        if(result!=self.STATUS.OK):
            raise NeXusError,"opengrouppath(%s) FAILED[%d]" % (path,result)
        
    def closegroup(self):
        result=nexus.NXclosegroup(self.__HANDLE__)
        if(result!=self.STATUS.OK):
            raise NeXusError,"closegroup() FAILED[%d]" % (result)

    def makedata(self,name,type,dims):
        # convert the information to c-natives
        (rank,c_dims)=self.dims_to_cdims(dims)
        # create the data
        result=nexus.NXmakedata(self.__HANDLE__,name,rank,type,c_dims)
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
        result=nexus.NXopendata(self.__HANDLE__,name)
        if(result!=self.STATUS.OK):
            raise NeXusError,"opendata(%s) FAILED[%d]" % (name,result)

    def closedata(self):
        result=nexus.NXclosedata(self.__HANDLE__)
        if(result!=self.STATUS.OK):
            raise NeXusError,"closedata() FAILED[%d]" % (result)

    def putdata(self,c_ptr):
        result=nexus.NXputdata(self.__HANDLE__,c_ptr)
        if(result!=self.STATUS.OK):
            raise NeXusError,"putdata() FAILED[%d]" % (result)

    def putslab(self,c_ptr,dims):
        (rank,c_dims)=self.dims_to_cdims(dims)
        result=nexus.NXputslab(self.__HANDLE__,c_ptr,c_dims)
        self.delete_sds(c_dims)
        if(result!=self.STATUS.OK):
            raise NeXusError,"putslab() FAILED[%d]" % (result)

    def getdata(self):
        status,result=nexus.NXgetdata(self.__HANDLE__)
        if(result==None):
            raise NeXusError,"getdata() FAILED"
        return result

    def getslab(self,dims,size):
        print "00:NeXusFile.getslab(",dims,",",size,")"
        status,result=nexus.NXgetslab(self.__HANDLE__,dims,size)
        if(result==None):
            raise NeXusError,"getslab() FAILED"
        return result

    def putattr(self,name,c_ptr,type):
        result=nexus.NXputattr(self.__HANDLE__,name,c_ptr,type)
        if(result!=self.STATUS.OK):
            raise NeXusError,"putattr(%s,c_ptr) FAILED[%d]" % (name)

    def getdataID(self):
        result=nexus.NXgetdataID(self.__HANDLE__)
        if(result!=self.STATUS.OK):
            raise NeXusError,"getdataID() FAILED[%d]"

    def makelink(self,link):
        result=nexus.NXmakelink(self.__HANDLE__,link)
        if(result!=self.STATUS.OK):
            raise NeXusError,"makelink() FAILED[%d]"

    def opensourcegroup(self):
        result=nexus.NXopensourcegroup(self.__HANDLE__)
        if(result!=self.STATUS.OK):
            raise NeXusError,"opensourcegroup() FAILED[%d]"

    def getdims(self):
        # getinfo returns the dimensions
        status,rank,dims,type=nexus.NXgetinfo(self.__HANDLE__)
        # create exception if this doesn't make sense
        if(dims==None):
            raise NeXusError,"getdims() FAILED"

        print "0:",dims,type

        # return the result
        return dims,type

    def getnextentry(self):
        status,name,nxclass,type=nexus.NXgetnextentry(self.__HANDLE__)
        if(status!=self.STATUS.OK):
            return (None,None)

        return (name,nxclass)

    def getnextattr(self):
        # find out about the attribute
        status,name,length,type=nexus.NXgetnextattr(self.__HANDLE__)
        if(status!=self.STATUS.OK):
            return (None,None)
    
        type=self.SDS_TYPES.key(int(type))

        return (name,self.getattr(name,type))

    def getattr(self,name,type):
        i_type=self.SDS_TYPES.val(type)
        status,value,i_type=nexus.NXgetattr(self.__HANDLE__,name,i_type)
        if(value==None):
            raise NeXusError,"getattr(%s,%s) FAILED" % (name,type)

        return value

    def getgroupID(self):
        result=nexus.NXgetgroupID(self.__HANDLE__)
        if(result!=self.STATUS.OK):
            raise NeXusError,"getgroupID() FAILED[%d]"

#    def sameID(self): # not exposed through swig
#        raise NotImplementedError

    def initgroupdir(self):
        result=nexus.NXinitgroupdir(self.__HANDLE__)
        if(result!=self.STATUS.OK):
            raise NeXusError,"initgroupdir() FAILED[%d]" % result

    def initattrdir(self):
        result=nexus.NXinitattrdir(self.__HANDLE__)
        if(result!=self.STATUS.OK):
            raise NeXusError,"initattrdir() FAILED[%d]" % result

#    def setnumberformat(self): # not exposed through swig
#        raise NotImplementedError

##### These two functions appear in napi.h, but should NEVER be
##### brought into the python layer
#extern  NXstatus  NXmalloc(void** data, int rank, int dimensions[], int datatype);
#extern  NXstatus  NXfree(void** data);

# ----- nxdataset.i (c <-> python) stuff
def create_sds(type,dims):
    args=[type]
    try:
        args.extend(dims)
    except TypeError:
        args.append(dims)
    return apply(nexus.create_nxds,args)

def create_text_sds(value):
    return nexus.create_text_nxds(value)

def delete_sds(c_ptr):
    nexus.drop_nxds(c_ptr)

def get_sds_rank(c_ptr):
    return nexus.get_nxds_rank(c_ptr)

#def get_sds_type(c_ptr):
#    type=nexus.get_nxds_type(c_ptr)
#    return NeXusFile.SDS_TYPES.key(type)

def get_sds_dim(rank,c_ptr):
    result=[]
    for i in range(rank):
        result.append(nexus.get_nxds_dim(c_ptr,i))
    return result

def get_sds_value(c_ptr,type,index):
    args=[c_ptr]
    try:
        args.extend(index)
    except TypeError:
        args.append(index)
    value=apply(nexus.get_nxds_value,args)
    try: # hack to deal with terrible enum class
        type=NeXusFile.SDS_TYPES.val(type)
    except KeyError:
        pass # is already an integer
    if(type==NeXusFile.SDS_TYPES.FLOAT32 or type==NeXusFile.SDS_TYPES.FLOAT64):
        return value
    else:
        return int(value)

def get_sds_text(c_ptr):
    return nexus.get_nxds_text(c_ptr)
    
def put_sds_value(c_ptr,value,index):
    args=[c_ptr,value]
    try:
        args.extend(index)
    except TypeError:
        args.append(index)
    result=apply(nexus.put_nxds_value,args)
    if result!=NeXusFile.STATUS.OK:
        raise NeXusError,"put_sds_value(?,%s,%s) FAILED[%d]" % (str(value),str(index))

# ----- utility functions
def dims_to_cdims(dims):
    """The result of this needs to be freed using delete_sds(c_ptr)"""
    # convert the information to c-natives
    rank=len(dims)
    c_dims=create_sds(NeXusFile.SDS_TYPES.INT32,rank)
    for (it,pos) in map(None,dims,range(rank)):
        put_sds_value(c_dims,it,pos)
    # return the void pointer
    return (rank,c_dims)

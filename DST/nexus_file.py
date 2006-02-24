import nxpython
import enum

class NeXusException(SystemError):
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
#    ACCESS.set("CREATEXML",nxpython.NXACC_CREATEXML) # NOT PUBLISHED
#    ACCESS.set("NOSTRIP",  nxpython.NXACC_NOSTRIP) # NOT PUBLISHED

    # status reports from functions
    STATUS=enum.Enum()
    STATUS.set("OK",   1)
    STATUS.set("ERROR",0)
    STATUS.set("EOD",  -1)

    # compression algorithms to use
    COMPRESS=enum.Enum()
#    COMPRESS.set("NONE",nxpython.NX_COMP_NONE) # NOT PUBLISHED
#    COMPRESS.set("LZW", nxpython.NX_COMP_LZW) # NOT PUBLISHED
#    COMPRESS.set("RLE", nxpython.NX_COMP_RLE) # NOT PUBLISHED
#    COMPRESS.set("HUF", nxpython.NX_COMP_HUF) # NOT PUBLISHED

    # ----- python stuff
    def __init__(self,filename,access=nxpython.NXACC_READ):
        if(access!=nxpython.NXACC_READ):
            raise NotImplementedError,"Can only read files"
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
        if(result!=STATUS.OK):
            raise NeXusError,"makegroup(%s,%s) FAILED[%d]" % (name,type,result)

    def opengroup(self,name,type):
        result=nxpython.nx_opengroup(self.__HANDLE__,name,type)
        if(result!=STATUS.OK):
            raise NeXusError,"opengroup(%s,%s) FAILED[%d]" % (name,type,result)

    def openpath(self,path):
        result=nxpython.nx_openpath(self.__HANDLE__,path)
        if(result!=STATUS.OK):
            raise NeXusError,"openpath(%s) FAILED[%d]" % (path,result)
        
    def opengrouppath(self,path):
        result=nxpython.nx_opengrouppath(self.__HANDLE__,path)
        if(result!=STATUS.OK):
            raise NeXusError,"opengrouppath(%s) FAILED[%d]" % (path,result)
        
    def closegroup(self):
        result=nxpython.nx_closegroup(self.__HANDLE__)
        if(result!=STATUS.OK):
            raise NeXusError,"closegroup() FAILED[%d]" % (result)

#    def makedata(self,name,type,dims):
#        rank=len(dims)
#        c_dims=nxpython.create_nxds(rank,NeXusFile.SDS_TYPES.INT8,dims)
#        result=nxpython.nx_makedata(self.__HANDLE__,name,rank,type,c_dims)
#        if(result!=STATUS.OK):
#            raise NeXusError,"makedata(%s,%d,%s) FAILED[%d]" % (name,type,str(dims),result)

    # ----- nxdataset.i (c <-> python) stuff
    def create_sds(self,type,dims):
        args=[type]
        args.extend(dims)
        return apply(nxpython.create_nxds,args)

    def create_text_sds(self,value):
        return nxpython.create_text_nxds(value)

    def drop_sds(self,c_ptr):
        nxpython.drop_nxds(c_ptr)

    def get_sds_rank(self,c_ptr):
        return nxpython.get_nxds_rank(c_ptr)

    def get_sds_type(self,c_ptr):
        type=get_nxds_type(c_ptr)
        return self.SDS_TYPES.key(type)

    def get_sds_dim(self,rank,c_ptr):
        result=[]
        for i in rank:
            result.append(nxpython.get_nxds_dim(c_ptr,i))
        return result

    def get_sds_value(self,c_ptr,index):
        args=[c_ptr]
        args.extend(index)
        return apply(nxpython.get_nxds_value,args)

    def get_sds_text(self,c_ptr):
        return nxpython.get_nxds_text(c_ptr)

    def put_sds_value(self,c_ptr,value,index):
        args=[c_ptr,value]
        args.extend(index)
        result=apply(nxpython.put_nxds_value,args)
        if result!=self.SDS_TYPES.OK:
            raise NeXusError,"put_sds_value(?,%s,%s) FAILED[%d]" % (str(value),str(index))


    ######################################################################

"""
int  put_nxds_value(void *ptr, double value, int dim0, int dim1, int dim2, 
	int dim3, int dim4, int dim5,int dim6){
	int dim[MAXDIM];

	dim[0] = dim0;
	dim[1] = dim1;
	dim[2] = dim2;
	dim[3] = dim3;
	dim[4] = dim4;
	dim[5] = dim5;
	dim[6] = dim6;

	return putNXDatasetValue((pNXDS)ptr,dim,value);
}
"""

    ######################################################################


"""
extern  NXstatus  NXmakedata (NXhandle handle, CONSTCHAR* label, int datatype, int rank, int dim[]);
extern  NXstatus  NXcompmakedata (NXhandle handle, CONSTCHAR* label, int datatype, int rank, int dim[], int comp_typ, int bufsize[]);
extern  NXstatus  NXcompress (NXhandle handle, int compr_type);
extern  NXstatus  NXopendata (NXhandle handle, CONSTCHAR* label);
extern  NXstatus  NXclosedata(NXhandle handle);
extern  NXstatus  NXputdata(NXhandle handle, void* data);

extern  NXstatus  NXputattr(NXhandle handle, CONSTCHAR* name, void* data, int iDataLen, int iType);
extern  NXstatus  NXputslab(NXhandle handle, void* data, int start[], int size[]);    

extern  NXstatus  NXgetdataID(NXhandle handle, NXlink* pLink);
extern  NXstatus  NXmakelink(NXhandle handle, NXlink* pLink);
extern  NXstatus  NXopensourcegroup(NXhandle handle);

extern  NXstatus  NXgetdata(NXhandle handle, void* data);
extern  NXstatus  NXgetinfo(NXhandle handle, int* rank, int dimension[], int* datatype);
extern  NXstatus  NXgetnextentry(NXhandle handle, NXname name, NXname nxclass, int* datatype);

extern  NXstatus  NXgetslab(NXhandle handle, void* data, int start[], int size[]);
extern  NXstatus  NXgetnextattr(NXhandle handle, NXname pName, int *iLength, int *iType);
extern  NXstatus  NXgetattr(NXhandle handle, char* name, void* data, int* iDataLen, int* iType);
extern  NXstatus  NXgetattrinfo(NXhandle handle, int* no_items);
extern  NXstatus  NXgetgroupID(NXhandle handle, NXlink* pLink);
extern  NXstatus  NXgetgroupinfo(NXhandle handle, int* no_items, NXname name, NXname nxclass);
extern  NXstatus  NXsameID(NXhandle handle, NXlink* pFirstID, NXlink* pSecondID);

extern  NXstatus  NXinitgroupdir(NXhandle handle);
extern  NXstatus  NXinitattrdir(NXhandle handle);
extern  NXstatus  NXsetnumberformat(NXhandle handle,
						      int type, char *format);
"""

#extern  NXstatus  NXmalloc(void** data, int rank, int dimensions[], int datatype);
#extern  NXstatus  NXfree(void** data);

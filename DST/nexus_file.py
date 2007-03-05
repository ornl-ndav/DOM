#                        Data Object Model
#           A part of the SNS Analysis Software Suite.
#
#                  Spallation Neutron Source
#          Oak Ridge National Laboratory, Oak Ridge TN.
#
#
#                             NOTICE
#
# For this software and its associated documentation, permission is granted
# to reproduce, prepare derivative works, and distribute copies to the public
# for any purpose and without fee.
#
# This material was prepared as an account of work sponsored by an agency of
# the United States Government.  Neither the United States Government nor the
# United States Department of Energy, nor any of their employees, makes any
# warranty, express or implied, or assumes any legal liability or
# responsibility for the accuracy, completeness, or usefulness of any
# information, apparatus, product, or process disclosed, or represents that
# its use would not infringe privately owned rights.
#

import sns_napi
import nessi_list
import enum

class NeXusError(SystemError):
    pass

class NeXusFile:
    # access methods
    ACCESS=enum.Enum()
    ACCESS.set("READ",     sns_napi.ACC_READ)
    ACCESS.set("RDWR",     sns_napi.ACC_RDWR)
    ACCESS.set("CREATE",   sns_napi.ACC_CREATE)
    ACCESS.set("CREATE4",  sns_napi.ACC_CREATE4)
    ACCESS.set("CREATE5",  sns_napi.ACC_CREATE5)
    ACCESS.set("CREATEXML",sns_napi.ACC_CREATEXML)
    ACCESS.set("NOSTRIP",  sns_napi.ACC_NOSTRIP)

    # ----- python stuff
    def __init__(self,filename,access=sns_napi.ACC_READ):
        self.__HANDLE__=sns_napi.open(filename,access)
        if(self.__HANDLE__==None):
            raise SystemError,"Failed to read file: %s" % filename
        self.__filename    = filename
        self.__path        = ""

    def filename(self):
        return self.__filename

    # ----- napi stuff
    def flush(self):
        sns_napi.flush(self.__HANDLE__)

    def makegroup(self,name,type):
        return sns_napi.makegroup(self.__HANDLE__,name,type)

    def opengroup(self,name,type):
        self.__path=""
        return sns_napi.opengroup(self.__HANDLE__,name,type)

    def openpath(self,path):
        if path==self.__path:
            return None
        self.__path=path
        return sns_napi.openpath(self.__HANDLE__,path)
        
    def opengrouppath(self,path):
        self.__path=""
        return sns_napi.opengrouppath(self.__HANDLE__,path)
        
    def closegroup(self):
        self.__path=""
        return sns_napi.closegroup(self.__HANDLE__)

    def makedata(self,name,type,dims):
        return sns_napi.makedata(self.__HANDLE__,name,type,dims)

    def compmakedata(self,name,type,dims,c_buffer):
        return sns_napi.compmakedata(self.__HANDLE__,name,type,dims)

    def compress(self,compression):
        return sns_napi.compress(self.__HANDLE__,compression)

    def opendata(self,name):
        self.__path=""
        return sns_napi.opendata(self.__HANDLE__,name)

    def closedata(self):
        self.__path=""
        return sns_napi.closedata(self.__HANDLE__)

    def putdata(self,c_ptr):
        return sns_napi.putdata(self.__HANDLE__,c_ptr)

    def putslab(self,c_ptr,dims):
        return sns_napi.putslab(self.__HANDLE__,c_ptr,dims)

    def getdata(self,type="f"):
        return sns_napi.getdata(self.__HANDLE__,type)

    def getslab(self,start,size,type="f"):
        return sns_napi.getslab(self.__HANDLE__,start,size,type)

    def putattr(self,name,c_ptr,type):
        return sns_napi.putattr(self.__HANDLE__,name,c_ptr,type)

    def getdataID(self):
        return sns_napi.getdataID(self.__HANDLE__)

    def makelink(self,link):
        return sns_napi.makelink(self.__HANDLE__,link)

    def opensourcegroup(self):
        self.__path=""
        return sns_napi.opensourcegroup(self.__HANDLE__)

    def getdims(self):
        return sns_napi.getinfo(self.__HANDLE__)

    def getnextentry(self):
        (name,nxclass,number)=sns_napi.getnextentry(self.__HANDLE__)
        return (name,nxclass)

    def getnextattr(self):
        return sns_napi.getnextattr(self.__HANDLE__)

    def getattr(self,name,type):
        return sns_napi.getattr(self.__HANDLE__,name)

    def getgroupID(self):
        return sns_napi.getgroupID(self.__HANDLE__)

#    def sameID(self): # not exposed through swig
#        raise NotImplementedError

    def initgroupdir(self):
        return sns_napi.initgroupdir(self.__HANDLE__)

    def initattrdir(self):
        return sns_napi.initattrdir(self.__HANDLE__)

#    def setnumberformat(self): # not exposed through swig
#        raise NotImplementedError

##### These two functions appear in napi.h, but should NEVER be
##### brought into the python layer
#extern  NXstatus  NXmalloc(void** data, int rank, int dimensions[], int datatype);
#extern  NXstatus  NXfree(void** data);

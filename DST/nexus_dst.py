import dst_base
import nxpython

class NeXusDST(dst_base.DST_BASE):
    MIME_TYPE="application/x-NeXus"

    ########## DST_BASE function
    def __init__(self,resource,*args,**kwargs):
        self.__HANDLE__=nxpython.nx_open(resource,nxpython.NXACC_READ)
        if(self.__HANDLE__==None):
            raise SystemError,"Failed to read file: %s" % resource
        self.__filename__=resource

    def __del__(self):
        super(type(dst_base.DST_BASE),self).__del__()
        self.release_resource()        # free allocated resource

    def release_resource(self):
        if(self.__HANDLE__!=None):
            nxpython.nx_close(self.__HANDLE__)
            self.__HANDLE=None

    ########## special functions

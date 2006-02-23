import dst_base
import sns_nexus

class NeXusDST(dst_base.DST_BASE):
    MIME_TYPE="application/x-NeXus"

    ########## DST_BASE function
    def __init__(self,resource,*args,**kwargs):
        self.__nexus=sns_nexus.SNSNeXus(resource)

    def release_resource(self):
        self.__nexus.close()

    ########## special functions
    def list_entries(self):
        return self.__nexus.ls()

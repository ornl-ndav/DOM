import dst_base
import nexus_file

class NeXusDST(dst_base.DST_BASE):
    MIME_TYPE="application/x-NeXus"

    ########## DST_BASE function
    def __init__(self,resource,*args,**kwargs):
        self.__nexus=nexus_file.NeXusFile(resource)

    def release_resource(self):
        self.__nexus.close()

    ########## special functions
    def list_entries(self):
        listing=[]
        self.__nexus.initgroupdir()
        name="blah"
        while name!=None:
            (name,type)=self.__nexus.getnextentry()
            if (name!=None) and (type!="CDF0.0"):
                listing.append((name,type))
        return listing

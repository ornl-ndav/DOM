import dst_base
import nexus_file

class NeXusDST(dst_base.DST_BASE):
    MIME_TYPE="application/x-NeXus"

    ########## DST_BASE function
    def __init__(self,resource,*args,**kwargs):
        self.__nexus=nexus_file.NeXusFile(resource)
        listing=self.__build_tree()
        print listing

    def release_resource(self):
        self.__nexus.close()

    ########## special functions
    def __list_level(self):
        listing=[]
        self.__nexus.initgroupdir()
        name="blah"
        while name!=None:
            (name,type)=self.__nexus.getnextentry()
            if (name!=None) and (type!="CDF0.0"):
                if(type!="SDS"):
                    type=""
                listing.append("%s%s" % (name,type))
        return listing

    def __purge_listing(self,listing):
        for item in listing:
            first=listing.index(item)
            try:
                while True:
                    index=listing.index(item,first+1)
                    del listing[index]
            except ValueError:
                pass
        return listing

    def __prepend_parent(self,parent,listing):
        my_list=[]
        for item in listing:
            my_list.append("%s/%s" % (parent,item))
        return my_list

    def __build_tree(self,listing=[]):
        # set up result
        my_listing=[]
        my_listing.extend(listing)

        # get a listing for each element in the tree
        if(listing!=None) and (len(listing)>0):
            for parent in listing:
                if(not parent.endswith("SDS")):
                    self.__nexus.openpath(parent)
                    level_listing=self.__list_level()
                    if(len(level_listing)>0):
                        my_listing.extend(self.__prepend_parent(parent,
                                                                level_listing))
        # start at the beginning
        else:
            my_listing=self.__prepend_parent("",self.__list_level())

        # remove repetitive items
        my_listing=self.__purge_listing(my_listing)

        # recurse if the list has changed
        if len(my_listing)>len(listing):
            return self.__build_tree(my_listing)
        else:
            return my_listing
        

    def list_entries(self):
        self.__nexus.openpath("/")
        listing=self.__list_level()

        return self.__prepend_parent("",listing)

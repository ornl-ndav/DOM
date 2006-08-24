import dst_base
import nexus_dst
import nexus_file
import SOM

class GeomDST(dst_base.DST_BASE):
    MIME_TYPE="application/x-NxsGeom"

    def __init__(self, resource, data_group_path=None, signal=1,
                 *args, **kwargs):

        self.__nexus = nexus_file.NeXusFile(resource)
        self.__tree = self.__build_tree()

        self.__inst_info = nexus_dst.NeXusInstrument(self.__nexus,
                                                     self.__tree,
                                                     from_saf=True)
        self.__sns_info = nexus_dst.SnsInformation(self.__nexus, self.__tree,
                                                   self.__inst_info.getName())

    def setGeometry(self, som_id, som):
        id_list = []
        try:
            som_id.reverse()
            som_id.reverse()
            for i in range(len(som_id)):
                id_list.append(som_id[i])
        except AttributeError:
            id_list.append(som_id)

        inst_keys = []

        # If there is only one ID in the list, expect that starting and
        # ending ids are a single tuple each
        if len(id_list) == 1:
            len_id_1 = True
        else:
            len_id_1 = False

        for id in id_list:
            inst_keys.append(id[0].split('/')[-1])
            inst_keys.append(self.__inst_info.getInstrument(id[0],
                                                            from_saf=True))

        if len(inst_keys) > 2:
            inst = SOM.CompositeInstrument(pairs=inst_keys)
            som.attr_list.instrument = inst
        else:
            som.attr_list.instrument = inst_keys[1]

        info_keys = self.__sns_info.getKeys()
        for key in info_keys:
            pair_list = self.__sns_info.getInformation(key)
            if pair_list[1] is None:
                info = None
            else:
                if len(pair_list) > 2:
                    info = SOM.CompositeInformation(pairs=pair_list)
                else:
                    info = pair_list[1]

            som.attr_list[key] = info

        return

    def release_resource(self):
        del self.__nexus
        del self.__tree
        del self.__inst_info
        del self.__sns_info

    def __list_level(self):
        listing={}
        self.__nexus.initgroupdir()
        name="blah"
        while name!=None:
            (name,type)=self.__nexus.getnextentry()
            if (name!=None) and (type!="CDF0.0"):
                listing[name]=type
        return listing

    def __prepend_parent(self,parent,listing):
        my_list={}
        for key in listing.keys():
            my_list[("%s/%s" % (parent,key))]=listing[key]
        return my_list

    def __build_tree(self,listing={}):
        # set up result
        my_listing=listing.copy()

        # get a listing for each element in the tree
        if(listing!=None) and (len(listing)>0):
            for parent in listing.keys():
                if(not listing[parent]=="SDS"):
                    self.__nexus.openpath(parent)
                    level_listing=self.__list_level()
                    level_listing=self.__prepend_parent(parent,level_listing)
                    for inner in level_listing.keys():
                        my_listing[inner]=level_listing[inner]
        # or start at the beginning
        else:
            my_listing=self.__prepend_parent("",self.__list_level())

        # recurse if the list has changed
        if len(my_listing)>len(listing):
            return self.__build_tree(my_listing)
        else:
            return my_listing

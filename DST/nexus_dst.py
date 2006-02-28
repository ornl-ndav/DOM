import dst_base
import nexus_file

class NeXusDST(dst_base.DST_BASE):
    MIME_TYPE="application/x-NeXus"

    ########## DST_BASE function
    def __init__(self,resource,data_group_path=None,*args,**kwargs):
        self.__nexus=nexus_file.NeXusFile(resource)
        self.__tree=self.__build_tree()

        # set the data group
        if(data_group_path==None):
            data_list=self.list_type("NXdata")
            if len(data_list)==1:
                data_group_path=data_list[0]
        self.set_data(data_group_path)

    def release_resource(self):
        self.__nexus.close()

    ########## special functions
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
        
    def __get_data_children(self):
        if self.__data_group==None:
            return None

        # get the list of SDS in the data group
        SDS_list=[]
        for key in self.__tree.keys():
            if self.__tree[key]=="SDS":
                if key.startswith(self.__data_group):
                    SDS_list.append(key)

        # create the list of children with attributes
        data_children={}
        for sds in SDS_list:
            self.__nexus.openpath(sds)
            child_attrs={}
            while True:
                (attr_name,attr_value)=self.__nexus.getnextattr()
                if(attr_name==None): break
                child_attrs[attr_name]=attr_value
            data_children[sds]=child_attrs

        return data_children

    def list_type(self,type):
        my_list=[]
        for key in self.__tree.keys():
            if self.__tree[key]==type:
                my_list.append(key)
        return my_list

    def print_data_info(self):
        print "***** DATA    %s" % self.__data_group
        print "      COUNTS  %s" % self.__data_counts
        print "      VAR     %s" % self.__data_var
        if(self.__data_axes==None):
            print "      AXES    %s" % self.__data_axes
        else:
            for i in range(len(self.__data_axes)):
                print "      AXIS[%d] %s" % (i,self.__data_axes[i])

    def set_data(self,path,signal=1):
        if(path==None): # unset everything
            self.__data_group=None
            self.__data_axes=None
            self.__data_counts=None
            self.__data_var=None
            return

        if not path in self.__tree.keys():
            raise ValueError,"Specified invalid data path \"%s\"" % path

        # set starting values
        self.__data_group=path
        self.__data_axes=None
        self.__data_counts=None
        self.__data_var=None

        # search through available attributes for information
        children=self.__get_data_children()
        axes={}
        for child in children.keys():
            for key in children[child]:
                print child,children[child],key,children[child][key]
                value=children[child][key]
                if key=="signal": # look for the data
                    if value==signal:
                        self.__data_counts=child
                elif key=="axis": # look for the axis to label themselves
                    axes[value]=key

        # look for the axes as an attribute to the signal data
        counts_attrlist=children[self.__data_counts]
        for key in counts_attrlist.keys():
            if key=="axes":
                inner_list=(counts_attr_list[key]).split(",")
                for i in range(len(inner_list)):
                    axes[i]=inner_list[i]

        # set the axes
        if len(axes)>0:
            self.__data_axes=[]
        for i in range(len(axes)):
            self.__data_axes.append(axes[i])

        # if the varience in the counts is not found then set it to be
        # the counts
        if self.__data_var==None:
            self.__data_var=self.__data_counts

        #self.print_data_info() # DEBUG PRINT STATEMENT

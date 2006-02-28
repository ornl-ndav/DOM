import dst_base
import nexus_file
import nessi_vector

class NeXusDST(dst_base.DST_BASE):
    MIME_TYPE="application/x-NeXus"

    ########## DST_BASE function
    def __init__(self,resource,data_group_path=None,so_axis="time_of_flight",
                 *args,**kwargs):

        # allocate places for everything
        self.__nexus=nexus_file.NeXusFile(resource)
        self.__tree=self.__build_tree()
        self.__data_group=None
        self.__data_signal=None
        self.__data_axes=None
        self.__data_counts=None
        self.__data_var=None
        self.__so_axis=None
        self.__label_axes=None

        # set the data group if there is only one
        if(data_group_path==None):
            data_list=self.list_type("NXdata")
            if len(data_list)==1:
                data_group_path=data_list[0]
        self.set_data(data_group_path)

        # set the so axis
        self.set_SO_axis(so_axis)

    def release_resource(self):
        self.__nexus.close()

    def get_SO_ids(self,SOM_id=None):
        change_som= (SOM_id!=None) \
                    and (SOM_id!=(self.__data_group,self.__data_signal))
        print "CHANGE:",change_som

        # cache initial state
        my_data_group=self.__data_group
        my_data_signal=self.__data_signal
        my_so_axis=self.__so_axis

        # set the active SOM
        if change_som:
            apply(self.set_data,SOM_id)

        print "AXES",self.__so_axis,self.__label_axes

        num_axes=len(self.__data_axes)
        so_list=[]
        if num_axes==1:
            so_list.append(1)
        elif num_axes==2:
            pass

        # restore the initial SOM
        if(change_som):
            self.set_data(my_data_group,my_data_signal)
            self.set_SO_axis(my_so_axis)

        return so_list

    def get_SOM_ids(self):
        path_list=self.list_type("NXdata")
        SOM_list=[]
        for path in path_list:
            signal_list=self.__get_avail_signals(path)
            for it in signal_list:
                SOM_list.append((path,it))
        return SOM_list

    def getSO(self,som_id,so_id):
        return None

    def getSOM(self,som_id=None):
        if(som_id!=None):
            self.set_data((som_id,1))
        return None

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
        
    def __get_data_children(self,data_group=None):
        if(data_group==None):
            data_group=self.__data_group
        if data_group==None:
            return None

        # get the list of SDS in the data group
        SDS_list=[]
        for key in self.__tree.keys():
            if self.__tree[key]=="SDS":
                if key.startswith(data_group):
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

    def __get_avail_signals(self,data_group):
        children=self.__get_data_children(data_group)

        signal_list=[]
        for child in children.keys():
            for key in children[child]:
                value=children[child][key]
                if key=="signal":
                    signal_list.append(value)

        return signal_list

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
        print "      SO_AXIS %s" % self.__so_axis
        print "      L_AXES  %s" % self.__label_axes


    def __1d_c2nessi(self,c_ptr,type,length):
        result=nessi_vector.NessiVector()
        for i in range(length):
            val=self.__nexus.get_sds_value(c_ptr,type,i)
            result.append(val)
        return result

    def set_SO_axis(self,so_axis):
        if self.__data_axes==None:
            return

        self.__label_axes=[]
        for axis in self.__data_axes:
            if axis.endswith(so_axis):
                self.__so_axis=axis
            else:
                self.__label_axes.append(axis)

        # for giggles, get the so axis values
        self.__nexus.openpath(self.__so_axis)
        c_so_axis=self.__nexus.getdata()
        so_axis_info=self.__nexus.getinfo()
        print self.__so_axis,"=",so_axis_info,c_so_axis
        nv_so_axis=self.__1d_c2nessi(c_so_axis,so_axis_info[0],so_axis_info[1][0])
        print nv_so_axis

    def set_data(self,path,signal=1):
        if(path==None): # unset everything
            self.__data_group=None
            self.__data_signal=None
            self.__data_axes=None
            self.__data_counts=None
            self.__data_var=None
            return

        if not path in self.__tree.keys():
            raise ValueError,"Specified invalid data path \"%s\"" % path

        # set starting values
        self.__data_group=path
        self.__data_signal=signal
        self.__data_axes=None
        self.__data_counts=None
        self.__data_var=None

        # search through available attributes for information
        children=self.__get_data_children()
        axes={}
        for child in children.keys():
            for key in children[child]:
                value=children[child][key]
                if key=="signal": # look for the data
                    if value==self.__data_signal:
                        self.__data_counts=child
                elif key=="axis": # look for the axis to label themselves
                    axes[value]=child

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
            self.__data_axes.append(axes[i+1])
        self.set_SO_axis(self.__data_axes[0])

        # if the varience in the counts is not found then set it to be
        # the counts
        if self.__data_var==None:
            self.__data_var=self.__data_counts

        #self.print_data_info() # DEBUG PRINT STATEMENT

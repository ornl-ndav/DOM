import dst_base
import nexus_file
import nessi_list
import so
import som

class NeXusDST(dst_base.DST_BASE):
    MIME_TYPE="application/x-NeXus"

    ########## DST_BASE function
    def __init__(self,resource,data_group_path=None,signal=1,
                 so_axis="time_of_flight",*args,**kwargs):

        # allocate places for everything
        self.__nexus=nexus_file.NeXusFile(resource)
        self.__tree=self.__build_tree()
        self.__data_group=None
        self.__data_signal=None
        self.__so_axis=None
        self.__avail_data={}

        # create the data list
        som_ids=self.__generate_SOM_ids()
        for (location,signal) in som_ids:
            data=NeXusData(self.__nexus,self.__tree,location,signal)
            self.__avail_data[(location,signal)]=data

        # set the data group if there is only one
        if data_group_path==None:
            if len(self.__avail_data)==1:
                key=self.__avail_data.keys()[0]
                self.__data_group=key[0]
                self.__signal=key[1]

        # set the so axis
        self.__so_axis=so_axis

    def get_SO_ids(self,SOM_id=None,so_axis=None):
        if(SOM_id!=None):
            data=self.__avail_data[SOM_id]
        else:
            data=self.__avail_data[(self.__data_group,self.__signal)]

        return data.get_ids()

    def get_SOM_ids(self):
        return self.__avail_data.keys()

    def getSO(self,som_id,so_id,so_axis=None):
        if so_axis==None:
            return self.__avail_data[som_id].get_so(so_id)

        data=self.__avail_data[som_id]
        orig_axis=data.variable

        if orig_axis.label==so_axis or orig_axis.location==so_axis:
            return data.get_so(so_id)
        data.set_so_axis(so_axis)
        result=data.get_so(so_id)
        data.set_so_axis(orig_axis.label)
        return result
        

    def getSOM(self,som_id=None,so_axis=None,**kwds):
        """Available keywords are start_id,end_id which provide a way
        to carve out the data to retrieve"""

        # grab the keyword paramaters
        if(kwds.has_key("start_id")):
            start_id=kwds["start_id"]
        else:
            start_id=None
        if(kwds.has_key("end_id")):
            end_id=kwds["end_id"]
        else:
            end_id=None

        if(som_id!=None):
            data=self.__avail_data[som_id]
        else:
            data=self.__avail_data[(self.__data_group,self.__signal)]

        orig_axis=data.variable
        if orig_axis.label==so_axis or orig_axis.location==so_axis:
            orig_axis=None

        if orig_axis!=None and so_axis!=None and data.has_axis(so_axis):
            data.set_so_axis(so_axis)

        result=som.SOM()
        result.attr_list[result.TITLE]="" # should put something here
        result.attr_list[result.X_LABEL]=data.variable.label
        result.attr_list[result.X_UNITS]=data.variable.units
        result.attr_list[result.Y_LABEL]=data.data_label
        result.attr_list[result.Y_UNITS]=data.data_units
        result.attr_list["filename"]=self.__nexus.filename()

        attrs=self.__get_attr_list(data.location)
        for key in attrs.keys():
            result.attr_list[key]=attrs[key]

        min_id=data.get_id_min()
        max_id=data.get_id_max()

        if (start_id==None) or (min_id>start_id):
            start_id=min_id

        if (end_id==None) or (max_id<end_id):
            end_id=max_id

        ids=self.__generate_ids(start_id,end_id)

        for item in ids:
            so=data.get_so(item)
            result.append(so)

        if orig_axis!=None:
            data.set_so_axis(orig_axis.location)

        return result

    ########## special functions
    def __generate_ids(self,start,stop):
        if(start==stop):
            return [start]
        try:
            dim=len(start)
            result=[]
            if dim==2:
                for i in range(start[0],stop[0]+1):
                    for j in range(start[1],stop[1]+1):
                        result.append((i,j))
                return result
            else:
                raise RuntimeError,"Do not understand %dd indices" % dim
        except TypeError,e: #assume it is a scalar
            return range(start,stop)
            
        

    def __get_attr_list(self,data_path):
        # prefix of what attributes to use
        data_path="/"+data_path.split("/")[0]

        # generate the full list of attributes to use
        possible_list=self.list_type("SDS")
        attr_list=[]
        for item in possible_list:
            if item.startswith(data_path):
                if len(item.split("/"))==3:
                    attr_list.append(item)

        attrs={}
        for path in attr_list:
            key=path.split("/")[-1]
            attrs[key]=self.__get_val_as_str(path)

        return attrs

    def __get_val_as_str(self,path):
        self.__nexus.openpath(path)
        return str(self.__nexus.getdata())

    def __generate_SOM_ids(self):
        path_list=self.list_type("NXdata")
        SOM_list=[]
        for path in path_list:
            signal_list=self.__get_avail_signals(path)
            for it in signal_list:
                SOM_list.append((path,it))
        return SOM_list

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
            return {}

        # get the list of SDS in the data group
        SDS_list=[]
        for key in self.__tree.keys():
            if self.__tree[key]=="SDS":
                if key.startswith(data_group):
                    SDS_list.append(key)

        # create the list of children with attributes
        data_children={}
        for sds in SDS_list:
            data_children[sds]=__get_sds_attr__(self.__nexus,sds)

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

    def set_SO_axis(self,so_axis):
        data=self.__avail_data[(self.__data_group,self.__data_signal)]
        if data.has_axis(so_axis):
            self.__so_axis=so_axis
        else:
            raise ValueError,"Invalid axis specified (%s)" % so_axis

    def set_data(self,path,signal=1):
        if self.__avail_data.has_key((path,signal)):
            self.__data_group=path
            self.__data_signal=signal
        else:
            raise ValueError,"Invalid data specified (%s,%d)" % (path,signal)

class NeXusData:
    def __init__(self,filehandle,tree,path,signal):
        # do the easy part
        self.location=path
        self.__nexus=filehandle
        self.signal=None
        self.__data=None
        self.__data_var=None # if left unset use the data for this
        self.__data_dims=[]
        self.data_label=""
        self.data_units=""
        self.axes=[]
        self.variable=""
        self.__data_cptr=None # replace with getslab stuff
        
        # now start pushing through attributes
        children=self.__get_data_children(tree,path)
        axes={}
        for child in children.keys():
            for key in children[child]:
                value=children[child][key]
                if key=="signal": # look for the data
                    if value==signal:
                        self.signal=signal
                        self.__data=child
                        self.data_label=child.split("/")[-1]
                elif key=="axis": # look for the axis to label themselves
                    axes[value]=NeXusAxis(self.__nexus,child)
        if self.signal==None:
            raise ValueError,"Could not find signal=%d" % int(signal)

        # look for the axes as an attribute to the signal data
        # also find the units
        counts_attrlist=children[self.__data]
        for key in counts_attrlist.keys():
            if key=="axes":
                inner_list=(counts_attr_list[key]).split(",")
                for i in range(len(inner_list)):
                    axes[i]=NeXusAxis(self.__nexus,inner_list[i])
            if key=="units":
                self.units=counts_attrlist[key]

        # set the axes
        if len(axes)>0:
            self.axes=[]
        for i in range(len(axes)):
            self.axes.append(axes[i+1])
        self.variable=self.axes[0]

    def set_so_axis(self,axis):
        for my_axis in self.axes:
            if my_axis.label==axis:
                self.variable=my_axis
                return
            if my_axis.location==axis:
                self.variable=my_axis
                return
        raise RuntimeError,"Invalid axis request %s" % axis
        
    def __id_to_index(self,so_id):
        num_axes=len(self.axes)

        if num_axes==2:
            if self.axes[0]==self.variable:
                return [0,so_id]
            else:
                return [so_id,0]
        elif num_axes==3:
            var_index=self.axes.index(self.variable)
            index=0
            result=[]
            for i in range(3):
                if i==var_index:
                    result.append(0)
                else:
                    result.append(so_id[index])
                    index=index+1
            return result

        raise RuntimeError,"Do not know how to deal with %dd data" % num_axes

    def __get_slice(self,location,start_dim=None):
        self.__nexus.openpath(location)

        if start_dim==None: # assume that it is 1d
            #print "---------> 1d"
            return self.__nexus.getdata()
            
        #print "---------> %dd <-" % len(start_dim)
        # the number of values in the independent axis direction
        num_points=len(self.variable)-1 # assume histogram

        # set up the arguments for getting the slab
        end_dim=[]
        for item in start_dim:
            end_dim.append(item)
        var_index=self.axes.index(self.variable)
        end_dim[var_index]=end_dim[var_index]+num_points

        # get the value
        return self.__nexus.getslab(start_dim,end_dim)

    def get_so(self,so_id):
        #print "retrieving",so_id # remove
        # create a spectrum object
        spectrum=so.SO()

        # give it the id specified
        spectrum.id=so_id

        # give it the appropriate independent variable
        spectrum.x=self.variable.value

        # locate the data slice
        start_dim=self.__id_to_index(so_id)

        # set the data
        spectrum.y=self.__get_slice(self.__data,start_dim)

        # set the variance to be the data if no location is specified
        if self.__data_var==None:
            spectrum.var_y=self.__get_slice(self.__data,start_dim)
        else:
            spectrum.var_y=self.__get_slice(self.__data_var,start_dim)

        return spectrum

    def get_ids(self,var_axis=None):
        if(var_axis==None):
            var_axis=self.variable
        elif not var_axis.startswith("/"):
            for my_axis in self.axes:
                if my_axis.label==var_axis:
                    var_axis=my_axis

        num_axes=len(self.axes)
        if num_axes==1:
            return [0]
        elif num_axes==2:
            if self.axes[0]==var_axis:
                return range(len(self.axes[1]))
            else:
                return range(len(self.axes[0]))
        elif num_axes==3:
            label_axes=[]
            for axis in self.axes:
                if axis!=var_axis:
                    label_axes.append(axis)
#            for axis in label_axes:
#                print axis,
#                for i in range(10):
#                    print axis.value[i],
#                print
            id_list=[]
            for i in range(len(label_axes[0].value)):
                for j in range(len(label_axes[1].value)):
                    so_id=(i,j)
                    id_list.append(so_id)
            print
            print len(id_list)
            return id_list

        raise SystemError,"Cannot generate ids for %dd data" % num_axes

    def get_id_min(self):
        num_axes=len(self.axes)
        if num_axes==1:
            return 0
        elif num_axes==2:
            return 0
        elif num_axes==3:
            return (0,0)
        else:
            raise SystemError,"Cannot generate ids for %dd data" % num_axes

    def get_id_max(self):
        num_axes=len(self.axes)
        if num_axes==1:
            return 0
        elif num_axes==2:
            if self.axes[0]==self.variable:
                return len(self.axis[1])
            else:
                return len(self.axis[0])
        elif num_axes==3:
            label_axes=[]
            for axis in self.axes:
                if axis!=self.variable:
                    label_axes.append(axis)
            return (len(label_axes[0]),len(label_axes[1]))
        else:
            raise SystemError,"Cannot generate ids for %dd data" % num_axes


    def has_axis(self,axis):
        for my_axis in self.axes:
            if my_axis.label==axis:
                return True
            if my_axis.location==axis:
                return True
        return False

    def __repr__(self,verbose=False):
        result="%s:%d" % (self.location,self.signal)
        if not verbose:
            return result

        for axis in self.axes:
            result=result+"\n  "+str(axis)
        return result

    def __get_data_children(self,tree,data_group=None):
        if data_group==None:
            return {}

        # get the list of SDS in the data group
        SDS_list=[]
        for key in tree.keys():
            if tree[key]=="SDS":
                if key.startswith(data_group):
                    SDS_list.append(key)

        # create the list of children with attributes
        data_children={}
        for sds in SDS_list:
            data_children[sds]=__get_sds_attr__(self.__nexus,sds)

        return data_children

class NeXusAxis:
    def __init__(self,filehandle,path):
        # set the location
        self.location=path

        # the label is the tail of the path
        self.label=path.split("/")[-1]

        # get the value
        filehandle.openpath(path)
        self.value=filehandle.getdata()

        # get the list of attributes to set the label and units
        attrs=__get_sds_attr__(filehandle,path)
        try:
            self.units=attrs["units"]
        except KeyError:
            self.units=None
        try:
            self.number=attrs["axis"]
        except KeyError:
            self.number=None


    def __str__(self):
        return "[%d]%s (%s)" % (int(self.number),str(self.label),
                                str(self.units))

    def __len__(self):
        return len(self.value)

def __get_sds_attr__(filehandle,path):
    attrs={}
    filehandle.openpath(path)
    while True:
        (name,value)=filehandle.getnextattr()
        if(name==None): break
        attrs[name]=value
    return attrs


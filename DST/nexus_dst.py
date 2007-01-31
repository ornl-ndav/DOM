import dst_base
import nexus_file
import nessi_list
import param_map
import SOM

class NeXusDST(dst_base.DST_BASE):
    MIME_TYPE="application/x-NeXus"

    ########## DST_BASE function
    def __init__(self,resource,data_group_path=None,signal=1,
                 so_axis="time_of_flight",*args,**kwargs):

        # allocate places for everything
        self.__nexus=nexus_file.NeXusFile(resource)
        self.__tree=self.__build_tree()
        self.__data_group=[]
        self.__data_signal=[]
        self.__so_axis=None
        self.__avail_data={}
        self.__inst_info=None
        self.__extra_params = param_map.ParameterMap()        

        # create the data list
        som_ids=self.__generate_SOM_ids()
        for (location,signal) in som_ids:
            data=NeXusData(self.__nexus,self.__tree,location,signal)
            self.__avail_data[(location,signal)]=data

        self.__inst_info=NeXusInstrument(self.__nexus,self.__tree)
        self.__sns_info = SnsInformation(self.__nexus, self.__tree,
                                         self.__inst_info.getName())

        # set the data group to be all NXdata
        if data_group_path==None:
            nxdata_ids=self.__generate_SOM_ids(type="NXdata")
            for (location,signal) in nxdata_ids:
                self.__data_group.append(location)
                self.__data_signal.append(signal)

        # set the so axis
        self.__so_axis=so_axis

    def getParameter(self, name):
        entry_locations = self.list_type("NXentry")

        (tag, type) = self.__extra_params.getPathAndType(name)

        path = entry_locations[0] + "/" + tag

        try:
            self.__nexus.openpath(path)
        except IOError:
            return None

        try:
            units = self.__nexus.getattr("units", "s")
        except RuntimeError:
            units = None

        if type == "float":
            return (float(self.__nexus.getdata()[0]), units)
        elif type == "int":
            return (int(self.__nexus.getdata()[0]), units)
        elif type == "string":
            return (str(self.__nexus.getdata()[0]), units)
        else:
            raise RuntimeError("Do not understand type %s" % type)
    

    def get_SO_ids(self,SOM_id=None,so_axis=None):
        id_list = []
        if(SOM_id!=None):
            data=self.__avail_data[SOM_id]
            id_list = data.get_ids()
        else:
            som_id_list = self.__create_loc_sig_list()
            for som_id in som_id_list:
                data=self.__avail_data[som_id]
                id_list.extend(data.get_ids())

        return id_list

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
        

    def getSOM(self, som_id=None, so_axis=None, **kwds):
        """Available keywords are start_id,end_id which provide a way
        to carve out the data to retrieve"""

        # grab the keyword paramaters
        if kwds.has_key("start_id"):
            start_id = kwds["start_id"]
        else:
            start_id = None
        if kwds.has_key("end_id"):
            end_id = kwds["end_id"]
        else:
            end_id = None

        if so_axis is None:
            so_axis = "time_of_flight"
        else:
            pass

        try:
            mask_file = kwds["mask_file"]
        except KeyError:
            mask_file = None

        try:
            roi_file = kwds["roi_file"]
        except KeyError:
            roi_file = None

        if som_id is not None:
            id_list = []
            try:
                som_id.reverse()
                som_id.reverse()
                for i in range(len(som_id)):
                    id_list.append(som_id[i])
            except AttributeError:
                id_list.append(som_id)

        else:
            id_list = self.__create_loc_sig_list()

        result = SOM.SOM()
        result.attr_list["filename"] = self.__nexus.filename()
        result.attr_list["instrument_name"] = self.__inst_info.getName()
        result.attr_list["beamline"] = self.__inst_info.getBeamline()
        if mask_file is not None:
            result.attr_list["mask_file"] = mask_file
        else:
            pass

        if roi_file is not None:
            result.attr_list["roi_file"] = roi_file
        else:
            pass

        entry_locations = self.list_type("NXentry")
        path = entry_locations[0] + "/title"
        try:
            result.setTitle(self.__get_val_as_str(path))
        except IOError:
            result.setTitle("")

        path = entry_locations[0] + "/notes"
        try:
            result.attr_list["notes"] = self.__get_val_as_str(path)
        except IOError:
            result.attr_list["notes"] = ""

        inst_keys = []

        # If there is only one ID in the list, expect that starting and
        # ending ids are a single tuple each
        if len(id_list) == 1:
            len_id_1 = True
        else:
            len_id_1 = False

        count = 0
        for id in id_list:
            inst_keys.append(id[0].split('/')[-1])
            inst_keys.append(self.__inst_info.getInstrument(id[0]))

            data = self.__avail_data[id]
            # Construct keywords if necessary
            kwargs = {}
            if start_id is not None:
                if len_id_1:
                    kwargs["start_id"] = start_id
                else:
                    kwargs["start_id"] = start_id[count]
            else:
                pass
            
            if end_id is not None:
                if len_id_1:
                    kwargs["end_id"] = end_id
                else:
                    kwargs["end_id"] = end_id[count]
            else:
                pass

            if mask_file is not None:
                kwargs["mask_file"] = mask_file
            else:
                pass

            if roi_file is not None:
                kwargs["roi_file"] = roi_file
            else:
                pass

            self.__construct_SOM(result, data, so_axis, inst_keys[0], **kwargs)
            count += 1

        if len(inst_keys) > 2:
            inst = SOM.CompositeInstrument(pairs=inst_keys)
            result.attr_list.instrument = inst
        else:
            result.attr_list.instrument = inst_keys[1]

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

            result.attr_list[key] = info

        return result

    def __construct_SOM(self, result, data, so_axis, bank_id, **kwargs):

        if kwargs.has_key("start_id"):
            start_id = kwargs["start_id"]
        else:
            start_id = None
        if kwargs.has_key("end_id"):
            end_id = kwargs["end_id"]
        else:
            end_id = None

        try:
            mask_file = kwargs["mask_file"]
        except KeyError:
            mask_file = None

        try:
            roi_file = kwargs["roi_file"]
        except KeyError:
            roi_file = None

        orig_axis = data.variable
        if orig_axis.label == so_axis or orig_axis.location == so_axis:
            orig_axis = None

        if orig_axis is not None and so_axis is not None and \
               data.has_axis(so_axis):
            data.set_so_axis(so_axis)

        result.setAxisLabel(0, data.variable.label)
        result.setAxisUnits(0, data.variable.units)
        result.setYLabel(data.data_label)
        result.setYUnits(data.data_units)

        attrs = self.__get_attr_list(data.location)
        for key in attrs.keys():
            result.attr_list[key] = attrs[key]

        min_id = data.get_id_min()
        max_id = data.get_id_max()

        if start_id is None or min_id > start_id:
            start_id = min_id

        if end_id is None or max_id < end_id:
            end_id = max_id

        ids = self.__generate_ids(start_id, end_id, data.location)

        if mask_file is not None:
            ids = self.__mask_pixels(ids, mask_file)
        else:
            pass

        if roi_file is not None:
            ids = self.__filter_pixels(ids, bank_id, roi_file)
        else:
            pass

        num_tof_chan = data.get_variable_length() - 1
        num_y_pix = max_id[1]

        for item in ids:
            #so = data.get_so(item)
            so = data.get_so2(item, num_tof_chan, num_y_pix)
            result.append(so)

        if orig_axis is not None:
            data.set_so_axis(orig_axis.location)

    def __create_loc_sig_list(self):
        id_list = []
        for (location, signal) in map(None, self.__data_group,
                                     self.__data_signal):
            id_list.append((location, signal))

        return id_list

    def release_resource(self):
        del self.__nexus
        del self.__tree
        del self.__data_group
        del self.__data_signal
        del self.__so_axis
        del self.__avail_data

    def delete_blocks(self):
        del self.__avail_data
        self.__avail_data = None

    ########## special functions
    def __generate_ids(self,start,stop,location):
        if(start==stop):
            return [start]
        try:
            dim=len(start)
            result=[]
            if dim==2:
                from os.path import basename
                loc = basename(location)
                for i in range(start[0],stop[0]):
                    for j in range(start[1],stop[1]):
                        result.append((loc,(i,j)))
                return result
            else:
                raise RuntimeError,"Do not understand %dd indices" % dim
        except TypeError,e: #assume it is a scalar
            return range(start,stop)

    def __mask_pixels(self, id_list, mask_filename):

        try:
            mask_file = open(mask_filename, "r")
        except IOError:
            raise RuntimeError("Cannot open mask file %s" % mask_filename)

        for pixel_id_line in mask_file:

            pixel_id = self.__generate_pixel_id(pixel_id_line.rstrip())

            try:
                id_list.remove(pixel_id)
            except ValueError:
                pass

        mask_file.close()

        return id_list

    def __filter_pixels(self, id_list, bank_id, roi_filename):
        try:
            roi_file = open(roi_filename, "r")
        except IOError:
            raise RuntimeError("Cannot open roi file %s" % roi_filename)

        roi_id_list = []

        for pixel_id_line in roi_file:

            pixel_id = self.__generate_pixel_id(pixel_id_line.rstrip())

            # if bank IDs are not the same, move on
            if pixel_id[0] != bank_id:
                continue
            
            roi_id_list.append(pixel_id)
            
            #try:
            #    index = id_list.index(pixel_id)
            #    roi_id_list.append(id_list.pop(index))
            #except ValueError:
            #    pass

        roi_file.close()

        return roi_id_list

    def __generate_pixel_id(self, pixel_id_str):
        parts = pixel_id_str.split('_')
        return (parts[0], (int(parts[1]), int(parts[2])))        
        
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
            val=self.__get_val_as_str(path)
            if val.startswith('[') and val.endswith(']'):
                val = self.__strip_string(val)
            attrs[key]=val

        return attrs

    def __get_val_as_str(self,path):
        self.__nexus.openpath(path)
        return str(self.__nexus.getdata())

    def __strip_string(self, string):
        return string.lstrip('[').rstrip(']')

    def __generate_SOM_ids(self,**kwargs):
        try:
            value = kwargs["type"]
            if value == "NXdata":
                path_list=self.list_type("NXdata")
            elif value == "NXmonitor":
                path_list=self.list_type("NXmonitor")
            else:
                raise RuntimeError, "Do not understand type %s" % value
        except KeyError:
            path_list=self.list_type("NXdata")
            path_list.extend(self.list_type("NXmonitor"))
            
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
        som_id_list = self.__create_loc_sig_list()
        for som_id in som_id_list:
            data=self.__avail_data[som_id]
            if data.has_axis(so_axis):
                self.__so_axis=so_axis
            else:
                raise ValueError,"Invalid axis specified (%s)" % so_axis

    def set_data(self,path,signal=1):
        if self.__avail_data.has_key((path,signal)):
            self.__data_group.append(path)
            self.__data_signal.append(signal)
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
        self.__data_var_cptr=None # replace with getslab stuff
        
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
                    axis = NeXusAxis(self.__nexus,child)
                    if axis.primary is not None and axis.primary == 1:
                        axes[value] = axis
        if self.signal==None:
            raise ValueError,"Could not find signal=%d" % int(signal)

        # look for the axes as an attribute to the signal data
        # also find the units
        counts_attrlist=children[self.__data]
        for key in counts_attrlist.keys():
            if key=="axes":
                inner_list=(counts_attrlist[key]).split(",")
                for i in range(len(inner_list)):
                    axes[i+1]=NeXusAxis(self.__nexus,inner_list[i])
            if key=="units":
                self.units=counts_attrlist[key]

        # set the axes
        if len(axes)>0:
            self.axes=[]
        for i in range(len(axes)):
            self.axes.append(axes[i+1])
        self.variable=self.axes[0]


        self.__data_cptr = self.__get_slice(self.__data)
        if self.__data_var is not None:
            self.__data_var_cptr = self.__get_slice(self.__data_var)

    def get_variable_length(self):
        return len(self.variable.value)

    def get_block_length(self):
        return len(self.__data_cptr)

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

        if num_axes==1:
            return None
        elif num_axes==2:
            if self.axes[0]==self.variable:
                return [0,so_id[1]]
            else:
                return [so_id[1],0]
        elif num_axes==3:
            var_index=self.axes.index(self.variable)
            # Give the (i,j) part of the ID
            so_id = so_id[1]
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
            end_dim.append(1)
        var_index=self.axes.index(self.variable)
        end_dim[var_index]=num_points

        # get the value
        return self.__nexus.getslab(start_dim,end_dim)

    def get_so(self,so_id):
        import copy
        #print "retrieving",so_id # remove
        # create a spectrum object
        spectrum=SOM.SO()

        # give it the id specified
        spectrum.id=so_id

        # give it the appropriate independent variable
        spectrum.axis[0].val=copy.deepcopy(self.variable.value)

        # locate the data slice
        start_dim=self.__id_to_index(so_id)

        # set the data
        spectrum.y=self.__get_slice(self.__data,start_dim)

        # set the variance to be the data if no location is specified
        if self.__data_var==None:
            spectrum.var_y = copy.deepcopy(spectrum.y)
        else:
            spectrum.var_y=self.__get_slice(self.__data_var,start_dim)

        return spectrum

    def get_so2(self, so_id, tof_chan, num_y):
        import copy
        # create a spectrum object
        spectrum=SOM.SO()

        # give it the id specified
        spectrum.id=so_id

        # give it the appropriate independent variable
        spectrum.axis[0].val=copy.deepcopy(self.variable.value)

        # locate the data slice
        start_dim=self.__id_to_index(so_id)

        # calculate 1D indicies
        start_index = tof_chan * (start_dim[1] + (start_dim[0] * num_y))
        end_index = tof_chan + start_index

        spectrum.y=self.__data_cptr[start_index:end_index]

        # set the data
        if self.__data_var is None:
            spectrum.var_y=copy.deepcopy(spectrum.y)
        else:
            spectrum.var_y=self.__data_var_cptr[start_index:end_index]

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
            from os.path import basename
            loc = basename(self.location)
            for i in range(len(label_axes[0].value)):
                for j in range(len(label_axes[1].value)):
                    so_id=(loc,(i,j))
                    id_list.append(so_id)

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
                return len(self.axes[1])
            else:
                return len(self.axes[0])
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
        try:
            self.primary = attrs["primary"]
        except KeyError:
            self.primary = None


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


class NeXusInstrument:
    def __init__(self,filehandle,tree, **kwargs):
        # do the easy part
        import math

        try:
            from_saf = kwargs["from_saf"]
        except KeyError:
            from_saf = False

        self.__tag="/instrument"
        self.__nexus=filehandle
        self.__tree=tree
        if from_saf:
            self.__entry_locations=self.__list_type(tree,"NXinstrument")
        else:
            self.__entry_locations=self.__list_type(tree,"NXentry")
        self.__det_locations=self.__list_type(tree,"NXdetector")
        self.__mon_locations=self.__list_type(tree,"NXmonitor")

        self.__det_data={}
        self.__mon_data={}

        self.__det_info=["secondary_flight_path", "polar_angle",
                         "azimuthal_angle", "distance"]

        if not from_saf:
            self.__head_tag = self.__entry_locations[-1]+self.__tag
        else:
            self.__head_tag = self.__entry_locations[-1]
        
        self.__nexus.openpath(self.__head_tag+"/name")
        self.__inst_name=self.__nexus.getattr("short_name","")

        try:
            self.__beamline = self.__get_val_as_str(self.__head_tag
                                                    +"/beamline")
        except IOError:
            self.__beamline = None

        for location in self.__det_locations:
            label = location.split('/')[-1]
            info_list=[]
            for name in self.__det_info:
                path = location+"/"+name
                info_list.append(self.__get_value(path))
                
            self.__det_data[label]=info_list

        for location in self.__mon_locations:
            label = location.split('/')[-1]
            path = location+"/distance"
            self.__mon_data[label]=self.__get_value(path)

        self.__primary = self.__get_value(self.__head_tag+
                                          "/moderator/distance")

        # Remake tuple with primary with |distance|
        self.__primary = (math.fabs(self.__primary[0]), self.__primary[1],
                          self.__primary[2])


    def __get_value(self,path):
        try:
            self.__tree[path]
        except KeyError:
            return (None, None, None)
            
        try:
            self.__nexus.openpath(path)
        except IOError:
            return (None, None, None)

        values = self.__nexus.getdata()
        len_values = len(values)
        if len_values == 1:
            values = values[0]
        else:
            pass
        
        while True:
            (name,value)=self.__nexus.getnextattr()
            if name == None:
                break
            if name == "units":
                units = value

        errors = self.__get_errors(path)
        if errors == None:
            if len_values > 1:
                pass
            else:
                errors = 0.0
        else:
            pass
    
        return (values,errors,units)


    def __get_errors(self,path):
        path = path+"_errors"

        try:
            self.__tree[path]
        except KeyError:
            return None
            
        try:
            self.__nexus.openpath(path)
        except IOError:
            return None

        return self.__nexus.getdata()
    
        
    def __list_type(self,tree,type):
        my_list=[]
        for key in tree.keys():
            if tree[key]==type:
                my_list.append(key)
        return my_list


    def __get_val_as_str(self,path):
        self.__nexus.openpath(path)
        return str(self.__nexus.getdata())


    def getName(self):
        return self.__inst_name


    def getBeamline(self):
        return self.__beamline
    

    def getInstrument(self, path, **kwargs):

        try:
            from_saf = kwargs["from_saf"]
        except KeyError:
            from_saf = False
        
        label = path.split('/')[-1]

        # Check the monitor list
        flag = False
        try:
            geometry = self.__mon_data[label]
            # Add monitor distance to |moderator distance| to get correct
            # distance and recreate tuple
            geometry = (self.__primary[0] + geometry[0], geometry[1])
            return SOM.Instrument(primary=geometry)
        except KeyError:
            flag = True
            
        # Check the detector list
        try:
            az_selector = None
            pol_selector = None
            sec_selector = None

            instname = self.__inst_name
            extra_stuff = None
            
            geometry = self.__det_data[label]

            # Secondary flight path versus distance checks
            if geometry[0][0] == None:
                distance = geometry[3][0]
            else:
                distance = geometry[0][0]

            if geometry[0][1] == None:
                distance_err2 = geometry[3][1]
            else:
                distance_err2 = geometry[0][1]

            if self.__inst_name == "BSS":
                if label == "bank3":
                    instname = "BSS_diff"
                    if from_saf:
                        dis_path = "/instrument-diffraction/"+label+"/distance"
                        pol_path = "/instrument-diffraction/"+label\
                                   +"/polar_angle"
                        az_path = "/instrument-diffraction/"+label\
                                   +"/azimuthal_angle"                        
                    else:
                        dis_path = "/entry-diff/instrument/"+label+"/distance"
                        pol_path = "/entry-diff/instrument/"+label\
                                   +"/polar_angle"
                        az_path = "/entry-diff/instrument/"+label\
                                   +"/azimuthal_angle"                        

                    self.__nexus.openpath(dis_path)
                    dims = self.__nexus.getdims()
                    extra_stuff = dims[0][1]
                    self.__nexus.openpath(pol_path)
                    dims = self.__nexus.getdims()
                    if len(dims[0]) < 2:
                        pol_selector = "ISelector"
                    self.__nexus.openpath(az_path)
                    dims = self.__nexus.getdims()
                    if len(dims[0]) < 2:
                        az_selector = "JSelector"
                    
                else:
                    if from_saf:
                        path = "/instrument-inelastic/"+label+"/polar_angle"
                    else:
                        path = "/entry/instrument/"+label+"/polar_angle"
                    self.__nexus.openpath(path)
                    dims = self.__nexus.getdims()
                    if len(dims[0]) < 2:
                        pol_selector = "ISelector"
                    else:
                        extra_stuff = dims[0][1]
            elif self.__inst_name == "REF_M" or self.__inst_name == "REF_L"\
                     or self.__inst_name == "GLAD":
                instname = self.__inst_name
                if from_saf:
                    path = "/instrument/"+label+"/distance"
                else:
                    path = "/entry/instrument/"+label+"/distance"
                self.__nexus.openpath(path)
                dims = self.__nexus.getdims()
                extra_stuff = dims[0][1]
            else:
                pass

            return SOM.Instrument(instrument=instname,
                                  primary=(self.__primary[0],
                                           self.__primary[1]),
                                  secondary=distance,
                                  secondary_err2=distance_err2,
                                  secondary_selector=sec_selector,
                                  polar=geometry[1][0],
                                  polar_err2=geometry[1][1],
                                  polar_selector=pol_selector,
                                  azimuthal=geometry[2][0],
                                  azimuthal_err2=geometry[2][1],
                                  azimuthal_selector=az_selector,
                                  extra=extra_stuff)
        except KeyError:
            flag = True

        # No label found in monitor or detector list
        if flag:
            return None

class SnsInformation:
    def __init__(self, filehandle, tree, inst_name):
        self.__tag = "/instrument"
        self.__nexus = filehandle
        self.__tree = tree
        self.__inst_name = inst_name

        self.__entry_locations = self.__list_type(tree,"NXentry")
        self.__det_locations = self.__list_type(tree,"NXdetector")
        self.__det_data={}

        self.__head_tag = self.__entry_locations[-1]+self.__tag
        
        if self.__inst_name == "BSS":

            self.__det_locations.extend(self.__list_type(tree,"NXcrystal"))

            SOM_keys = {"analyzer" : ["Wavelength_final"],
                        "bank" : ["Initial_energy_offset",
                                  "Final_energy_offset"]}
            data_loc = {"analyzer" : ["wavelength"],
                        "bank" : ["initial_energy_offset",
                                  "final_energy_offset"]}

            index_sel = {"analyzer" : ["JSelector"],
                         "bank" : ["IJSelector", "IJSelector"]}

            self.__get_data(SOM_keys, data_loc, index_sel)

        else:
            self.__det_data = {None : (None, None, None)}

    def __get_data(self, keys, data, selectors):
        import re

        expression = r'\d+$'
        myre = re.compile(expression)

        for location in self.__det_locations:
            label = location.split('/')[-1]

            if self.__inst_name == "BSS" and label == "bank3":
                continue
            else:
                pass

            value = myre.split(label)[0]
            number = label.split(value)[-1]
            for key, dpath, sel in map(None, keys[value], data[value],
                                       selectors[value]):
                if not self.__det_data.has_key(key):
                    self.__det_data[key] = []
                else:
                    pass
                    
                path = location + "/" + dpath
                info = (self.__get_value(path))
                bank_label = "bank" + number

                self.__det_data[key].append(bank_label)

                if sel == "IJSelector":
                    try:
                        self.__nexus.openpath(path)
                        dims = self.__nexus.getdims()
                        try:
                            dim = dims[0][1]
                            self.__det_data[key].append(\
                                SOM.Information(info[0],
                                                info[1],
                                                info[2],
                                                sel,
                                                Nj=dim))
                        except IndexError:
                            self.__det_data[key].append(None)
                            
                    except IOError:
                        self.__det_data[key].append(None)
                else:
                    self.__det_data[key].append(SOM.Information(info[0],
                                                                info[1],
                                                                info[2],
                                                                sel))

    def __get_value(self,path):
        try:
            self.__tree[path]
        except KeyError:
            return (None, None, None)
            
        try:
            self.__nexus.openpath(path)
        except IOError:
            return (None, None, None)

        values = self.__nexus.getdata()
        len_values = len(values)
        if len_values == 1:
            values = values[0]
        else:
            pass
        
        while True:
            (name,value)=self.__nexus.getnextattr()
            if name == None:
                break
            if name == "units":
                units = value

        errors = self.__get_errors(path)
        if errors == None:
            if len_values > 1:
                pass
            else:
                errors = 0.0
        else:
            pass
    
        return (values,errors,units)


    def __get_errors(self,path):
        path = path+"_errors"

        try:
            self.__tree[path]
        except KeyError:
            return None
            
        try:
            self.__nexus.openpath(path)
        except IOError:
            return None

        return self.__nexus.getdata()
    
        
    def __list_type(self,tree,type):
        my_list=[]
        for key in tree.keys():
            if tree[key]==type:
                my_list.append(key)
        return my_list


    def __get_val_as_str(self,path):
        self.__nexus.openpath(path)
        return str(self.__nexus.getdata())


    def getKeys(self):
        try:
            return self.__det_data.keys()
        except AttributeError:
            return None

    def getInformation(self, key):
        try:
            return self.__det_data[key]
        except KeyError:
            return None

###############################################################################
#
# This class creates a 3 column ASCII file with a metadata header. The
# formatting is based on spec
# (http://www.certif.com/spec_manual/user_1_4_1.html) file format.
#
# $Id$
#
###############################################################################

import dst_base
import math
import sys

class Ascii3ColDST(dst_base.DST_BASE):
    MIME_TYPE="text/Spec"
    EMPTY=""
    SPACE=" "
    COLUMNS=3
    
    ########## DST_BASE functions

    def __init__(self, resource, *args, **kwargs):
        import time
        
        self.__file = resource
        self.__epoch = time.time()
        self.__timestamp = time.strftime("%Y-%m-%d %T", \
                                         time.localtime(self.__epoch))

    def release_resource(self):
        self.__file.close()


    def writeSO(self,so):
        self.writeData(so)


    def writeSOM(self,som):
        self.__data_type = som.getDataSetType()
        self.writeHeader(som)
        self.__counter = 1
        for so in som:
            self.writeData(so)

    ########## Special functions

    def __formatDataInfo(self,som):
        # Need SO for primary axis information
        so = som[0]
        dim = som.getDimension()

        if dim != so.dim():
            raise RuntimeError, "SOM and attending SOs do not have the same"\
                  +" dimensions"

        names = []
        result = "#L ";
        # Add primary axis format positions
        for i in range(dim):
            result += "%s(%s) "
            names.append(som.getAxisLabel(i))
            names.append(som.getAxisUnits(i))
            if so.axis[i].var != None:
                result += "Sigma(%s) "
                names.append(som.getAxisUnits(i))

        # Add y and var_y axis format positions
        result += "%s(%s) Sigma(%s)"
        names.append(som.getYLabel())
        names.append(som.getYUnits())
        names.append(som.getYUnits())

        return (result, tuple(names))

    def writeHeader(self,som):
        try:
            som.attr_list["filename"].reverse()
            som.attr_list["filename"].reverse()
            for file in som.attr_list["filename"]:
                print >> self.__file, "#F", file
        except AttributeError:
            print >> self.__file, "#F",som.attr_list["filename"]

        print >> self.__file, "#E",self.__epoch
        print >> self.__file, "#D",self.__timestamp
        
        if som.attr_list.has_key("run_number"):
            print >> self.__file, "#C Run Number:",som.attr_list["run_number"]
        else:
            pass
        
        print >> self.__file, "#C Title:",som.getTitle()
        if som.attr_list.has_key("notes"):
            print >> self.__file, "#C Notes:", som.attr_list["notes"]
        else:
            pass

        if som.attr_list.has_key("username"):
            print >> self.__file, "#C User:",som.attr_list["username"]
        else:
            pass

        if som.attr_list.has_key("detector_angle"):
            print >> self.__file, "#C Detector Angle:",\
                  som.attr_list["detector_angle"]
        else:
            pass
        
        if som.attr_list.has_key("operations"):
            for op in som.attr_list["operations"]:
                print >> self.__file, "#C Operation",op
        else:
            pass
        
        if som.attr_list.has_key("parents"):
            print >> self.__file, "#C Parent Files"
            pdict = som.attr_list["parents"]
            for key in pdict:
                print >> self.__file, "#C %s: %s" % (key, pdict[key]) 
        else:
            pass

        if som.attr_list.has_key("proton_charge"):
            print >> self.__file, "#C Proton Charge:",\
                  str(som.attr_list["proton_charge"])
        else:
            pass
                
        
        (format_str, names) = self.__formatDataInfo(som)
        self.__axes_and_units =  format_str % names


    def writeData(self,so):
        print >> self.__file, self.EMPTY
        print >> self.__file, "#S",self.__counter,"Spectrum ID",so.id
        print >> self.__file, "#N", self.COLUMNS
        print >> self.__file, self.__axes_and_units
        so_y_len=len(so.y)

        size = so_y_len
        if self.__data_type == "" or self.__data_type == "histogram":
            size += 1
        # Density data does not need to be incremented by one
        else:
            pass
        
        for i in range(size):
            dim = so.dim()
            for j in range(dim):
                print >> self.__file, so.axis[j].val[i],self.SPACE,
                if so.axis[j].var != None:
                    print >> self.__file, \
                          math.sqrt(math.fabs(so.axis[j].var[i])),self.SPACE,
            
            if i < so_y_len:
                print >> self.__file, so.y[i],self.SPACE,
                print >> self.__file, math.sqrt(math.fabs(so.var_y[i]))
            else:
                print >> self.__file, self.EMPTY

        self.__counter += 1

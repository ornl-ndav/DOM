#                        Data Object Model
#           A part of the SNS Analysis Software Suite.
#
#                  Spallation Neutron Source
#          Oak Ridge National Laboratory, Oak Ridge TN.
#
#
#                             NOTICE
#
# For this software and its associated documentation, permission is granted
# to reproduce, prepare derivative works, and distribute copies to the public
# for any purpose and without fee.
#
# This material was prepared as an account of work sponsored by an agency of
# the United States Government.  Neither the United States Government nor the
# United States Department of Energy, nor any of their employees, makes any
# warranty, express or implied, or assumes any legal liability or
# responsibility for the accuracy, completeness, or usefulness of any
# information, apparatus, product, or process disclosed, or represents that
# its use would not infringe privately owned rights.
#

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
import dst_utils
import math
import sys

class Ascii3ColDST(dst_base.DST_BASE):
    MIME_TYPE="text/Spec"
    EMPTY=""
    SPACE=" "
    
    ########## DST_BASE functions

    def __init__(self, resource, *args, **kwargs):
        import time
        
        self.__file = resource
        self.__epoch = time.time()
        self.__columns = 0

    def release_resource(self):
        self.__file.close()

    def writeSO(self,so):
        self.writeData(so)

    def writeSOM(self, som, **kwargs):
        self.__data_type = som.getDataSetType()
        try:
            extra_som = kwargs["extra_som"]
        except KeyError:
            extra_som = None

        if extra_som is not None and \
               self.__data_type != extra_som.getDataSetType():
            raise RuntimeError("The SOMs are not the same data type: "\
                           +"%s, extra_som=%s" % (self._data_type,
                                                  extra_som.getDataSetType()))
        
        dst_utils.write_spec_header(self.__file, self.__epoch, som)
        (format_str, names) = self.__formatDataInfo(som, extra_som)
        self.__axes_and_units =  format_str % names
        self.__counter = 1
        if extra_som is None:
            for so in som:
                self.writeData(so)
        else:
            import itertools
            for so_tuple in itertools.izip(som, extra_som):
                self.writeData(so_tuple[0], so_tuple[1])

    ########## Special functions

    def __dataSelfCheck(self, som):
        # Need SO for primary axis information
        so = som[0]
        dim = som.getDimension()

        if dim != so.dim():
            raise RuntimeError("SOM and attending SOs do not have the same"\
                               +" dimensions")

    def __formatDataInfo(self,som,som1=None):
        self.__dataSelfCheck(som)

        names = []
        result = ["#L"];

        if som1 is not None:
            self.__dataSelfCheck(som1)
            (names, result) = self.__setPrimaryAxisInfo(som1.getDimension(),
                                                        som1, som1[0],
                                                        names, result)

        (names, result) = self.__setPrimaryAxisInfo(som.getDimension(), som,
                                                    som[0], names, result)

        # Add y and var_y axis format positions
        result.append("%s(%s) Sigma(%s)")
        names.append(som.getYLabel())
        names.append(som.getYUnits())
        names.append(som.getYUnits())
        self.__columns += 2

        return (self.SPACE.join(result), tuple(names))

    def __setPrimaryAxisInfo(self, dim, som, so, names, result):
        # Add primary axis format positions
        for i in range(dim):
            self.__columns += 1
            result.append("%s(%s)")
            names.append(som.getAxisLabel(i))
            names.append(som.getAxisUnits(i))
            if so.axis[i].var != None:
                self.__columns += 1
                result.append("Sigma(%s)")
                names.append(som.getAxisUnits(i))

        return (names, result)

    def writeData(self, so, so1=None):
        print >> self.__file, self.EMPTY
        print >> self.__file, "#S",self.__counter,"Spectrum ID",so.id
        print >> self.__file, "#N", self.__columns
        print >> self.__file, self.__axes_and_units
        so_y_len=len(so.y)

        size = so_y_len
        if self.__data_type == "" or self.__data_type == "histogram":
            size += 1
        # Density data does not need to be incremented by one
        else:
            pass
        
        for i in range(size):
            if so1 is not None:
                dim1 = so1.dim()
                for k in range(dim1):
                    print >> self.__file, so1.axis[k].val[i],self.SPACE,
                    if so1.axis[k].var is not None:
                        print >> self.__file, \
                              math.sqrt(math.fabs(so1.axis[k].var[i])),
            
            dim = so.dim()
            for j in range(dim):
                print >> self.__file, so.axis[j].val[i],self.SPACE,
                if so.axis[j].var is not None:
                    print >> self.__file, \
                          math.sqrt(math.fabs(so.axis[j].var[i])),self.SPACE,

            if i < so_y_len:
                print >> self.__file, so.y[i],self.SPACE,
                print >> self.__file, math.sqrt(math.fabs(so.var_y[i]))
            else:
                print >> self.__file, self.EMPTY

        self.__counter += 1

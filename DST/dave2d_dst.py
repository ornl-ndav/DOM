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
# This class creates a DAVE 2d ASCII file with a metadate header. The
# formatting is based on what is found here:
# http://www.ncnr.nist.gov/dave/documentation/ascii_help.pdf
#
# $Id$
#
###############################################################################

import dst_base
import dst_utils
import math

class Dave2dDST(dst_base.DST_BASE):
    MIME_TYPE="text/Dave2d"
    EMPTY=""
    SPACE=" "

    ########## DST_BASE functions

    def __init__(self, resource, *args, **kwargs):
        import time
        
        self.__file = resource
        self.__epoch = time.time()

    def release_resource(self):
        self.__file.close()

    def writeSO(self,so):
        self.writeData(so)


    def writeSOM(self,som):
        self.writeXValues(som)
        self.writeData(som[0])
        dst_utils.write_spec_header(self.__file, self.__epoch, som)

    ########## Special functions

    def writeXValues(self,som):
        so = som[0]
        len_x1 = len(so.axis[1].val) - 1
        len_x2 = len(so.axis[0].val) - 1

        print >> self.__file, "# Number of",som.getAxisLabel(1),"values"
        print >> self.__file, len_x1
        print >> self.__file, "# Number of",som.getAxisLabel(0),"values"
        print >> self.__file, len_x2

        print >> self.__file, "#",som.getAxisLabel(1),"Values:"
        for i in range(len_x1):
            print >> self.__file, so.axis[1].val[i] + \
                  (so.axis[1].val[i+1] - so.axis[1].val[i])/ 2.0

        print >> self.__file, "#",som.getAxisLabel(0),"Values:"
        for i in range(len_x2):
            print >> self.__file, so.axis[0].val[i] + \
                  (so.axis[0].val[i+1] - so.axis[0].val[i]) / 2.0
        

    def writeData(self,so):
        len_x1 = len(so.axis[0].val) - 1
        len_x2 = len(so.axis[1].val) - 1

        for i in range(len_x1):
            print >> self.__file, "# Group", i
            slice_y = so.y[i*len_x2:((i+1)*len_x2)]
            slice_var_y = so.var_y[i*len_x2:((i+1)*len_x2)] 

            for (y,var_y) in map(None,slice_y,slice_var_y):
                print >> self.__file, y, self.SPACE, \
                      math.sqrt(math.fabs(var_y))

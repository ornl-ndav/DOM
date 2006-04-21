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
        self.__timestamp = dst_utils.make_ISO8601(time.time())

    def release_resource(self):
        self.__file.close()


    def writeSO(self,so):
        self.writeData(so)


    def writeSOM(self,som):
        self.writeHeader(som)
        self.writeXValues(som)
        self.writeData(som[0])

    ########## Special functions

    def writeHeader(self,som):
        print >> self.__file, "# Filename:",som.attr_list["filename"]
        print >> self.__file, "# Key:", dst_utils.make_magic_key()
        print >> self.__file, "# Creation Time:",self.__timestamp
        if som.attr_list.has_key("run_number"):
            print >> self.__file, "# Run Number:",som.attr_list["run_number"]
        print >> self.__file, "# Title:",som.getTitle()
        if som.attr_list.has_key("username"):
            print >> self.__file, "# User:",som.attr_list["username"]
        if som.attr_list.has_key("operations"):
            for op in som.attr_list["operations"]:
                print >> self.__file, "# Operation",op
        if som.attr_list.has_key("parents"):
            print >> self.__file, "# Parent Files"
            pdict = som.attr_list["parents"]
            for key in pdict:
                print >> self.__file, "#%s: %s" % (key, pdict[key]) 


    def writeXValues(self,som):
        so = som[0]
        len_x1 = len(so.axis[1].val) - 1
        len_x2 = len(so.axis[0].val) - 1

        print >> self.__file, "# Number of",som.getAxisLabel(1),"values"
        print >> self.__file, len_x1
        print >> self.__file, "# Number of",som.getAxisLabel(0),"values"
        print >> self.__file, len_x2

        print >> self.__file, som.getAxisLabel(1),"Values:"
        for i in range(len_x1):
            print >> self.__file, so.axis[1].val[i] + \
                  (so.axis[1].val[i+1] - so.axis[1].val[i])/ 2.0

        print >> self.__file, som.getAxisLabel(0),"Values:"
        for i in range(len_x2):
            print >> self.__file, so.axis[0].val[i] + \
                  (so.axis[0].val[i+1] - so.axis[0].val[i]) / 2.0
        

    def writeData(self,so):
        len_x1 = len(so.axis[0].val) - 1
        len_x2 = len(so.axis[1].val) - 1

        for i in range(len_x1):
            print >> self.__file, "#Group", i
            slice_y = so.y[i*len_x2:((i+1)*len_x2)]
            slice_var_y = so.var_y[i*len_x2:((i+1)*len_x2)] 

            for (y,var_y) in map(None,slice_y,slice_var_y):
                print >> self.__file, y, self.SPACE, \
                      math.sqrt(math.fabs(var_y))

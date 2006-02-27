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
    COLUMNS=3
    
    ########## DST_BASE functions

    def __init__(self, resource, *args, **kwargs):
        self.__file = resource


    def release_resource(self):
        self.__file.close()


    def writeSO(self,so):
        self.writeData(so)


    def writeSOM(self,som):
        self.writeHeader(som)
        for so in som:
            self.writeData(so)

    ########## Special functions

    def writeHeader(self,som):
        print >> self.__file, "#F",som.attr_list["filename"]
        print >> self.__file, "#E",som.attr_list["epoch"]
        print >> self.__file, "#D",som.attr_list["timestamp"]
        print >> self.__file, "#C Title:",som.attr_list["title"]
        print >> self.__file, "#C User:",som.attr_list["username"]

        self.__axes_and_units = "#L TOF(%s) Counts(%s) Sigma(%s)" \
        % (som.attr_list["x_units"], som.attr_list["y_units"],
         som.attr_list["y_units"])

    def writeData(self,so):
        print >> self.__file, self.EMPTY
        print >> self.__file, "#S",so.id+1,"Pixel",so.id
        print >> self.__file, "#N", self.COLUMNS
        print >> self.__file, self.__axes_and_units
        for i in range(len(so)+1):
            print >> self.__file, so.x[i]," ",
            if i < len(so.y):
                print >> self.__file, so.y[i]," ",
                print >> self.__file, math.sqrt(so.var_y[i])
            else:
                print >> self.__file, self.EMPTY


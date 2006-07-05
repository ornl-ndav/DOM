###############################################################################
#
# This class creates a GSAS ASCII file.
#
# $Id$
#
###############################################################################

import dst_base

class GsasDST(dst_base.DST_BASE):
    MIME_TYPE="text/GSAS"
    EMPTY=""
    SPACE=" "

    ########## DST_BASE functions

    def __init__(self, resource, *args, **kwargs):
        self.__file = resource

    def release_resource(self):
        self.__file.close()

    def writeSO(self,so):
        self.writeData(so)

    def writeSOM(self,som):
        self.writeHeader(som)
        self.writeData(som[0])

    ########## Special functions

    def writeHeader(self,som):
        nchan = len(som[0]) + 1
        nrec = int(nchan / 10) + 1
        
        offset = som[0].axis[0].val[0]
        binwidth = som[0].axis[0].val[1] - offset
        
        print >> self.__file, som.getTitle().ljust(80)
        print >> self.__file, "BANK 1 %d %d CONST %f %f 0 0 STD" % \
              (nchan, nrec, offset, binwidth)

    def writeData(self,so):
        counter = 0
        values = []
        format_str = "%8d%8d%8d%8d%8d%8d%8d%8d%8d%8d"
        for y in so.y:
            if counter < 10:
                values.append(int(y))
                counter += 1
            elif counter == 10:
                print >> self.__file, format_str % tuple(values)

                counter = 0
                values = []
            else:
                pass

        if counter < 10:
            pad = 10 - counter
            for i in range(pad):
                values.append(0)
        else:
            pass

        print >> self.__file, format_str % tuple(values)


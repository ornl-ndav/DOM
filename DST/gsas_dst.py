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


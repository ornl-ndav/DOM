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

# $Id$

import dst_base

class GsasDST(dst_base.DST_BASE):
    """
    This class creates a GSAS ASCII file.

    @cvar MIME_TYPE: The MIME-TYPE of the class
    @type MIME_TYPE: C{string}
    
    @cvar EMPTY: Variable for holding an empty string
    @type EMPTY: C{string}
    
    @cvar SPACE: Variable for holding a space
    @type SPACE: C{string}

    @ivar __file: The handle to the output data file
    @type __file: C{file}    
    """
    
    MIME_TYPE = "text/GSAS"
    EMPTY = ""
    SPACE = " "

    ########## DST_BASE functions

    def __init__(self, resource, *args, **kwargs):
        """
        Object constructor

        @param resource: The handle to the output data file
        @type resource: C{file}

        @param args: Argument objects that the class accepts (UNUSED)

        @param kwargs: A list of keyword arguments that the class accepts:
        """        
        self.__file = resource

    def release_resource(self):
        """
        This method closes the file handle to the output file.
        """        
        self.__file.close()

    def writeSO(self, so):
        """
        This method writes the L{SOM.SO} information to the output file.

        @param so: The object to have its information written to file.
        @type so: L{SOM.SO}
        """        
        self.writeData(so)

    def writeSOM(self, som):
        """
        This method writes the L{SOM.SOM} information to the output file.

        @param som: The object to have its information written to file.
        @type som: L{SOM.SOM}
        """        
        self.writeHeader(som)
        self.writeData(som[0])

    ########## Special functions

    def writeHeader(self, som):
        """
        This method writes the information in the L{SOM.SOM} to the file
        header.

        @param som: The object containing the information for the header 
        @type som: L{SOM.SOM}
        """
        nchan = len(som[0]) + 1
        nrec = int(nchan / 10) + 1
        
        offset = som[0].axis[0].val[0]
        binwidth = som[0].axis[0].val[1] - offset
        
        print >> self.__file, som.getTitle().ljust(80)
        print >> self.__file, "BANK 1 %d %d CONST %f %f 0 0 STD" % \
              (nchan, nrec, offset, binwidth)

    def writeData(self, so):
        """
        This method is responsible for writing the actual data contained within
        the L{SOM.SO}s to the attached file. 

        @param so: Object containing data to be written to file
        @type so: L{SOM.SO}
        """        
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


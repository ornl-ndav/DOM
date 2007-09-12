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
import dst_utils
import math

class Dave2dDST(dst_base.DST_BASE):
    """
    This class creates a DAVE 2D ASCII file with a metadata footer. The
    formatting is based on what is found
    U{here<http://www.ncnr.nist.gov/dave/documentation/ascii_help.pdf>}.
    
    @cvar MIME_TYPE: The MIME-TYPE of the class
    @type MIME_TYPE: C{string}
    
    @cvar EMPTY: Variable for holding an empty string
    @type EMPTY: C{string}
    
    @cvar SPACE: Variable for holding a space
    @type SPACE: C{string}

    @ivar __file: The handle to the output data file
    @type __file: C{file}

    @ivar __epoch: The epoch (UNIX time) when the object was instantiated.
                   This is used as the creation time of the file information.
    @type __epoch: C{string} 
    """
    
    MIME_TYPE = "text/Dave2d"
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
        import time
        
        self.__file = resource
        self.__epoch = time.time()

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
        This method writes the L{SOM.SOM} information to the output file. The
        C{SOM.SOM} carries only one C{SOM.SO} that has a 2-dimensional spectrum
        contained in it.

        @param som: The object to have its information written to file.
        @type som: L{SOM.SOM}
        """
        self.writeXValues(som)
        self.writeData(som[0])
        dst_utils.write_spec_header(self.__file, self.__epoch, som)

    ########## Special functions

    def writeXValues(self, som):
        """
        This method is responsible for writing the values of the two
        independent axes to the file. The values must be converted to bin
        centers.
        
        @param som: The object containing the information about the independent
                    axes.
        @type som: L{SOM.SOM}
        """
        so = som[0]
        len_x1 = len(so.axis[1].val) - 1
        len_x2 = len(so.axis[0].val) - 1

        print >> self.__file, "# Number of", som.getAxisLabel(1), "values"
        print >> self.__file, len_x1
        print >> self.__file, "# Number of", som.getAxisLabel(0), "values"
        print >> self.__file, len_x2

        print >> self.__file, "#", som.getAxisLabel(1), "Values:"
        for i in range(len_x1):
            print >> self.__file, so.axis[1].val[i] + \
                  (so.axis[1].val[i+1] - so.axis[1].val[i]) / 2.0

        print >> self.__file, "#", som.getAxisLabel(0), "Values:"
        for i in range(len_x2):
            print >> self.__file, so.axis[0].val[i] + \
                  (so.axis[0].val[i+1] - so.axis[0].val[i]) / 2.0
        
    def writeData(self, so):
        """
        This method is responsible for writing the actual data contained within
        the L{SOM.SO}s to the attached file. 

        @param so: Object containing data to be written to file
        @type so: L{SOM.SO}
        """        
        len_x1 = len(so.axis[0].val) - 1
        len_x2 = len(so.axis[1].val) - 1

        for i in range(len_x1):
            print >> self.__file, "# Group", i
            slice_y = so.y[i*len_x2:((i+1)*len_x2)]
            slice_var_y = so.var_y[i*len_x2:((i+1)*len_x2)] 

            for (y, var_y) in map(None, slice_y, slice_var_y):
                print >> self.__file, y, self.SPACE, \
                      math.sqrt(math.fabs(var_y))

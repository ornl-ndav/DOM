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

class PhxDST(dst_base.DST_BASE):
    """
    This class creates a so-called PHX file for programs like MSlice. The first
    row in the file is the total number of pixels present in the output file.
    Each pixel is then given a separate line in the file. The columns are
    arranged with the following information:
      1. Historically redundant info (set to 1)
      2. Historically redundant info (set to 0)
      3. Polar angle (AKA TwoTheta)
      4. Azimuthal angle
      5. Delta polar
      6. Delta azimuthal
      7. Historically redundant info (set to 0)

    @cvar MIME_TYPE: The MIME-TYPE of the class
    @type MIME_TYPE: C{string}
    
    @cvar EMPTY: Variable for holding an empty string
    @type EMPTY: C{string}
    
    @cvar SPACE: Variable for holding a space
    @type SPACE: C{string}
    """

    MIME_TYPE = "text/PHX"
    EMPTY = ""
    SPACE = " "

    ########## DST_BASE functions

    def __init__(self, resource):
        """
        Object constructor

        @param resource: The handle to the output data file
        @type resource: C{file}
        """
        self.__file = resource

    def release_resource(self):
        """
        This method closes the file handle to the output file.
        """
        self.__file.close()

    def writeSOM(self, som, **kwargs):
        """
        This method writes the L{SOM.SOM} information to the output file.

        @param som: The object to have its information written to file.
        @type som: L{SOM.SOM}

        @param kwargs: A list of keyword arguments that the method accepts:
        """
        pass

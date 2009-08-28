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
import nxs

class RedNxsDST(dst_base.DST_BASE):
    """
    This class creates a HDF5-based reduced
    U{NeXus<http://www.nexusformat.org>} file.

    @cvar MIME_TYPE: The MIME-TYPE of the class
    @type MIME_TYPE: C{string}

    @ivar __file: The handle to the output data file
    @type __file: C{file}
    """

    MIME_TYPE = "application/x-RedNxs"

    ########## DST_BASE functions

    def __init__(self, resource, *args, **kwargs):
        """
        Object constructor

        @param resource: The handle to the input NeXus geometry file
        @type resource: C{file}

        @param args: Argument objects that the class accepts (UNUSED)

        @param kwargs: A list of keyword arguments that the class accepts:
        """
        self.__file = nxs.open(resource, nxs.napi.ACC_CREATE5)

    def release_resource(self):
        """
        This method closes the file handle to the output file.
        """
        self.__file.close()

    def writeSOM(self, som):
        pass

    ##### Methods not implemented
    # ----- inspection
    def get_SO_ids(self, som_id):
        """
        Method to get L{SOM.SO} IDs. 
        """
        raise NotImplementedError

    def get_SOM_ids(self):
        """
        Method to get L{SOM.SOM} IDs. 
        """
        raise NotImplementedError

    # ----- read information
    def getSO(self, som_id, so_id):
        """
        Retrieve a L{SOM.SO} from given L{SOM.SOM} and L{SOM.SO} IDs.        
        """
        raise NotImplementedError

    def getSOM(self, som_id):
        """
        Retrieve a L{SOM.SOM} for a given L{SOM.SOM} ID.
        """
        raise NotImplementedError

    # ----- write information
    def writeSO(self, so):
        """
        Method to write the L{SOM.SO} information to the resource.
        """
        raise NotImplementedError

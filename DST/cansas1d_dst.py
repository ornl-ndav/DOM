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

class CanSas1dDST(dst_base.DST_BASE):
    """
    This class creates a CanSAS 1D format file. This file is based on the
    schema specification found U{here<>}.

    @cvar MIME_TYPE: The MIME-TYPE of the class
    @type MIME_TYPE: C{string}

    @ivar __file: The handle to the output data file
    @type __file: C{file}

    """
    MIME_TYPE = "text/canSAS"

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

    def writeSOM(self, som):
        """
        This method writes the L{SOM.SOM} information to the output file.

        @param som: The object to have its information written to file.
        @type som: L{SOM.SOM}
        """
        pass
        

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

class Roi(object):
    """
    This class handles collecting region-of-interest (ROI) information from
    a file and generating a list of L{NeXusId}s.

    @ivar __id_list: The list of ROI identifiers
    @type __id_list: C{list}
    """

    def __init__(self, filename):
        """
        Object constructor

        @param filename: Name of the ROI file
        @type filename: C{string}
        """
        import SOM
        
        self.__id_list = []

        try:
            roi_file = open(filename, "r")
        except IOError:
            raise RuntimeError("Cannot open roi file %s" % filename)

        for line in roi_file:
            if line.startswith("#"):
                continue

            self.__id_list.append(SOM.NeXusId.fromString(line.rstrip()))
        
    def __iter__(self):
        """
        Iteration method
        """
        return self.__id_list.__iter__()

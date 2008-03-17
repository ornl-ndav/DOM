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

class NeXusId(object):
    """
    This class represents the pixel ID as retreived from the NeXus file
    when written out to a data reduction output file.

    @ivar __det_id: The identification tag of the detector in the NeXus file
    @type __det_id: C{string}

    @ivar __x_index: The x index in the 2D detector data representation
    @type __x_index: C{int}

    @ivar __y_index: The y index in the 2D detector data representation
    @type __y_index: C{int}    
    """

    def __init__(self, det_id, x_idx, y_idx):
        """
        Object constructor

        @param det_id: The detector ID to set for the NeXusId
        @type det_id: C{string}

        @param x_idx: The x index position of the detector
        @type x_idx: C{int}

        @param y_idx: The y index position of the detector
        @type y_idx: C{int}        
        """
        self.__det_id = det_id
        self.__x_index = int(x_idx)
        self.__y_index = int(y_idx)

    def getDetId(self):
        """

        """
        return self.__det_id

    def getXindex(self):
        """

        """
        return self.__x_index

    def getYindex(self):
        """

        """
        return self.__y_index    

    def toTuple(self):
        """
        This method creates a built-in object representation of the ID.

        @return: The ID as a built-in object
        @rtype: C{tuple}
        """
        return (self.__det_id, (self.__x_index, self.__y_index))

    def fromList(cls, ilist):
        """

        """
        if len(ilist) != 3:
            raise RuntimeError("Cannot create NeXus ID from %s. Must have "\
                               +"three pieces of information" \
                               % " ".join(ilist))

        det_id = ilist[0].lstrip('(').rstrip(',').strip('\'')
        x_idx = ilist[1].lstrip('(').rstrip(',')
        y_idx = ilist[2].rstrip(')')
        
        return NeXusId(det_id, x_idx, y_idx)

    fromList = classmethod(fromList)

    def fromString(cls, istr):
        """

        """
        parts = istr.split()
        return NeXusId.fromList(parts)

    fromString = classmethod(fromString)

    

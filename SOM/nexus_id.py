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

    def __eq__(self, right):
        """
        This method detemines if to L{NeXusId} instances are equal.

        @param right: The other object to check
        @type right: L{NeXusId}


        @return: Whether or not the two L{NeXusId}s are equal
        @rtype: C{boolean}
        """
        return (self.__det_id == right.getDetId() and \
                self.__x_index == right.getXindex() and \
                self.__y_index == right.getYindex())

    def __neq__(self, right):
        """
        This method detemines if to L{NeXusId} instances are not equal.

        @param right: The other object to check
        @type right: L{NeXusId}


        @return: Whether or not the two L{NeXusId}s are not equal
        @rtype: C{boolean}
        """
        return not self.__eq__(right)

    def __str__(self):
        """
        This method returns the string representation of the information
        held by the object. It has the format: (bankN, (x, y)).


        @return: The object information
        @rtype: C{string}
        """
        return str((self.__det_id, (self.__x_index, self.__y_index)))

    def getDetId(self):
        """
        This method returns the detector ID.

        @return: The detector ID
        @rtype: C{string}
        """
        return self.__det_id

    def getXindex(self):
        """
        This method returns the x index of the detector ID.

        @return: The x index
        @rtype: C{int}
        """
        return self.__x_index

    def getYindex(self):
        """
        This method returns the y index of the detector ID.

        @return: The y index
        @rtype: C{int}
        """
        return self.__y_index

    def isDetIdEqual(self, detid):
        """
        This method determines if the given detector ID is equal to the one in
        the current instance.

        @param detid: The given detector ID
        @type detid: C{string}


        @return: Whether or not the detector IDs are equal
        @rtype: C{boolean}
        """
        return self.__det_id == detid

    def isXidxEqual(self, xid):
        """
        This method determines if the given x index is equal to the one in
        the current instance.

        @param xid: The given x index
        @type xid: C{string}


        @return: Whether or not the x indexes are equal
        @rtype: C{boolean}
        """
        return self.__x_index == xid

    def isYidxEqual(self, yid):
        """
        This method determines if the given y index is equal to the one in
        the current instance.

        @param yid: The given y index
        @type yid: C{string}


        @return: Whether or not the y indexes are equal
        @rtype: C{boolean}
        """        
        return self.__y_index == yid

    def toTuple(self):
        """
        This method creates a built-in object representation of the ID.

        @return: The ID as a built-in object
        @rtype: C{tuple}
        """
        return (self.__det_id, (self.__x_index, self.__y_index))

    def fromList(cls, ilist):
        """
        This method creates a L{NeXusId} object from a list containing the
        detector ID and the x and y pixel indicies.
        
        @param ilist: The object containing the detector ID and the x and y
                      pixel indicies.
        @type ilist: C{list}


        @return: A NeXus pixel ID
        @rtype: L{NeXusId}


        @raise RuntimeError: If the list is not of length 3.
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
        This method creates a L{NeXusId} object from a string containing the
        detector ID and the x and y pixel indicies. The allowed formats of the
        string are \"(bank1, (0, 0))\", \"bank1,0,0\" or \"bank1_0_0\".
        
        @param istr: The object containing the detector ID and the x and y
                     pixel indicies.
        @type istr: C{string}


        @return: A NeXus pixel ID
        @rtype: L{NeXusId}
        """
        if "(" in istr:
            parts = istr.split()
        elif "," in istr:
            parts = istr.split(',')
        elif "_" in istr:
            parts = istr.split('_')
        return NeXusId.fromList(parts)

    fromString = classmethod(fromString)

    

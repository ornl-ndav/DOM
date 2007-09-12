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

import indexselector

class ISelector(indexselector.IndexSelectorBase):
    """
    This class takes a NeXus spectrum ID and returns the index associated
    with the slowest varying position index.
    """

    def __init__(self, **kwargs):
        """
        C{ISelector} constructor
        """
        pass

    def getIndex(self, id):
        """
        Return the slowest varying pixel position index

        @param id: A NeXus spectrum ID. See L{IndexSelectorBase} for format.
        @type id: C{tuple}
        

        @return: The slowest varying pixel position index
        @rtype: C{int}
        """
        return id[1][0]

    def __str__(self):
        """
        This method provides the string representation of the C{ISelector}.
        """
        return "ISelector"

class JSelector(indexselector.IndexSelectorBase):
    """
    This class takes a NeXus spectrum ID and returns the index associated
    with the fastest varying position index.
    """

    def __init__(self, **kwargs):
        """
        C{JSelector} constructor
        """        
        pass

    def getIndex(self, id):
        """
        Return the fastest varying pixel position index

        @param id: A NeXus spectrum ID. See L{IndexSelectorBase} for format.
        @type id: C{tuple}

        
        @returns: The fastest varying pixel position index
        @rtype: C{int}
        """
        return id[1][1]

    def __str__(self):
        """
        This method provides the string representation of the C{JSelector}.
        """        
        return "JSelector"

class ZSelector(indexselector.IndexSelectorBase):
    """
    This class always returns zero from the getIndex function
    """

    def __init__(self, **kwargs):
        """
        C{ZSelector} constructor
        """                
        pass

    def getIndex(self, id):
        """
        Always return zero no matter what the index is.

        @param id: A NeXus spectrum ID. See L{IndexSelectorBase} for format.
        @type id: C{tuple}

        @returns: 0
        @rtype: C{int}
        """
        return 0

    def __str__(self):
        """
        This method provides the string representation of the C{ZSelector}.
        """                
        return "ZSelector"

class IJSelector(indexselector.IndexSelectorBase):
    """
    This class takes a NeXus spectrum ID and returns the index associated
    with the slowest varying position index.

    @ivar __N_j: The maximum value of the fastest varying index
    @type __N_j: C{int}
    """
    
    def __init__(self, **kwargs):
        """
        C{IJSelector} constructor

        @param kwargs: A list of keyword arguments that the class accepts

        @keyword Nj: The maximum value of the fastest running index
        @type Nj: C{int}
        """                
        try:
            input = kwargs["Nj"]
            if input is None:
                return None
            else:
                self.__N_j = int(input)
        except KeyError:
            raise RuntimeError("Need to provide the number of pixels for the "\
                               +"fastest running index")

    def getIndex(self, id):
        """
        Return the slowest varying pixel position index

        @param id: A NeXus spectrum ID. See L{IndexSelectorBase} for format.
        @type id: C{tuple}

        
        @returns: The slowest varying pixel position index
        @rtype: C{int}
        """
        
        return id[1][1] + self.__N_j * id[1][0]

    def __str__(self):
        """
        This method provides the string representation of the C{ZSelector}.
        """                        
        return "IJSelector (Nj=%d)" % self.__N_j
